(() => {
  const defaults = {
    summaryPath: "/api/rest_v1/page/summary/",
  };

  const globalConfig = window.mkdocsWikipediaConfig || {};
  const domainEntries = Object.entries(globalConfig.domains || {});

  const domainMap = domainEntries.length
    ? domainEntries.reduce((acc, [domain, config]) => {
        const normalized = Object.assign({}, config);
        normalized.domain = domain;
        normalized.summaryPath = (normalized.summaryPath || defaults.summaryPath).endsWith("/")
          ? normalized.summaryPath
          : `${normalized.summaryPath}/`;
        normalized.domainParts = domain.split(".");
        acc[domain] = normalized;
        return acc;
      }, {})
    : {
        "wikipedia.org": {
          domain: "wikipedia.org",
          language: "en",
          summaryPath: defaults.summaryPath,
          languageSubdomains: true,
          domainParts: "wikipedia.org".split("."),
        },
      };

  const defaultDomain = globalConfig.defaultDomain && domainMap[globalConfig.defaultDomain]
    ? globalConfig.defaultDomain
    : Object.keys(domainMap)[0];

  const processedFlag = "data-wiki-popup-bound";

  const findDomainConfig = (hostname) => {
    const parts = hostname.split(".");
    for (const domain of Object.keys(domainMap)) {
      const config = domainMap[domain];
      if (parts.length >= config.domainParts.length) {
        const tail = parts.slice(-config.domainParts.length).join(".");
        if (tail === domain) {
          return { config, parts };
        }
      }
    }
    return null;
  };

  const ready = (callback) => {
    if (typeof window.document$ !== "undefined" && window.document$ !== null) {
      window.document$.subscribe(() => callback(document));
    } else if (document.readyState === "loading") {
      document.addEventListener(
        "DOMContentLoaded",
        () => callback(document),
        { once: true },
      );
    } else {
      callback(document);
    }
  };

  const selectWikiLinks = (root) =>
    Array.from(root.querySelectorAll("a[href]")).filter((link) => {
      if (link.hasAttribute(processedFlag) || link.querySelector("abbr")) {
        return false;
      }
      let url;
      try {
        url = new URL(link.href, window.location.href);
      } catch {
        return false;
      }
      if (!/^https?:$/.test(url.protocol)) {
        return false;
      }
      const match = findDomainConfig(url.host);
      if (!match) {
        return false;
      }
      if (!url.pathname.startsWith("/wiki/")) {
        return false;
      }
      link.__wikiDomainConfig = match.config;
      return true;
    });

  const createPopup = () => {
    const popup = document.createElement("div");
    popup.className = "wiki-popup";
    return popup;
  };

  const positionPopup = (popup, link) => {
    const rect = link.getBoundingClientRect();
    popup.style.top = `${rect.bottom + window.scrollY}px`;
    popup.style.left = `${rect.left + window.scrollX}px`;
    popup.style.display = "block";
  };

  const renderSummary = (popup, data) => {
    popup.innerHTML = "";

    if (data.thumbnail && data.thumbnail.source) {
      const image = document.createElement("img");
      image.src = data.thumbnail.source;
      image.alt = data.title ? `${data.title} thumbnail` : "Wikipedia thumbnail";
      popup.appendChild(image);
    }

    const container = document.createElement("div");
    container.className = "wiki-popup-container";

    if (data.title) {
      const title = document.createElement("h2");
      title.textContent = data.title;
      container.appendChild(title);
    }

    const description = data.extract || data.description;
    if (description) {
      const extract = document.createElement("p");
      extract.textContent = description;
      container.appendChild(extract);
    }

    if (!container.childNodes.length) {
      const fallback = document.createElement("p");
      fallback.textContent = "No summary available";
      container.appendChild(fallback);
    }

    popup.appendChild(container);
  };

  const showError = (popup, message) => {
    popup.innerHTML = "";
    const paragraph = document.createElement("p");
    paragraph.textContent = message;
    popup.appendChild(paragraph);
  };

  const sanitizeTitle = (pathname) =>
    pathname.replace(/^\/wiki\//, "").replace(/\//g, "%2F");

  const summaryUrlFor = (url, config) =>
    `${url.origin}${config.summaryPath}${sanitizeTitle(url.pathname)}`;

  const destroyPopup = (link) => {
    if (link.__wikiPopup) {
      link.__wikiPopup.remove();
      link.__wikiPopup = null;
    }
  };

  const attachHandlers = (link) => {
    link.setAttribute(processedFlag, "true");

    link.addEventListener("mouseenter", async () => {
      destroyPopup(link);
      const popup = createPopup();
      link.__wikiPopup = popup;
      document.body.appendChild(popup);

      let url;
      try {
        url = new URL(link.href, window.location.href);
      } catch {
        showError(popup, "Invalid link");
        positionPopup(popup, link);
        return;
      }

      const domainConfig = link.__wikiDomainConfig || domainMap[defaultDomain];

      try {
        const response = await fetch(summaryUrlFor(url, domainConfig));
        if (!response.ok) {
          showError(popup, "Could not retrieve summary");
        } else {
          const data = await response.json();
          if (link.__wikiPopup === popup) {
            renderSummary(popup, data);
          }
        }
      } catch {
        showError(popup, "Error fetching summary");
      }

      if (link.__wikiPopup === popup) {
        positionPopup(popup, link);
      }
    });

    link.addEventListener("mouseleave", () => {
      destroyPopup(link);
    });
  };

  const enhance = (root) => {
    selectWikiLinks(root).forEach(attachHandlers);
  };

  ready(enhance);
})();
