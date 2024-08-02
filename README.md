# Handbook

Cours d'informatique pour les étudiants de la HEIG-VD, département TIN.

Ce cours couvre les bases de l'informatique, de l'architecture des ordinateurs à la programmation en C, il est prévu de l'étendre à C++ et Python.

La version web est disponible sur cette [page](https://heig-tin-info.github.io/handbook/).

## Technologies


## Développement

La version utilisée est Ubuntu 24.04 LTS. Commencez par installer les paquets suivants :

```bash
sudo apt install -y fonts-symbola fonts-noto fonts-firacode
sudo apt install -y texlive-full
sudo apt install -y pipx
sudo fc-cache -fv
```

Initialisez le dépôt avec :

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