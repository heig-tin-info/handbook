import os
import subprocess
from hashlib import sha256
from pathlib import Path
import shutil
import logging
import tempfile
from PIL import Image
import cairosvg
import re
from typing import Union

log = logging.getLogger('mkdocs')


def mermaid2pdf(content, output_path=Path()):
    """Converts Mermaid content to PDF using the mermaid-cli docker image."""

    filename = (output_path / sha256(content.encode()).hexdigest()).with_suffix('.mmd')
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(content)

    pdfpath = output_path / filename.with_suffix('.pdf')

    command = [
        'docker',
        'run',
        '--rm',
        '-u', f'{os.getpid()}:{os.getgid()}',
        '-v', f'{output_path}:/data',
        'minlag/mermaid-cli',
        '-i', f'{filename}',
        '-f',
        '-o', f'{pdfpath}'
    ]

    completed_process = subprocess.run(command,
                                       check=False,
                                       stderr=subprocess.PIPE)

    for line in completed_process.stderr.splitlines():
        log.error("mermaid: %s", {line.decode()})

    if completed_process.returncode != 0:
        log.error('Return code %s', completed_process.returncode)
        return None

    os.remove(filename)

    return pdfpath

def drawio2pdf(filename, output_path=Path()):
    log.info("Converting Draw.io to PDF...")

    pdfpath = output_path / get_filename(filename).with_suffix('.pdf')
    intermediate = output_path / filename.with_suffix('.pdf').name
    # If destination path is older than source, recompile
    if not pdfpath.exists() or pdfpath.stat().st_mtime < filename.stat().st_mtime:
        command = [
            'drawio',
            '--export',
            '--format', 'pdf',
            '--crop',
            '--output', f'{output_path}',
            f"{filename}"
            ]
        log.info(f"Running {''.join(str(e) for e in command)}")

        # Recompile the svg file
        completed_process = subprocess.run(command, stderr=subprocess.PIPE)
        for line in completed_process.stderr.splitlines():
            ignore = [
                'Could not create a backing OpenGL context',
                'failed with error EGL_NOT_INITIALIZED',
                'Initialization of all EGL display types failed',
                'GLDisplayEGL::Initialize failed',
                'Exiting GPU process due to errors during initialization',
                "'font-feature-settings' is not a valid property name",
                'ContextResult::kTransientFailure: Failed to send',
                'libGL error: failed to load driver: swrast',
                'libGL error: MESA-LOADER: failed to open swrast',
            ]
            if not any([i in line.decode() for i in ignore]) and len(line.decode()) > 3:
                log.error(f"drawio: {line.decode()}")

        if completed_process.returncode != 0:
            log.error(f'Could not process {filename}, eturn code {completed_process.returncode}')
        else:
            # Drawio cannot output to a specific file,
            # so we need to move it manually :(
            shutil.move(intermediate, pdfpath)
            log.debug('Command succeeded')

    return pdfpath

def image2pdf(filename, output_path=Path()):
    log.info("Converting webp to PDF...")

    pdfpath = output_path / get_filename(filename).with_suffix('.pdf')

    if not pdfpath.exists() or pdfpath.stat().st_mtime < filename.stat().st_mtime:
        log.debug('Running command:')
        image = Image.open(filename)
        image.save(pdfpath, 'PDF')

    return pdfpath

def svg2pdf(svg: Union[str, Path], output_path=Path()) -> Path:
    log.info("Converting SVG to PDF...")


    if isinstance(svg, str):
        filename = output_path / get_filename(svg).with_suffix('.pdf')
        svgpath = Path(os.path.join(tempfile.mkdtemp(), filename))
        with open(svgpath, 'w') as fp:
            fp.write(svg)
        svg = svgpath
    elif isinstance(svg, Path):
        filename = svg
        svg = svg.read_bytes()
    else:
        raise ValueError(f"Unknown type {type(svg)}")

    pdfpath = output_path / get_filename(svg).with_suffix('.pdf')

    if not pdfpath.exists() or pdfpath.stat().st_mtime < filename.stat().st_mtime:
        cairosvg.svg2pdf(bytestring=svg, write_to=str(pdfpath))

    return pdfpath


def svg2pdf_old(svg, output_path=Path()):
    log.info("Converting SVG to PDF...")
    # Create temporary svg file
    filename = Path(sha256(svg.encode()).hexdigest() + '.svg')
    svgpath = Path(os.path.join(tempfile.mkdtemp(), filename))
    with open(svgpath, 'w') as fp:
        fp.write(svg)

    pdfpath = output_path / filename.with_suffix('.pdf')

    inkscape_version = subprocess.check_output(
        ['inkscape', '--version'], universal_newlines=True)
    log.debug(inkscape_version)

    # Convert
    # - 'Inkscape 0.92.4 (unknown)' to [0, 92, 4]
    # - 'Inkscape 1.1-dev (3a9df5bcce, 2020-03-18)' to [1, 1]
    # - 'Inkscape 1.0rc1' to [1, 0]
    inkscape_version = re.findall(r'[0-9.]+', inkscape_version)[0]
    inkscape_version_number = [int(part) for part in inkscape_version.split('.')]

    # Right-pad the array with zeros (so [1, 1] becomes [1, 1, 0])
    inkscape_version_number += [0] * (3 - len(inkscape_version_number))

    # Tuple comparison is like version comparison
    if inkscape_version_number < [1, 0, 0]:
        command = [
            'inkscape',
            '--export-area-drawing',
            '--export-dpi', '300',
            '--export-pdf',
            pdfpath,
            svgpath
            ]
    else:
        command = [
            'inkscape', svgpath,
            '--export-area-drawing',
            '--export-dpi', '300',
            '--export-type=pdf',
            '--export-filename',
            pdfpath
            ]

    log.debug('Running command: %s', ' '.join(str(e) for e in command))

    # Recompile the svg file
    completed_process = subprocess.run(command)

    if completed_process.returncode != 0:
        log.error('Return code %s', completed_process.returncode)
    else:
        log.debug('Command succeeded')

    return pdfpath
