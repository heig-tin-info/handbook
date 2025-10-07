""" This module contains functions to convert various formats to PDF. """

import logging
import mimetypes
import os
import re
import subprocess
import tempfile
from hashlib import sha256
from io import BytesIO
from math import ceil
from pathlib import Path
from typing import Union

import cairosvg
import pillow_avif  # noqa
import pypdf
import requests
import unidecode
from PIL import Image

log = logging.getLogger("mkdocs")

pillow_supported_types = Image.registered_extensions().keys()


def get_filename_from_content(content: Union[str, bytes], output_path: Path) -> Path:
    """Generate a filename from content.
    This renderer, store assets with files sometime
    generated from content. This function will generate
    a unique filename based on the content.
    """
    if isinstance(content, str):
        content = content.encode()
    digest = sha256(content).hexdigest()
    return output_path / digest


def fetch_image(url: str, output_path: Path) -> Path:
    """Fetch an image from an URL and store it in the output path.
    If the image already exists, it will not be fetched again.
    """
    response = requests.head(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image: {response.status_code}")

    mime_type = response.headers["Content-Type"]
    etag = response.headers.get("ETag")
    extension = mimetypes.guess_extension(mime_type)
    if not extension:
        raise ValueError(f"Unknown mime type: {mime_type}")

    filename = get_filename_from_content(
        f"ETag:{etag}\0{url}", output_path
    ).with_suffix(extension + ".pdf")

    if filename.exists():
        return filename

    # Fetch file
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image: {response.status_code}")

    # SVG case
    if extension == ".svg":
        filename = svg2pdf(response.content, output_path)
        return filename
    elif extension in pillow_supported_types:
        image = Image.open(BytesIO(response.content))
        image.convert("RGB").save(filename, "PDF")
    else:
        raise ValueError(
            f"Unsupported image type: {extension}, cannot be converted to PDF"
        )

    return filename


def image2pdf(filename, output_path=Path()):
    pdfpath = get_filename_from_content(filename, output_path).with_suffix(".pdf")

    if not pdfpath.exists():
        log.info("Converting %s to PDF...", filename)
        image = Image.open(filename)
        image.save(pdfpath, "PDF")

    return pdfpath


def get_docker_command(wdir: Path) -> list:
    return [
        "docker",
        "run",
        "-u",
        f"{os.getuid()}:{os.getgid()}",
        "-e",
        "HOME=/data/home",
        "-w",
        "/data",
        "-v",
        "/etc/passwd:/etc/passwd:ro",
        "-v",
        f"{wdir.absolute()}:/data",
    ]


def mermaid2pdf(
    content: Union[str, Path], output_path: Path = Path(), **kwargs
) -> Path:
    """Converts Mermaid content to PDF using the
    mermaid-cli docker image."""

    options = []

    if "config_filename" in kwargs:
        config = Path(kwargs["config_filename"]).read_text("utf-8")
        config_filename = get_filename_from_content(config, output_path).with_suffix(
            ".json"
        )
        config_filename.write_text(config)
        options += ["-c", f"{config_filename.name}"]

    if isinstance(content, str) and "\n" not in content:
        log.warning("Assuming content is a filename")
        content = Path(content)

    if isinstance(content, Path):
        content = content.read_text("utf-8")

    mmd_filename = get_filename_from_content(
        content + "".join(options), output_path
    ).with_suffix(".mmd")

    if "output" in kwargs:
        pdf_filename = Path(kwargs["output"])
    else:
        pdf_filename = mmd_filename.with_suffix(".mmd.pdf")

        if pdf_filename.exists():
            return pdf_filename

    # Docker is chrooted, file must be in the working directory
    mmd_filename.write_text(content)

    log.info("Converting mermaid diagram to PDF...")

    command = get_docker_command(mmd_filename.parent) + [
        "minlag/mermaid-cli",
        "-i",
        f"{mmd_filename.name}",
        "-f",
        "-t",
        "neutral",
        "-o",
        f"{pdf_filename.name}",
        *options,
    ]

    print(" ".join(str(e) for e in command))

    completed_process = subprocess.run(command, check=False, stderr=subprocess.PIPE)

    if completed_process.returncode != 0:
        log.error("Executing: %s", " ".join(str(e) for e in command))
        log.error("Return code %s", completed_process.returncode)

    for line in completed_process.stderr.splitlines():
        log.error("mermaid: %s", {line.decode()})

    if completed_process.returncode != 0:
        return None

    return pdf_filename


def up_to_date(source: Path, destination: Path) -> bool:
    """Check if a file is up to date.
    Does not work well with GitHub Actions cache.
    """
    return (
        destination.exists() and destination.stat().st_mtime >= source.stat().st_mtime
    )


def pdf2pdf15(filename: Path, output_path: Path) -> Path:
    """Convert a PDF to PDF 1.5 format."""
    command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.5",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-sOutputFile=" + str(output_path),
        str(filename),
    ]

    log.debug("Running command: %s", " ".join(str(e) for e in command))
    completed_process = subprocess.run(command, check=False)
    if completed_process.returncode != 0:
        log.error("Return code %s", completed_process.returncode)
        return None
    return output_path


