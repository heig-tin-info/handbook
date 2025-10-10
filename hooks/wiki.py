"""Fetch and cache Wikipedia metadata referenced in MkDocs pages."""

from __future__ import annotations

import re
import urllib.parse
from collections.abc import Iterator
from html import unescape
from pathlib import Path
from typing import Any

import click
import requests
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils import log
from ruamel.yaml import YAML
from unidecode import unidecode
from voluptuous import Optional, Required, Schema
from voluptuous.error import MultipleInvalid

LINK_SCHEMA = Schema(
    {
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
    }
)


class Wikipedia:
    """Lightweight wrapper around the Wikipedia API with local caching."""

    def __init__(
        self,
        filename: Path | str = Path("links.yml"),
        lang: str = "en",
        timeout: int = 5,
    ) -> None:
        self.filename = Path(filename)
        self.language = lang
        self.base_url = f"https://{lang}.wikipedia.org"
        self.search_url = self.base_url + "/w/api.php"
        self.timeout = timeout
        self.data: dict[str, Any] = {}

    def get_api_url(self, language: str | None = None) -> str:
        """Return the REST API endpoint for the given language."""

        target_language = language or self.language
        return f"https://{target_language}.wikipedia.org/api/rest_v1"

    def search_from_keyword(
        self,
        keyword: str,
        limit: int = 5,
        interactive: bool = False,
    ) -> dict[str, str] | None:
        """Retrieve a Wikipedia link for the provided keyword."""

        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "srlimit": limit,
            "srsearch": keyword,
        }
        headers = {"User-Agent": "MkDocs-Wiki-Helper/1.0"}

        try:
            response = requests.get(
                self.search_url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            log.error(
                "Error while fetching wikipedia search for keyword: %s (%s)",
                keyword,
                exc,
            )
            return None

        data = response.json()
        query = data.get("query", {})
        results = query.get("search", [])
        if not results:
            log.error("No search results found for keyword: %s", keyword)
            return None

        if interactive:
            click.echo(f"Search results for keyword '{keyword}':")
            for index, result in enumerate(results):
                click.echo(f"   {index}: {result['title']}")

            choice = click.prompt("Choose a result", type=int)
            if choice < 0 or choice >= len(results):
                log.error("Invalid choice")
                return None
            result = results[choice]
        else:
            result = results[0]

        page_title = result["title"]
        page_url = f"{self.base_url}/wiki/{page_title.replace(' ', '_')}"
        return {
            "title": page_title,
            "url": page_url,
            "timestamp": result.get("timestamp", ""),
        }

    def fetch_summary(
        self,
        page_title: str,
        language: str | None = None,
    ) -> dict[str, Any] | None:
        """Fetch the page summary for the provided Wikipedia title."""

        api_url = self.get_api_url(language)
        summary_url = f"{api_url}/page/summary/{page_title}"

        try:
            response = requests.get(summary_url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            log.error(
                "Error while fetching wikipedia summary for page: %s (%s)",
                page_title,
                exc,
            )
            return None

        data = response.json()
        extract = data.get("extract", "")
        keep_keys = {"title", "thumbnail", "timestamp", "description", "extract", "tid"}
        filtered = {key: value for key, value in data.items() if key in keep_keys}
        if extract:
            filtered["extract"] = extract.strip()
        return filtered

    def load(self) -> None:
        """Load the cached metadata from disk if available."""

        default: dict[str, Any] = {"wikipedia": {}, "version": "0.2"}
        yaml = YAML()
        yaml.preserve_quotes = True

        if not self.filename.exists():
            self.data = default
            return

        with self.filename.open(encoding="utf-8") as handle:
            links = yaml.load(handle)

        try:
            self.data = LINK_SCHEMA(links)
        except (MultipleInvalid, TypeError) as exc:
            log.error("Invalid links file, regenerate it...", exc_info=exc)
            self.data = default
            return

        if self.data.get("version") != "0.2":
            log.error("Invalid version in links file, regenerate it...")
            self.data = default

    def save(self) -> None:
        """Persist the cached metadata to disk."""

        yaml = YAML()
        with self.filename.open("w", encoding="utf-8") as handle:
            yaml.dump(self.data, handle)

    def __contains__(self, keyword: str) -> bool:
        return keyword in self.data.get("wikipedia", {})

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        return iter(self.data.get("wikipedia", {}).items())

    def __getitem__(self, keyword: str) -> Any:
        return self.data["wikipedia"][keyword]

    def __setitem__(self, keyword: str, value: Any) -> None:
        self.data.setdefault("wikipedia", {})[keyword] = value


RE_WIKI_LINK = re.compile(
    r'<a[^>]+?href="(https?://([a-z]{2,3})\.wikipedia.org\/wiki/([^"]+))"'
)

wiki = Wikipedia(lang="fr")


def on_config(config: MkDocsConfig) -> None:
    """Load cached Wikipedia data before the build starts."""

    del config
    wiki.load()


def to_ascii(key: str) -> str:
    """Create a slug suitable for file-system usage."""

    decoded = urllib.parse.unquote(unescape(key)).replace("_", "-").lower()
    ascii_key = unidecode(decoded)
    return re.sub(r"[^\w-]", "", ascii_key)


def to_human_url(key: str) -> str:
    """Decode percent-encoded segments for display."""

    return urllib.parse.unquote(unescape(key))


def on_page_content(
    html: str,
    page: Page,
    config: MkDocsConfig,
    files: Files,
) -> str:
    """Collect Wikipedia links and ensure their metadata is cached."""

    del page, config, files

    for link in re.finditer(RE_WIKI_LINK, html):
        language = link.group(2)
        page_title = link.group(3)
        key = to_ascii(f"{language}-{page_title}")
        url = f"https://{language}.wikipedia.org/wiki/{page_title}"
        if url in wiki:
            continue

        log.info("Fetching wikipedia summary for '%s'", to_human_url(page_title))
        summary = wiki.fetch_summary(page_title.replace("/", r"%2F"), language)
        if summary:
            summary["key"] = key
            summary["plainlink"] = to_human_url(url)
            wiki[url] = summary

    return html


def on_env(env: Any, config: MkDocsConfig, files: Files) -> None:
    """Persist cached data at the end of the build."""

    del env, config, files
    wiki.save()

