# Collection de figures

Collection de figure au format Microsoft Visio, exploitable en format SVG.

## Pourquoi ce référentiel ?

Nombreux sont ceux qui n'ont pas accès à [Microsoft Visio](https://products.office.com/en-ww/visio/flowchart-software), les figures en format `.vsdx` ne sont par conséquent pas exploitables. Ce référentiel est une interface entre le format `.vsdx`et le format vectroriel `.svg`.

Les référentiels qui font référence à ces figures peuvent l'utiliser en [sous-module](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

## Comment l'utiliser ?

La commande `make` s'occupe de générer les version `.svg` à condition que l'utilisateur soit sous Windows et que Microsoft Visio soit installé.
`make publish` met à jour la branche `dist` avec les nouvelles figures.

```bash
$ make
$ make publish
```

Depuis un autre référentiel il suffit d'utiliser un sous-module:

```bash
git submodule add -b dist https://github.com/heig-vd-tin/figures.git
```