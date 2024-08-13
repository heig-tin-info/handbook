"""Provide local wikipedia links in mkdocs pages.

Use the following syntax in your markdown files:

    [link text](wiki:keyword)

Where `keyword` is the keyword used to search on wikipedia.

It creates a local database in links.yml. It can be used to
generate glossary in printed version of the documentation.
"""

import re
from pathlib import Path
import requests
from ruamel.yaml import YAML
from mkdocs.utils import log
from voluptuous import Schema, Required, Optional
import click

schema = Schema(
    {
        "wikipedia": {
            str: {
                Required("url"): str,
                Required("title"): str,
                Required("validated", default=False): bool,
                Optional("tid"): str,
                Optional("description"): str,
                Optional("extract"): str,
                Optional("thumbnail"): {
                    Required("source"): str,
                    Required("width"): int,
                    Required("height"): int,
                },
                Optional("timestamp"): str,
            }
        }
    }
)


class Wikipedia:
    def __init__(self, filename=Path("links.yml"), lang="en", timeout=5):
        self.filename = Path(filename)
        self.language = lang
        self.base_url = f"https://{lang}.wikipedia.org"
        self.search_url = self.base_url + "/w/api.php"
        self.api_url = self.base_url + "/api/rest_v1"
        self.timeout = timeout
        self.data = {}  # Populated by load()

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
            log.error("Error while fetching wikipedia search for keyword: %s", keyword)
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

    def fetch_summary(self, page_title):
        summary_url = f"{self.api_url}/page/summary/{page_title}"
        response = requests.get(summary_url, timeout=self.timeout)
        if response.status_code != 200:
            log.error("Error while fetching wikipedia summary for page: %s", page_title)
            return None
        data = response.json()
        keep_keys = ["title", "thumbnail", "timestamp", "description", "extract", "tid"]

        return {k: v for k, v in data.items() if k in keep_keys}

    def update(self):
        """Update links with missing data from wikipedia API."""
        for keyword, entry in self:
            url = entry["url"]
            if "title" not in entry:
                title = url.split("/")[-1]
                entry["title"] = title

            if "tid" not in entry:
                log.info("Updating wikipedia summary for keyword %s", keyword)
                summary = self.fetch_summary(entry["title"])
                if summary:
                    entry.update(summary)
                else:
                    log.error(
                        "Unable to find wikipedia summary for keyword: %s",
                        keyword
                    )

    def load(self):
        yaml = YAML()
        yaml.preserve_quotes = True
        links = yaml.load(self.filename.open(encoding="utf-8"))
        self.data = schema(links)

    def save(self):
        yaml = YAML()
        yaml.dump(self.data, self.filename.open("w", encoding="utf-8"))

    def __contains__(self, keyword):
        return keyword in self.data["wikipedia"]

    @property
    def non_validated_links(self):
        return {k: v for k, v in self.data["wikipedia"].items() if not v["validated"]}

    def __iter__(self):
        return iter(self.data["wikipedia"].items())

    def __getitem__(self, keyword):
        return self.data["wikipedia"][keyword]

    def __setitem__(self, keyword, value):
        self.data["wikipedia"][keyword] = value
        self.data["wikipedia"][keyword].setdefault("validated", False)


RE_WIKI_LINK = re.compile(r"(\[[^\]]+\]\()wiki:([^\)]+)(\))")

wiki = Wikipedia(lang="fr")


def on_config(config):
    wiki.load()
    wiki.update()


def on_page_markdown(markdown, page, config, files):
    def replace_link(link):
        keyword = link.group(2)

        if keyword not in wiki:
            result = wiki.search_from_keyword(keyword, interactive=True)

            if result is None:
                log.error("Unable to find wikipedia link for keyword: %s", keyword)
                return link.group(0)

            wiki[keyword] = result

        return f"{link.group(1)}{wiki[keyword]['url']}{link.group(3)}"

    return re.sub(RE_WIKI_LINK, replace_link, markdown)


def on_post_build(config):
    wiki.save()
