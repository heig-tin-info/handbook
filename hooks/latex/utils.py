"""Utility functions for LaTeX processing."""

import re
from pathlib import Path
from urllib.parse import quote, urlparse, urlunparse

import unidecode


def escape_latex_chars(text: str) -> str:
    """Escape LaTeX special characters in a string."""
    mapping = [
        ("&", r"\&"),
        ("%", r"\%"),
        ("#", r"\#"),
        ("$", r"\$"),
        ("_", r"\_"),
        ("^", r"\^"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("\\", r"\textbackslash{}"),
    ]
    return "".join([c if c not in dict(mapping) else dict(mapping)[c] for c in text])


def to_kebab_case(name: str) -> str:
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


def points_to_mm(points: float) -> float:
    """Convert points to mm.
    1 point = 1/72 inch
    1 inch = 25.4 mm
    """
    return points * 25.4 / 72


def resolve_asset_path(file_path, path):
    """Resolve a relative path from a given file path."""
    if Path(file_path).name == "index.md":
        file_path = file_path.parent
    path = (file_path / path).resolve()
    if not path.exists():
        return None
    return path


def safe_quote(url):
    """Percent-encode a URL, preserving reserved characters."""
    parsed_url = urlparse(url)
    encoded_path = quote(parsed_url.path)
    encoded_query = quote(parsed_url.query)
    encoded_fragment = quote(parsed_url.fragment)
    return urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            encoded_path,
            parsed_url.params,
            encoded_query,
            encoded_fragment,
        )
    )


def is_valid_url(url):
    """Check if a URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
