/**
 * Draw.io SVG normalization & theme-aware colorization for MkDocs Material.
 * - Converts <img src="...drawio..."> to inline GraphViewer blocks
 * - Normalizes SVG paint attributes (fill/stroke/stop-color)
 * - Preserves CSS light-dark(light, dark) exactly; no heuristic darkening if provided
 * - Preserves RGBA alpha and composes with existing *-opacity attributes
 * - Reacts to theme changes (attribute on <html>/<body>, system, storage)
 *
 * Public surface:
 *   - window.drawioConverter(xml, idx?)
 *   - window.normalizeRenderedSvg(root?)
 */
(() => {
  // ----------------------------- Constants ---------------------------------
  const DARK_BACKGROUND = "#0f172a";
  const EMULATE_LIGHT_DARK_FALLBACK = false;

  const prefersDark =
    typeof window !== "undefined" && window.matchMedia
      ? window.matchMedia("(prefers-color-scheme: dark)")
      : null;

  // -------------------------- Color utilities -------------------------------
  function ensureColorEngine() {
    if (typeof window === "undefined") return null;
    const { colord } = window;
    if (!colord) return null;

    if (!colord.__mxgExtended) {
      const plugins = [];
      if (window.colordMixPlugin) plugins.push(window.colordMixPlugin);
      if (window.colordLabPlugin) plugins.push(window.colordLabPlugin);
      if (plugins.length && typeof colord.extend === "function") {
        try {
          colord.extend(plugins);
        } catch (err) {
          console.warn("colord plugin extension failed", err);
        }
      }
      colord.__mxgExtended = true;
    }
    return colord;
  }

  // Detect `light-dark(light, dark)` and return both sides
  function parseLightDark(cssText) {
    if (typeof cssText !== "string") return null;
    const m = cssText.match(/light-dark\(\s*([^)]+?)\s*,\s*([^)]+?)\s*\)/i);
    if (!m) return null;
    return { light: m[1].trim(), dark: m[2].trim() };
  }

  // Basic hex/rgb helpers
  function hexToRgb(hex) {
    let s = hex.replace(/^#/, "");
    if (s.length === 3)
      s = s
        .split("")
        .map((c) => c + c)
        .join("");
    const num = parseInt(s, 16);
    if (Number.isNaN(num)) return null;
    return [num >> 16, (num >> 8) & 255, num & 255];
  }

  function rgbToHex(r, g, b) {
    const clamp = (v) => Math.max(0, Math.min(255, Math.round(v)));
    return `#${[r, g, b]
      .map((c) => clamp(c).toString(16).padStart(2, "0"))
      .join("")}`;
  }

  function rgbToHsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    const max = Math.max(r, g, b),
      min = Math.min(r, g, b);
    let h = 0,
      s = 0,
      l = (max + min) / 2;
    if (max !== min) {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r:
          h = (g - b) / d + (g < b ? 6 : 0);
          break;
        case g:
          h = (b - r) / d + 2;
          break;
        default:
          h = (r - g) / d + 4;
      }
      h *= 60;
    }
    return [h, s, l];
  }

  function hslToRgb(h, s, l) {
    h /= 360;
    let r, g, b;
    if (s === 0) {
      r = g = b = l;
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1 / 6) return p + (q - p) * 6 * t;
        if (t < 1 / 2) return q;
        if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
        return p;
      };
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hue2rgb(p, q, h + 1 / 3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1 / 3);
    }
    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
  }

  function relativeLuminance(hex) {
    const rgb = hexToRgb(hex);
    if (!rgb) return null;
    const [r, g, b] = rgb.map((c) => {
      const v = c / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }

  function isNearWhite(hex) {
    const l = relativeLuminance(hex);
    return l !== null && l >= 0.9;
  }

  function isNearBlack(hex) {
    const l = relativeLuminance(hex);
    return l !== null && l <= 0.1;
  }

  // Parse a color string into hex + optional alpha
  function parseColorWithAlpha(value) {
    if (typeof value !== "string") return null;
    const v = value.trim().toLowerCase();
    if (
      !v ||
      v === "none" ||
      v === "transparent" ||
      v.startsWith("var(") ||
      v.startsWith("url(")
    )
      return null;

    // #rgb or #rrggbb
    const hexMatch = v.match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
    if (hexMatch) {
      let hex = hexMatch[1];
      if (hex.length === 3)
        hex = hex
          .split("")
          .map((c) => c + c)
          .join("");
      return { hex: `#${hex}`, alpha: null };
    }

    // rgb()/rgba()
    const rgbMatch = v.match(/^rgba?\(([^)]+)\)$/i);
    if (rgbMatch) {
      const parts = rgbMatch[1].split(",").map((p) => p.trim());
      if (parts.length >= 3) {
        const clamp = (n) => Math.max(0, Math.min(255, Math.round(n)));
        const ch = (raw) =>
          raw.endsWith("%")
            ? clamp((parseFloat(raw) / 100) * 255)
            : clamp(parseFloat(raw));
        const aVal = (raw) =>
          raw.endsWith("%") ? parseFloat(raw) / 100 : parseFloat(raw);
        const [rRaw, gRaw, bRaw, aRaw] = parts;
        const r = ch(rRaw),
          g = ch(gRaw),
          b = ch(bRaw);
        if ([r, g, b].some(Number.isNaN)) return null;
        const hex = rgbToHex(r, g, b);
        const alpha = aRaw !== undefined ? aVal(aRaw) : null;
        return {
          hex,
          alpha: alpha != null && !Number.isNaN(alpha) ? alpha : null,
        };
      }
    }
    return null;
  }

  // Heuristic darkening fallback (only used if no author dark value is provided)
  function toDark(hex, prop) {
    if (!hex) return hex;
    const normalized = hex.toLowerCase();

    if (isNearWhite(normalized)) return "#000000";
    if (isNearBlack(normalized)) return "#ffffff";

    const engine = ensureColorEngine();
    if (engine) {
      try {
        let color = engine(hex);
        if (color && typeof color.isValid === "function" && !color.isValid())
          color = null;

        if (color) {
          const luminance =
            typeof color.luminance === "function" ? color.luminance() : null;
          const mixRatio =
            luminance !== null ? (luminance > 0.7 ? 0.6 : 0.4) : 0.5;

          if (typeof color.mix === "function") {
            color = color.mix(DARK_BACKGROUND, mixRatio, "lab");
          } else if (typeof color.darken === "function") {
            color = color.darken(mixRatio * 0.5);
          }
          if (typeof color.desaturate === "function")
            color = color.desaturate(0.15);

          if (prop === "stroke" && typeof color.contrast === "function") {
            const contrast = color.contrast(DARK_BACKGROUND);
            if (contrast < 4.5) {
              if (typeof color.mix === "function")
                color = color.mix("#ffffff", 0.65, "lab");
              else if (typeof color.lighten === "function")
                color = color.lighten(0.35);
              else return "#ffffff";
            }
          }
          return color.toHex();
        }
      } catch (err) {
        console.warn("colord conversion failed, fallback to HSL", err);
      }
    }

    const rgb = hexToRgb(hex);
    if (!rgb) return hex;
    const [r, g, b] = rgb;
    const [h, s, l] = rgbToHsl(r, g, b);
    const lightnessAdjust = l > 0.7 ? 0.45 : 0.65;
    const saturationAdjust = s * 0.75;
    const hueAdjust = (h + 10) % 360;
    const newL = Math.pow(lightnessAdjust * l, 1.1);
    const [nr, ng, nb] = hslToRgb(hueAdjust, saturationAdjust, newL);
    return rgbToHex(nr, ng, nb);
  }

  // ------------------------- SVG normalization ------------------------------
  function storePaintReference(el, prop, sourceValue) {
    if (!sourceValue) return false;
    const trimmed = sourceValue.trim();
    if (!trimmed || trimmed === "none" || trimmed === "transparent")
      return false;

    const lightDark = parseLightDark(trimmed);

    // Helper to set both color and optional opacity for a theme
    const setThemePaint = (themeKey, parsedColor) => {
      if (!parsedColor) return false;
      const colorAttr = `data-${themeKey}-${prop}`;
      const opacityAttr = `data-${themeKey}-${prop}-opacity`;
      if (!el.hasAttribute(colorAttr))
        el.setAttribute(colorAttr, parsedColor.hex);
      if (parsedColor.alpha != null && !el.hasAttribute(opacityAttr)) {
        el.setAttribute(opacityAttr, String(parsedColor.alpha));
      }
      return true;
    };

    if (lightDark) {
      // Exact colors provided by the SVG author → store both
      const lightParsed = parseColorWithAlpha(lightDark.light);
      const darkParsed = parseColorWithAlpha(lightDark.dark);
      const okL = lightParsed && setThemePaint("light", lightParsed);
      const okD = darkParsed && setThemePaint("dark", darkParsed);
      return !!(okL || okD);
    }

    // Single color → set as light; derive dark only if missing
    const single = parseColorWithAlpha(trimmed);
    if (!single) return false;

    const lightAttr = `data-light-${prop}`;
    const darkAttr = `data-dark-${prop}`;

    if (!el.hasAttribute(lightAttr)) el.setAttribute(lightAttr, single.hex);
    if (single.alpha != null) {
      const opaAttr = `data-light-${prop}-opacity`;
      if (!el.hasAttribute(opaAttr))
        el.setAttribute(opaAttr, String(single.alpha));
    }

    if (!el.hasAttribute(darkAttr)) {
      el.setAttribute(darkAttr, toDark(single.hex, prop));
    }
    return true;
  }

  function styleHasLightDark(el, prop) {
    if (!el || !el.style || typeof el.getAttribute !== "function") return false;
    const styleAttr = el.getAttribute("style") || "";
    // recherche robuste de "prop: ...light-dark(...)" (insensible à la casse / espaces)
    const re = new RegExp(`${prop}\\s*:\\s*[^;]*light-dark\\s*\\(`, "i");
    return re.test(styleAttr);
  }

  function applyThemePaint(el, prop, theme) {
    const colorAttr =
      theme === "dark" ? `data-dark-${prop}` : `data-light-${prop}`;
    const opacityAttr =
      theme === "dark"
        ? `data-dark-${prop}-opacity`
        : `data-light-${prop}-opacity`;
    const color = el.getAttribute(colorAttr);
    const alpha = el.getAttribute(opacityAttr);

    // 3.1 Si le style inline contient light-dark() pour cette prop,
    //     on NE TOUCHE PAS AU style pour préserver le texte de light-dark().
    //     À la place, on pose la couleur sur l'ATTRIBUT de présentation, qui
    //     servira de fallback si le style est ignoré par le navigateur.
    if (styleHasLightDark(el, prop)) {
      if (EMULATE_LIGHT_DARK_FALLBACK) {
        if (color) el.setAttribute(prop, color); // ex: fill="#rrggbb"

        if (alpha != null) {
          const opaProp =
            prop === "stroke"
              ? "stroke-opacity"
              : prop === "fill"
                ? "fill-opacity"
                : prop === "stop-color"
                  ? "stop-opacity"
                  : null;
          if (opaProp) {
            // Compose avec l'existant (si présent)
            const existingAttr = el.getAttribute(opaProp);
            const existing =
              existingAttr != null ? parseFloat(existingAttr) : null;
            const parsed = parseFloat(alpha);
            const finalAlpha =
              !Number.isNaN(parsed) && parsed != null
                ? existing != null && !Number.isNaN(existing)
                  ? existing * parsed
                  : parsed
                : null;
            if (finalAlpha != null)
              el.setAttribute(opaProp, String(finalAlpha));
          }
        }
      }
      // On s'arrête ici : pas de setProperty(...), donc le light-dark() reste visible dans l'attribut style.
      return;
    }

    // 3.2 Sinon, comportement standard : on force via style (important) + alpha
    if (color) el.style.setProperty(prop, color, "important");

    if (alpha != null) {
      const opaProp =
        prop === "stroke"
          ? "stroke-opacity"
          : prop === "fill"
            ? "fill-opacity"
            : prop === "stop-color"
              ? "stop-opacity"
              : null;
      if (opaProp) {
        const existingAttr = el.getAttribute(opaProp);
        const existing = existingAttr != null ? parseFloat(existingAttr) : null;
        const parsed = parseFloat(alpha);
        const finalAlpha =
          !Number.isNaN(parsed) && parsed != null
            ? existing != null && !Number.isNaN(existing)
              ? existing * parsed
              : parsed
            : null;
        if (finalAlpha != null) el.setAttribute(opaProp, String(finalAlpha));
      }
    }
  }

  function normalizePaintAttributes(el, theme) {
    const props = ["fill", "stroke", "stop-color"];

    // Convert attributes to data-* and remove original attributes
    props.forEach((attr) => {
      const v = el.getAttribute(attr);
      if (v) {
        // On stocke la référence, mais on NE SUPPRIME PLUS l'attribut d'origine
        // afin de préserver le markup initial et permettre un fallback si le style est invalide.
        storePaintReference(el, attr, v);
      }
    });

    // Convert inline styles (if present) to data-* (we don't edit the style string)
    props.forEach((prop) => {
      const inline = el.style?.getPropertyValue?.(prop);
      if (inline) storePaintReference(el, prop, inline);
    });

    // Apply themed paint (+ alpha) as authoritative values
    props.forEach((prop) => applyThemePaint(el, prop, theme));
  }

  function normalizeSvgElement(el, theme) {
    // Do not strip style; we override target properties with !important anyway
    normalizePaintAttributes(el, theme);
  }

  function resolveTheme() {
    const attrBody = document.body?.getAttribute("data-md-color-scheme");
    const attrHtml = document.documentElement?.getAttribute(
      "data-md-color-scheme"
    );
    const attr = attrBody || attrHtml;
    // MkDocs Material: "slate" is the dark palette
    return attr === "slate" ? "dark" : "light";
  }

  function normalizeRenderedSvg(root = document) {
    if (!root) return;
    const theme = resolveTheme();
    const containers = root.querySelectorAll("div.mxgraph");

    containers.forEach((mx) => {
      mx.style.setProperty("color-scheme", "normal", "important"); // isolate from page color-scheme
      const svg = mx.querySelector("svg");
      if (!svg) return;

      normalizeSvgElement(svg, theme);
      svg.querySelectorAll("*").forEach((el) => normalizeSvgElement(el, theme));
    });
  }

  // Expose for late calls
  window.normalizeRenderedSvg = normalizeRenderedSvg;

  // --------------------------- HTML helpers ---------------------------------
  const htmlEscapeMap = {
    "&": "&amp;",
    "'": "&#x27;",
    "`": "&#x60;",
    '"': "&quot;",
    "<": "&lt;",
    ">": "&gt;",
  };

  function escapeHTML(str) {
    if (typeof str !== "string") return str;
    return str.replace(/[&'`"<>]/g, (m) => htmlEscapeMap[m]);
  }

  // ------------------------- Draw.io conversion -----------------------------
  window.drawioConverter = function drawioConverter(xml, idx = Date.now()) {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xml, "text/xml");
    const mxfile = xmlDoc.getElementsByTagName("mxfile")[0];
    const model = mxfile?.getElementsByTagName("mxGraphModel")[0];

    const canvasWidth = model?.getAttribute("pageWidth") || undefined;
    const canvasHeight = model?.getAttribute("pageHeight") || undefined;

    const mxGraphData = {
      "auto-origin": false,
      "auto-crop": false,
      "auto-fit": false,
      "zoom-enabled": false,
      zoomEnabled: false,
      canvasWidth,
      canvasHeight,
      xml,
    };

    const json = JSON.stringify(mxGraphData);
    return `
      <div class="drawio-viewer-index-${idx}">
        <div class="mxgraph" style="max-width:100%;border:1px solid transparent" data-mxgraph="${escapeHTML(
      json
    )}"></div>
      </div>
    `;
  };

  // ------------------------ GraphViewer integration -------------------------
  function processGraphViewerElements(classname = "mxgraph") {
    const GV = window.GraphViewer;
    const mxUtils = window.mxUtils;

    if (!GV || !mxUtils || typeof GV.getElementsByClassName !== "function")
      return;

    window.mxUtils.forEach(GV.getElementsByClassName(classname), (div) => {
      try {
        div.textContent = "";
        GV.createViewerForElement(div, () => {
          /* no-op hook */
        });
      } catch (e) {
        div.textContent = e?.message || "Graph render error";
        console.error(e);
      }
    });
  }

  if (window.GraphViewer) {
    window.GraphViewer.processElements = processGraphViewerElements;
  }

  // ----------------------------- Lifecycle ----------------------------------
  function onThemeChanged() {
    try {
      normalizeRenderedSvg();
    } catch {
      /* noop */
    }
  }

  function installThemeObservers() {
    // Observe 'data-md-color-scheme' on both <html> and <body>
    const observeTarget = (node) => {
      if (!node) return null;
      const obs = new MutationObserver((muts) => {
        for (const m of muts) {
          if (
            m.type === "attributes" &&
            m.attributeName === "data-md-color-scheme"
          )
            onThemeChanged();
        }
      });
      obs.observe(node, {
        attributes: true,
        attributeFilter: ["data-md-color-scheme"],
      });
      return obs;
    };
    observeTarget(document.documentElement);
    observeTarget(document.body);

    // System dark-mode changes
    if (prefersDark?.addEventListener) {
      prefersDark.addEventListener("change", onThemeChanged);
    } else if (prefersDark?.addListener) {
      prefersDark.addListener(onThemeChanged); // legacy Safari
    }

    // Palette toggled from another tab (Material stores under __palette)
    window.addEventListener("storage", (ev) => {
      if (ev.key === "__palette") onThemeChanged();
    });
  }

  async function replaceDrawioImagesAndRender() {
    const images = document.querySelectorAll('img[src*="drawio"]');
    for (const img of images) {
      try {
        const resp = await fetch(img.src);
        if (!resp.ok)
          throw new Error("Network error while fetching drawio XML");
        const xml = await resp.text();

        const newHtml = window.drawioConverter(xml, Date.now());
        const tmp = document.createElement("div");
        tmp.innerHTML = newHtml;
        const block = tmp.firstElementChild;

        img.parentNode.replaceChild(block, img);
      } catch (err) {
        console.error("Failed to process", img.src, err);
      }
    }

    try {
      window.GraphViewer?.processElements();
    } catch (e) {
      console.error(e);
    }
    normalizeRenderedSvg();
  }

  // Initial hooks
  document.addEventListener("DOMContentLoaded", () => {
    installThemeObservers();
    // If no router events are available, run once on load
    replaceDrawioImagesAndRender();
    normalizeRenderedSvg();
  });

  // MkDocs Material "instant loading" re-renders page content
  if (typeof window.document$?.subscribe === "function") {
    window.document$.subscribe(() => {
      replaceDrawioImagesAndRender();
    });
  }
})();
