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

    GraphViewer.processElements = function (classname) {
        mxUtils.forEach(GraphViewer.getElementsByClassName(classname || 'mxgraph'), function (div) {
            try {
                div.innerText = '';
                GraphViewer.createViewerForElement(div, (element) => {
                    let ratio = element.graph.container.offsetWidth / element.graphConfig.canvasWidth;
                    // element.graph.zoomTo(ratio);
                    // Do not work as expected...
                });
            }
            catch (e) {
                div.innerText = e.message;

                if (window.console != null) {
                    console.error(e);
                }
            }
        });
    };

    const install = function (hook) {
        hook.doneEach((hook) => {
            try {
                window.GraphViewer.processElements();
            } catch { }
        });
    };
});

document$.subscribe(async function () {
    function escapeHTML(html) {
        return html
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    const images = document.querySelectorAll('img[src*="drawio"]');

    for (let img of images) {
        try {
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

            img.parentNode.replaceChild(drawioElement, img);
        } catch (error) {
            console.error('Erreur lors du traitement de', img.src, error);
        }
    }

    await window.GraphViewer.processElements();

    function rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }

    function convertColors(el, attr) {
        let color = el.getAttribute(attr).replace(/rgb\((\d+), (\d+), (\d+)\)/gi, function (match, r, g, b) {
            return rgbToHex(parseInt(r), parseInt(g), parseInt(b));
        });

        color = color.replace(/#([0-9a-f]{6})/gi, function (match, hex) {
            return `var(--mxgraph-color-${hex})`;
        });

        el.setAttribute(attr, color);
    }

    function convertInlineStyles(el) {
        let style = el.getAttribute("style").replace(/rgb\((\d+), (\d+), (\d+)\)/gi, function (match, r, g, b) {
            return rgbToHex(parseInt(r), parseInt(g), parseInt(b));
        });

        style = style.replace(/#([0-9a-f]{6})/gi, function (match, hex) {
            return `var(--mxgraph-color-${hex})`;
        });

        el.setAttribute("style", style);
    }

    document.querySelectorAll("div.mxgraph svg").forEach(function (svg) {
        svg.querySelectorAll("[stroke]").forEach(function (el) {
            convertColors(el, "stroke");
        });

        svg.querySelectorAll("[fill]").forEach(function (el) {
            convertColors(el, "fill");
        });

        svg.querySelectorAll("[style]").forEach(function (el) {
            convertInlineStyles(el);
        })
    });
});