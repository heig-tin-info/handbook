window.mkdocsWikipediaConfig = window.mkdocsWikipediaConfig || {};
window.mkdocsWikipediaConfig.domains = Object.assign(
  window.mkdocsWikipediaConfig.domains || {},
  {"wikipedia.org": {"language": "en", "summaryPath": "/api/rest_v1/page/summary/", "languageSubdomains": true}}
);
if (!window.mkdocsWikipediaConfig.defaultDomain) {
  window.mkdocsWikipediaConfig.defaultDomain = "wikipedia.org";
}