def drawio2pdf(filename: Path, output_path: Path) -> Path:

    pdfpath = get_filename_from_content(filename.read_bytes(), output_path).with_suffix(
        ".drawio.pdf"
    )

    intermediate = output_path / filename.with_suffix(".pdf").name

    if not pdfpath.exists():
        log.info("Converting %s to PDF...", filename)

        pwd = Path().absolute()
        command = get_docker_command(pwd) + [
            "rlespinasse/drawio-desktop-headless",
            "--export",
            "--format",
            "pdf",
            #'--crop',
            "--output",
            f"{output_path.relative_to(pwd)}",
            f"{filename.relative_to(pwd)}",
        ]

        log.info("Running %s", " ".join(str(e) for e in command))

        # Recompile the svg file
        completed_process = subprocess.run(command, stderr=subprocess.PIPE, check=False)
        for line in completed_process.stderr.splitlines():
            ignore = [
                "Could not create a backing OpenGL context",
                "failed with error EGL_NOT_INITIALIZED",
                "Initialization of all EGL display types failed",
                "GLDisplayEGL::Initialize failed",
                "Exiting GPU process due to errors during initialization",
                "'font-feature-settings' is not a valid property name",
                "ContextResult::kTransientFailure: Failed to send",
                "libGL error: failed to load driver: swrast",
                "libGL error: MESA-LOADER: failed to open swrast",
                "Failed to connect to the bus",
            ]
            if not any([i in line.decode() for i in ignore]) and len(line.decode()) > 3:
                log.error("drawio: %s", line.decode())

        if completed_process.returncode != 0:
            log.error(
                "Could not process %s, return code %s",
                filename,
                completed_process.returncode,
            )
        else:
            # Drawio cannot output to a specific file,
            # so we need to move it manually :(
            # shutil.move(intermediate, pdfpath)

            # Instead of moving, we convert the file to PDF 1.5
            log.info(f"Converting {intermediate} to PDF 1.5 -> {pdfpath}")
            pdfpath = pdf2pdf15(intermediate, pdfpath)
            intermediate.unlink()
            log.debug("Command succeeded")

    return pdfpath


def image2pdf(filename, output_path=Path()):
    """Convert an existing image to PDF."""
    if not filename.exists():
        raise ValueError(f"File does not exist: {filename}")

    pdfpath = get_filename_from_content(filename.name, output_path).with_suffix(".pdf")

    if not pdfpath.exists():
        image = Image.open(filename)
        image.save(pdfpath, "PDF")

    return pdfpath


RE_VIEWBOX = re.compile(
    r'viewbox="0 0 (?P<width>\d+(?:\.\d+)?) (?P<height>\d+(?:\.\d+)?)"', re.IGNORECASE
)


