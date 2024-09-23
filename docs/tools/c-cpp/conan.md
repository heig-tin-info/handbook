# Conan

Conan est un gestionnaire de paquets C/C++ multiplateforme. Il permet de gérer les dépendances de vos projets C/C++ de manière simple et efficace. Il est multiplateforme, open-source et supporte de nombreux gestionnaires de build (CMake, Visual Studio, Meson, etc.).

Il est souvent utilisé conjointement avec Meson, un autre outil de build C/C++ moderne.

Conan est développé avec Python et est disponible sur [PyPI](https://pypi.org/project/conan/). Pour l'installer, vous pouvez utiliser `pip` :

```bash
pipx install conan
```

Il utilise un fichier de configuration `conanfile.txt` ou `conanfile.py` pour déclarer les dépendances de votre projet. Voici un exemple de fichier `conanfile.txt` :

```plaintext
[requires]
poco/1.10.1
sdl2/2.0.10

[generators]
cmake
```

Alternativement vous pouvez ajouter une dépendance à un projet existant avec la commande `conan install` :

```bash
conan install conan install Poco/1.13.3@pocoproject/stable --build missing
```