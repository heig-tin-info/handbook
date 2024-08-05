// Once dom is ready
document.addEventListener("DOMContentLoaded", function () {
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

    /**
     * See options in
     * GraphViewer.prototype.init = function(container, xmlNode, graphConfig)
     */
    window.drawioConverter = function (xml, idx = new Date().getTime()) {

        let parser = new DOMParser();
        let xmlDoc = parser.parseFromString(xml, "text/xml");
        let mxfile = xmlDoc.getElementsByTagName("mxfile")[0];
        let mxGraphModel = mxfile.getElementsByTagName("mxGraphModel")[0];
        let canvasWidth = mxGraphModel.getAttribute("pageWidth");
        let canvasHeight = mxGraphModel.getAttribute("pageHeight");

        let mxGraphData = {
            // editable: false,
            // autoCrop: false,
            // autoFit: false

            'auto-origin': false,
            'auto-crop': false,
            'auto-fit': false,
            'zoom-enabled': false,
            zoomEnabled: false,
            // highlight: "#0000ff",
            // toolbar: null,
            // edit: null,
            //resize: true,
            // lightbox: "open",
            // // "check-visible-state": false,
            // autoFit: false,
            // autoCrop: false,
            // darkMode: true,
            // allowZoomIn: true,
            // move: false,
            canvasWidth,
            canvasHeight,
            xml,
        };
        const json = JSON.stringify(mxGraphData);

        return `<div class="drawio-viewer-index-${idx}">
          <div class="mxgraph" style="max-width: 100%; border: 1px solid transparent" data-mxgraph="${escapeHTML(json)}"></div>
        </div>
        `;
    };

    GraphViewer.processElements = function(classname)
    {
        mxUtils.forEach(GraphViewer.getElementsByClassName(classname || 'mxgraph'), function(div)
        {
            try
            {
                div.innerText = '';
                GraphViewer.createViewerForElement(div, (element) => {
                    let ratio = element.graph.container.offsetWidth / element.graphConfig.canvasWidth;
                    // element.graph.zoomTo(ratio);
                    // Do not work as expected...
                });
            }
            catch (e)
            {
                div.innerText = e.message;

                if (window.console != null)
                {
                    console.error(e);
                }
            }
        });
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


        let newHtml = window.drawioConverter(xml, new Date().getTime());

        let tempDiv = document.createElement('div');
        tempDiv.innerHTML = newHtml;

        let drawioElement = tempDiv.firstElementChild;
        // drawioElement.style.width = 'auto';
        // drawioElement.style.height = `${ratioHeight}%`;

        // Remplace l'image par le nouveau contenu
        img.parentNode.replaceChild(drawioElement, img);
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