# Colophon

L'écriture du présent ouvrage a été réalisée en utilisant [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText), un langage couramment utilisé pour l'écriture de documentation et largement utilisé dans la communauté Python. Ce langage s'intègre dans le projet Docutils qui s'inspire d'outils tels que Javadoc. La compilation des sources est réalisée sous Sphinx, un paquet Python permettant de générer une documentation HTML ainsi qu'un ouvrage PDF via LaTeX.

L'ensemble des sources est compilé dans un environnement isolé sous Docker en utilisant un service donnant accès à la suite logicielle texlive.

Les sources sont hébergées sous GitHub. Un système d'intégration continue permet de vérifier à chaque changement que l'ensemble compile sans erreur.