def add_size_to_svg(svg: str) -> tuple:
    if isinstance(svg, bytes):
        svg = svg.decode("utf-8")

    def add_dimensions(match):
        svg_tag = match.group()

        if match := RE_VIEWBOX.search(svg_tag):
            height = ceil(float(match.group("height")))
            width = ceil(float(match.group("width")))
        elif "width" in svg_tag and "height" in svg_tag:
            return svg_tag
        else:
            raise ValueError("No viewbox found in SVG")

        if "width" not in svg_tag:
            svg_tag = re.sub(r">$", f' width="{width}" height="{height}">', svg_tag)
        return svg_tag

    svg = re.sub(r"<svg[^>]*>", add_dimensions, svg)

    return svg


def svg2pdf_cairo(svg: Union[str, Path], output_path=Path()) -> Path:
    if isinstance(svg, Path):
        svg = svg.read_text()

    pdfpath = get_filename_from_content(svg, output_path).with_suffix(".pdf")

    svg = add_size_to_svg(svg)

    if not pdfpath.exists():
        cairosvg.svg2pdf(bytestring=svg, write_to=str(pdfpath.with_suffix(".temp.pdf")))
        pdf2pdf15(pdfpath.with_suffix(".temp.pdf"), pdfpath)
        os.remove(pdfpath.with_suffix(".temp.pdf"))
    return pdfpath


def svg2pdf_inkscape(svg, output_path=Path()):
    log.info("Converting SVG to PDF...")
    # Create temporary svg file
    filename = Path(sha256(svg.encode()).hexdigest() + ".svg")
    svgpath = Path(os.path.join(tempfile.mkdtemp(), filename))
    with open(svgpath, "w") as fp:
        fp.write(svg)

    pdfpath = output_path / filename.with_suffix(".pdf")

    inkscape_version = subprocess.check_output(
        ["inkscape", "--version"], universal_newlines=True
    )
    log.debug(inkscape_version)

    # Convert
    # - 'Inkscape 0.92.4 (unknown)' to [0, 92, 4]
    # - 'Inkscape 1.1-dev (3a9df5bcce, 2020-03-18)' to [1, 1]
    # - 'Inkscape 1.0rc1' to [1, 0]
    inkscape_version = re.findall(r"[0-9.]+", inkscape_version)[0]
    inkscape_version_number = [int(part) for part in inkscape_version.split(".")]

    # Right-pad the array with zeros (so [1, 1] becomes [1, 1, 0])
    inkscape_version_number += [0] * (3 - len(inkscape_version_number))

    # Tuple comparison is like version comparison
    if inkscape_version_number < [1, 0, 0]:
        command = [
            "inkscape",
            "--export-area-drawing",
            "--export-dpi",
            "300",
            "--export-pdf",
            pdfpath,
            svgpath,
        ]
    else:
        command = [
            "inkscape",
            svgpath,
            "--export-area-drawing",
            "--export-dpi",
            "300",
            "--export-type=pdf",
            "--export-filename",
            pdfpath,
        ]

    log.debug("Running command: %s", " ".join(str(e) for e in command))

    # Recompile the svg file
    completed_process = subprocess.run(command)

    if completed_process.returncode != 0:
        log.error("Return code %s", completed_process.returncode)
    else:
        log.debug("Command succeeded")

    return pdfpath


svg2pdf = svg2pdf_cairo


def points_to_mm(points):
    return points * 25.4 / 72


def get_pdf_page_sizes(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    for page in reader.pages:
        media_box = page.mediabox
        width_pts = float(media_box.width)
        height_pts = float(media_box.height)
        width_mm = points_to_mm(width_pts)
        height_mm = points_to_mm(height_pts)
        return (width_mm, height_mm)
    return None


def to_kebab_case(name):
    """Converts a string to kebab case
    >>> to_kebab_case("Hello World")
    'hello-world'
    >>> to_kebab_case("Hello World!")
    'hello-world'
    >>> to_kebab_case("L'abricot")
    'l-abricot'
    >>> to_kebab_case("Éléphant")
    'elephant'
    """
    name = unidecode.unidecode(name)
    name = re.sub(r"[^\w\s']", "", name)
    name = re.sub(r"[\s']+", "-", name)
    return name.lower()
    name = re.sub(r"[\s']+", "-", name)
    return name.lower()
    return name.lower()
