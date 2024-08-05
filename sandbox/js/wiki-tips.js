/**
 * Inspired from sphinx-tippy
 */
document$.subscribe(function() {
    const wikiLinks = document.querySelectorAll('a[href*="wikipedia.org"]');
    wikiLinks.forEach(link => {
        if (link.querySelector('abbr')) {
            return;
        }

        function shouldDisplayPopupAbove(rect, popupHeight) {
            const spaceBelow = window.innerHeight - (rect.bottom + window.scrollY);
            return spaceBelow < popupHeight;
        }

        link.addEventListener('mouseenter', async (event) => {
            const url = link.getAttribute('href');
            const { language, title } = extractLanguageAndTitleFromUrl(url);
            const apiUrl = `https://${language}.wikipedia.org/api/rest_v1/page/summary/${title}`;
            const popup = createPopup();
            document.body.appendChild(popup);

            try {
                const response = await fetch(apiUrl);
                if (response.ok) {
                    const data = await response.json();
                    extractHTML = `<div class="wiki-popup-container"><h2>${data.title}</h2><p>${data.extract}</p></div>`;
                    if ('thumbnail' in data) {
                        extractHTML = `<img src="${data.thumbnail.source}" alt="Wikipedia thumbnail" />${extractHTML}`;
                    }
                    popup.innerHTML = extractHTML;
                } else {
                    popup.innerHTML = `<p>Could not retrieve summary</p>`;
                }
            } catch (error) {
                popup.innerHTML = `<p>Error fetching summary</p>`;
            }

            const rect = link.getBoundingClientRect();
            const popupHeight = popup.offsetHeight;
            // console.log(rect, popupHeight);

            // if (shouldDisplayPopupAbove(rect, popupHeight)) {
            //     popup.style.top = `${rect.top + window.scrollY - popupHeight}px`;
            // } else {
            //     popup.style.top = `${rect.bottom + window.scrollY}px`;
            // }

            popup.style.top = `${rect.bottom + window.scrollY}px`;
            popup.style.left = `${rect.left + window.scrollX}px`;
            popup.style.display = 'block';
        });

        link.addEventListener('mouseleave', () => {
            const popup = document.querySelector('.wiki-popup');
            if (popup) {
                popup.remove();
            }
        });
    });

    function extractLanguageAndTitleFromUrl(url) {
        const parts = url.split('/');
        const language = parts[2].split('.')[0];
        const title = parts[parts.length - 1];
        return { language, title };
    }

    function createPopup() {
        const popup = document.createElement('div');
        popup.className = 'wiki-popup';
        return popup;
    }
});