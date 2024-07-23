// Once dom is ready
document.addEventListener("DOMContentLoaded", function () {
    console.log("Installing converter");
    const chatMap = {
        "&": "&amp;",
        "'": "&#x27;",
        "`": "&#x60;",
        '"': "&quot;",
        "<": "&lt;",
        ">": "&gt;",
    };
    const escapeHTML = (string) => {
        if (typeof string !== "string") return string;
        return string.replace(/[&'`"<>]/g, function (match) {
            return chatMap[match];
        });
    };
    window.drawioConverter = function (xml, idx = new Date().getTime()) {
        let mxGraphData = {
            editable: false,
            highlight: "#0000ff",
            nav: false,
            toolbar: null,
            edit: null,
            resize: true,
            lightbox: "open",
            // "check-visible-state": false,
            // "auto-fit": false,
            // move: false,
            xml,
        };

        const json = JSON.stringify(mxGraphData);

        return `<div class="drawio-viewer-index-${idx}">
          <div class="mxgraph" style="max-width: 100%; border: 1px solid transparent" data-mxgraph="${escapeHTML(json)}"></div>
        </div>
        `;
    };

    const install = function (hook) {
        hook.doneEach((hook) => {
            try {
                window.GraphViewer.processElements();
            } catch {}
        });
    };
});

document$.subscribe(async function() {
    function escapeHTML(html) {
      return html
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    // Sélectionne toutes les balises img dont le src contient "drawio"
    const images = document.querySelectorAll('img[src*="drawio"]');

    for (let img of images) {
      try {
        // Récupère le contenu XML du fichier drawio
        let response = await fetch(img.src);
        if (!response.ok) {
          throw new Error('Erreur de réseau');
        }
        let xml = await response.text();

        // Appelle la fonction drawioConverter
        let newHtml = window.drawioConverter(xml, new Date().getTime());

        // Crée un élément temporaire pour insérer le nouveau HTML
        let tempDiv = document.createElement('div');
        tempDiv.innerHTML = newHtml;

        // Remplace l'image par le nouveau contenu
        img.parentNode.replaceChild(tempDiv.firstElementChild, img);
      } catch (error) {
        console.error('Erreur lors du traitement de', img.src, error);
      }
    }

    await window.GraphViewer.processElements();

    // Fonction pour convertir rgb(r, g, b) en hex
    function rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }

    // Fonction pour convertir les couleurs en thème
    function convertColors(el, attr) {
        // Remplacer rgb(r, g, b) par la couleur hexadécimale
        let color = el.getAttribute(attr).replace(/rgb\((\d+), (\d+), (\d+)\)/gi, function (match, r, g, b) {
            return rgbToHex(parseInt(r), parseInt(g), parseInt(b));
        });

        // Remplacer #<hex> par var(--mxgraph-color-<hex>)
        color = color.replace(/#([0-9a-f]{6})/gi, function (match, hex) {
            return `var(--mxgraph-color-${hex})`;
        });

        el.setAttribute(attr, color);
    }

    // Fonction pour convertir les couleurs dans les styles inline
    function convertInlineStyles(el) {
        // Remplacer rgb(r, g, b) par la couleur hexadécimale dans le style
        let style = el.getAttribute("style").replace(/rgb\((\d+), (\d+), (\d+)\)/gi, function (match, r, g, b) {
            return rgbToHex(parseInt(r), parseInt(g), parseInt(b));
        });

        // Remplacer #<hex> par var(--mxgraph-color-<hex>) dans le style
        style = style.replace(/#([0-9a-f]{6})/gi, function (match, hex) {
            return `var(--mxgraph-color-${hex})`;
        });

        el.setAttribute("style", style);
    }

    // Itérer sur tous les SVG dans les div.mxgraph
    document.querySelectorAll("div.mxgraph svg").forEach(function (svg) {
        // Traiter tous les éléments avec l'attribut stroke
        svg.querySelectorAll("[stroke]").forEach(function (el) {
            convertColors(el, "stroke");
        });

        // Traiter tous les éléments avec l'attribut fill
        svg.querySelectorAll("[fill]").forEach(function (el) {
            convertColors(el, "fill");
        });
    });

    // Itérer sur tous les divs pour traiter les styles inline
    document.querySelectorAll("div[style]").forEach(function (div) {
        convertInlineStyles(div);
    });



});