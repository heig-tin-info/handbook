import requests
from hashlib import sha256
from pathlib import Path
import mimetypes
import logging
from typing import Union

log = logging.getLogger('mkdocs')

def escape_all_latex_chars(self, text):
    mapping = [
        ('&', r'\&'),
        ('%', r'\%'),
        ('#', r'\#'),
        ('$', r'\$'),
        ('_', r'\_'),
        ('\\', r'\textbackslash'),
    ]
    return ''.join([c if c not in dict(mapping) else dict(mapping)[c]
                    for c in text])

def escape_latex_chars(text):
    mapping = [
        ('&', r'\&'),
        ('%', r'\%'),
        ('#', r'\#'),
        #('$', r'\$'),
        #('_', r'\_'),
        #('\\', r'\textbackslash'),
    ]
    return ''.join([c if c not in dict(mapping) else dict(mapping)[c] for c in text])

def fetch_image(url, output_path=Path()):
    log.info(f"Fetching image {url}...")

    # Check if the url is valid
    response = requests.head(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image: {response.status_code}")

    mime_type = response.headers['Content-Type']
    etag = response.headers.get('ETag')
    extension = mimetypes.guess_extension(mime_type)
    if not extension:
        raise ValueError(f"Unknown mime type: {mime_type}")

    filename = (output_path / sha256(f"ETag:{etag}\0{url}".encode()).hexdigest()).with_suffix(extension)

    if filename.exists():
        return filename

    # Fetch file
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image: {response.status_code}")

    with open(filename, 'wb') as fp:
        fp.write(response.content)
    return filename

def get_class(element, regex):
    return next((c for c in element.get('class', []) if regex.match(c)), None)

def get_filename(filename: Union[str, Path]):
    if isinstance(filename, bytes):
        digest = sha256(filename).hexdigest()
        return Path(digest + '.unknown')
    else:
        if not filename.exists():
            raise ValueError(f"File not found: {filename}")
        digest = sha256(filename.read_bytes()).hexdigest()
        return Path(digest + filename.suffix)

def optimize_list(numbers):
    """Optimize a list of numbers to a list of ranges.
    >>> optimize_list([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16])
    ['1-6', '8-10', '12', '14-16']
    """
    if not numbers:
        return []

    numbers = sorted(numbers)
    optimized = []
    start = end = numbers[0]

    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            optimized.append(f"{start}-{end}" if start != end else str(start))
            start = end = num

    optimized.append(f"{start}-{end}" if start != end else str(start))
    return optimized




def get_depth(element):
    depth = 0
    while element.parent is not None:
        element = element.parent
        depth += 1
    return depth

def find_all_dfs(soup, *args, **kwargs):
    items = []
    for el in soup.find_all(*args, **kwargs):
        level = get_depth(el)
        items.append((level, el))
    return [item for _, item in sorted(items, key=lambda x: x[0], reverse=True)]
