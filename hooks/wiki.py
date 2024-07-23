""" Provide wikipedia link to the page """
import logging
import requests
import re
from ruamel.yaml import YAML
log = logging.getLogger('mkdocs')

def get_wiki_link(keyword, lang):
    search_url = f"https://{lang}.wikipedia.org/w/api.php"

    params = {
        'action': 'query',
        'list': 'search',
        'format': 'json',
        'srlimit': 5,
        'srsearch': keyword,
    }

    headers = {
        'User-Agent': 'MyWikipediaApp/1.0 (https://mywebsite.com)'
    }

    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()

    if 'query' in data and 'search' in data['query'] and len(data['query']['search']) > 0:
        page_title = data['query']['search'][0]['title']
        page_url = f"https://{lang}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        return page_url, page_title
    else:
        return None

links = {}

def on_config(config):
    global links
    yaml = YAML()
    yaml.preserve_quotes = True
    with open('links.yml') as f:
        links = yaml.load(f)
    if 'wikipedia' not in links:
        log.warning("No section wikipedia in links.yml")

def on_page_markdown(markdown, page, config, files):
    def replace_link(link):
        keyword = link.group(2)
        if not isinstance(links['wikipedia'], dict):
            links['wikipedia'] = {}
        if keyword not in links['wikipedia']:
            result = get_wiki_link(keyword, 'fr')
            if result is None:
                log.error(f"Unable to find wikipedia link for keyword: {keyword}")
                return link.group(0)
            url, title = result
            if url is not None:
                links['wikipedia'][keyword] = url
                log.warning(f"New wiki link discovered: {keyword}, guessing to be {title}")

        return f"{link.group(1)}{links['wikipedia'][keyword]}{link.group(3)}"

    return re.sub(r'(\[[^\]]+\]\()wiki:([^\)]+)(\))', replace_link, markdown)

def on_post_build(config):
    with open('links.yml', 'w') as f:
        yaml = YAML()
        yaml.dump(links, f)