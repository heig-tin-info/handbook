document$.subscribe(async function (el) {
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

    config = {
        'default': {
            '/course-c/': 'red',
            '/course-cpp/': 'cyan',
            '/course-python/': 'green',
            '/environment/': 'gray',
            'default': 'red'
        },
        'slate': {
            '/course-c/': 'black',
            '/course-cpp/': 'cyan',
            '/course-python/': 'green',
            '/environment/': 'gray',
            'default': 'black'
        }
    }

    let scheme = document.querySelector('body').getAttribute('data-md-color-scheme');
    for (let key in config[scheme]) {
        if (href.includes(key)) {
            color = config[scheme][key];
            document.querySelector('body').setAttribute('data-md-color-primary', color);
        }
    }
});