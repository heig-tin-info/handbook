/**
 * MkDocs Material exposes a global `document$` variable, which is an RxJS-like observable
 * that emits events whenever a new page is loaded or re-rendered (for example, when
 * navigating through pages using instant loading).
 *
 * This allows custom scripts to re-run logic (such as initializing widgets, rendering
 * diagrams, or processing dynamic content) every time the page changes.
 *
 * The following code listens for document$ updates and re-processes Draw.io diagrams
 * whenever a new page is loaded.
 *
 * If `document$` is not defined (e.g. when using a different MkDocs theme),
 * the script does nothing gracefully.
 */
if (typeof document$ !== 'undefined') {
  document$.subscribe(({ body }) => {
    // Re-render Draw.io diagrams in the new page content
    GraphViewer.processElements();
  });
}

(() => {
  const css = `
    .geDiagramContainer,
    .geDiagramContainer svg,
    .mxgraph {
      color-scheme: normal !important;
    }
  `;
  const tag = document.createElement('style');
  tag.setAttribute('data-color-scheme-patch', '');
  tag.appendChild(document.createTextNode(css));
  document.head.appendChild(tag);
})();

function stripColorScheme(el) {
  if (el && el.nodeType === 1) {
    el.style.removeProperty('color-scheme');
  }
}

function stripInContainer(container) {
  if (!container || container.nodeType !== 1) return;
  stripColorScheme(container);
  container.querySelectorAll('svg[style*="color-scheme"]').forEach(stripColorScheme);
}

function colorSchemeToggle() {
  document.querySelectorAll('div.mxgraph').forEach(stripColorScheme);
  document.querySelectorAll('.geDiagramContainer').forEach(stripInContainer);
}

if (typeof document$ !== 'undefined' && typeof document$.subscribe === 'function') {
  document$.subscribe(() => colorSchemeToggle());
} else {
  document.addEventListener('DOMContentLoaded', colorSchemeToggle);
}

const observer = new MutationObserver(mutations => {
  for (const m of mutations) {
    if (m.type === 'childList') {
      m.addedNodes.forEach(node => {
        if (node.nodeType !== 1) return;
        if (node.classList && node.classList.contains('geDiagramContainer')) {
          stripInContainer(node);
        }
        node.querySelectorAll?.('.geDiagramContainer').forEach(stripInContainer);
        node.querySelectorAll?.('svg[style*="color-scheme"]').forEach(stripColorScheme);
      });
    } else if (m.type === 'attributes' && m.attributeName === 'style') {
      const el = m.target;
      if (el.style && el.style.colorScheme) {
        stripColorScheme(el);
      }
    }
  }
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
  attributes: true,
  attributeFilter: ['style']
});
