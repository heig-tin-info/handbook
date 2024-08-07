document$.subscribe(async function(el) {
    const ul = el.querySelector('.md-tabs__list');
    if (!ul) {
        return;
    }
    const li = ul.querySelector('li.md-tabs__item--active');
    if (!li) {
        return;
    }
    const a = li.querySelector('a');
    if (!a) {
        return;
    }
    const href = a.getAttribute('href');

    if (href.includes('/course-c/')) {
        color = 'red'
    }
    else if (href.includes('/course-cpp/')) {
        color = 'cyan'
    }
    else if (href.includes('/course-python/')) {
        color = 'green'
    }
    else if (href.includes('/environment/')) {
        color = 'gray'
    }
    else {
        color = 'red'
    }
    document.querySelector('body').setAttribute('data-md-color-primary', color);
});