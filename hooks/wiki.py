"""Provide local wikipedia links in MkDocs pages.

Wiki pages are captured and the summary and thumbnail are fetched from
the internet. The links are stored in a YAML file.
"""

import re
import urllib.parse
from html import unescape
from pathlib import Path

import click
import requests
from mkdocs.utils import log
from ruamel.yaml import YAML
from unidecode import unidecode
from voluptuous import Optional, Required, Schema

schema = Schema({
    Required("version"): str,
    Required("wikipedia"): {
        str: {
            Required("title"): str,
            Optional("tid"): str,
            Optional("description"): str,
            Optional("extract"): str,
            Optional("key"): str,
            Optional("thumbnail"): {
                Required("source"): str,
                Required("width"): int,
                Required("height"): int,
            },
            Optional("timestamp"): str,
            Optional("plainlink"): str,
        }
    },
})


class Wikipedia:
    """Class to manage wikipedia links."""

    def __init__(self, filename=Path("links.yml"), lang="en", timeout=5):
        self.filename = Path(filename)
        self.language = lang
        self.base_url = f"https://{lang}.wikipedia.org"
        self.search_url = self.base_url + "/w/api.php"
        self.api_url = self.base_url + "/api/rest_v1"
        self.timeout = timeout
        self.data = {}  # Populated by load()

    def get_api_url(self, language=None):
        """Get the API URL for a given language."""
        if not language:
            language = self.language
        return f"https://{language}.wikipedia.org/api/rest_v1"

    def search_from_keyword(self, keyword, limit=5, interactive=False):
        """Retrieve a wikipedia link for a given keyword in a given language.
        Be careful, keywords may not be unique and the first result is returned.
        """
        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "srlimit": limit,
            "srsearch": keyword,
        }

        headers = {"User-Agent": "MyWikipediaApp/1.0 (https://mywebsite.com)"}

        response = requests.get(
            self.search_url, headers=headers, params=params, timeout=5
        )

        if response.status_code != 200:
            log.error(
                "Error while fetching wikipedia search for keyword: %s (%s)",
                keyword,
                self.search_url,
            )
            return None

        data = response.json()
        if "query" not in data or "search" not in data["query"]:
            log.error("No search results found for keyword: %s", keyword)
            return None

        if interactive:
            print(f"Search results for keyword '{keyword}':")
            for i, result in enumerate(data["query"]["search"]):
                print(f"   {i}: {result['title']}")

            choice = click.prompt("Choose a result", type=int)
            if choice < 0 or choice >= len(data["query"]["search"]):
                log.error("Invalid choice")
                return None

            result = data["query"]["search"][choice]
        else:
            result = data["query"]["search"][0]

        page_title = result["title"]
        page_url = f"{self.base_url}/wiki/{page_title.replace(' ', '_')}"
        return {
            "title": page_title,
            "url": page_url,
            "timestamp": result["timestamp"],
        }

    def fetch_summary(self, page_title, language=None):
        """Fetch the summary of a wikipedia page."""
        api_url = self.get_api_url(language)
        summary_url = f"{api_url}/page/summary/{page_title}"
        response = requests.get(summary_url, timeout=self.timeout)
        if response.status_code != 200:
            log.error(
                "Error while fetching wikipedia summary for page: %s (%s)",
                page_title,
                summary_url,
            )
            return None
        data = response.json()
        keep_keys = ["title", "thumbnail", "timestamp", "description", "extract", "tid"]

        data["extract"] = data["extract"].strip()

        return {k: v for k, v in data.items() if k in keep_keys}

    def load(self):
        """Load the links from the YAML file."""
        default = schema({"wikipedia": {}, "version": "0.2"})
        yaml = YAML()
        yaml.preserve_quotes = True
        if not self.filename.exists():
            self.data = default
            return
        links = yaml.load(self.filename.open(encoding="utf-8"))
        try:
            self.data = schema(links)
        except Exception as e:
            log.error("Invalid links file, regenerate it: %s", e)
            self.data = default
            return
        if "version" not in self.data or self.data["version"] != "0.2":
            log.error("Invalid version in links file, regenerate it...")
            self.data = default

    def save(self):
        """Save the links to the YAML file."""
        yaml = YAML()
        yaml.dump(self.data, self.filename.open("w", encoding="utf-8"))

    def __contains__(self, keyword):
        return keyword in self.data["wikipedia"]

    @property
    def non_validated_links(self):
        """Return the non validated links."""
        return {k: v for k, v in self.data["wikipedia"].items() if not v["validated"]}

    def __iter__(self):
        return iter(self.data["wikipedia"].items())

    def __getitem__(self, keyword):
        return self.data["wikipedia"][keyword]

    def __setitem__(self, keyword, value):
        self.data["wikipedia"][keyword] = value


RE_WIKI_LINK = re.compile(
    r'<a[^>]+?href="(https?://([a-z]{2,3})\.wikipedia.org\/wiki\/([^"]+))"'
)

wiki = Wikipedia(lang="fr")


def on_config(config):
    """Load the wikipedia links file."""
    wiki.load()


def to_ascii(key):
    """Convert a key to an ASCII-safe format."""
    key = urllib.parse.unquote(unescape(key)).replace("_", "-").lower()
    key = unidecode(key)
    key = re.sub(r"[^\w-]", "", key)
    return key


def to_human_url(key):
    """Convert a URL-encoded key to a human-readable format."""
    return urllib.parse.unquote(unescape(key))


def on_page_content(html, page, config, files):
    """Process the page content to find wikipedia links."""
    for link in re.finditer(RE_WIKI_LINK, html):
        language = link.group(2)
        page_title = link.group(3)
        key = to_ascii(f"{language}-{page_title}")
        url = f"https://{language}.wikipedia.org/wiki/{page_title}"
        if url not in wiki:
            log.info("Fetching wikipedia summary for '%s'", to_human_url(page_title))
            summary = wiki.fetch_summary(page_title.replace("/", r"%2F"), language)
            if summary:
                wiki[url] = summary
                wiki[url]["key"] = key
                wiki[url]["plainlink"] = to_human_url(url)


def on_env(env, config, files):
    """Make the wikipedia links available in the Jinja2 environment."""
    wiki.save()
