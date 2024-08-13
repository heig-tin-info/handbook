# Handbook

![.github/workflows/ci.yml](https://github.com/heig-tin-info/handbook/workflows/.github/workflows/ci.yml/badge.svg?branch=master)

![version](https://img.shields.io/github/v/release/heig-tin-info/handbook)
![downloads](https://img.shields.io/github/downloads/heig-tin-info/handbook/latest/total)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/heig-tin-info/handbook)

Cours d'informatique pour les étudiants de la HEIG-VD, département TIN.

Ce cours couvre les bases de l'informatique, de l'architecture des ordinateurs à la programmation en C, il est prévu de l'étendre à C++ et Python.

La version web est disponible sur cette [page](https://heig-tin-info.github.io/handbook/).

## Contribution

Une seule source de données est utilisée pour générer le site web et le livre en version PDF. Aussi, il est important de respecter les règles suivantes :

Éviter d'utiliser "en-dessus" et "en-dessous" pour les figures, les tableaux, les équations, etc. Utilisez les références croisées.

Les réfrences croisées sont ajoutée en lieu et place du texte sur la version web. Pour la version PDF, le texte suit de `(c.f. figure 2.1)`.

Les acronymes sont indiqués la première fois en entier suivi de l'acronyme entre parenthèses. Par exemple, "Système d'exploitation (OS)". puis l'acronyme est utilisé par la suite.

## Développement

La version utilisée est Ubuntu 24.04 LTS. Commencez par installer les paquets suivants :

```bash
sudo apt install -y fonts-noto
sudo apt install -y texlive-full
sudo apt install -y pipx
sudo fc-cache -fv
```

L'image Docker `Dockerfile` permet alternativement de compiler le livre en PDF.

Initialisez le dépôt  avec :

```bash
git clone https://github.com/heig-tin-info/handbook.git
cd handbook
pipx install poetry
```

Puis pour lancer le développement :

```bash
poetry install
poetry run mkdocs serve
```

## References

- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions)
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid](https://mermaid.js.org/)
- [Draw.io](https://www.draw.io/)