# Gestion des dépendances

Les dépendances sont des bibliothèques ou des modules qui sont utilisés dans un projet. Elles peuvent être des bibliothèques tierces, des modules internes ou des fichiers de configuration. La gestion des dépendances est un aspect important du développement logiciel, car elle permet de gérer les dépendances entre les différents composants d'un projet.

Lorsque vous travaillez sur un projet en C ou d'ailleurs dans un autre langage, vous aurez souvent besoin d'utiliser des bibliothèques tierces pour étendre les fonctionnalités de votre programme et ne nous le cachons pas c'est toujours un enfer de gérer les dépendances. Nous allons voir quelques outils qui peuvent vous aider à gérer les dépendances de votre projet.

## Gestionnaire de dépendances

Imagions le projet suivant. C'est un fichier unique qui utilise les bibliothèques Curl, SQLite et PCRE. Voici le code source :

```c
#include <stdio.h>
#include <curl/curl.h>
#include <sqlite3.h>
#include <pcre.h>

int main() {
    CURL *curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "http://example.com");
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }

    sqlite3 *db;
    if (sqlite3_open(":memory:", &db) == SQLITE_OK) {
        printf("SQLite database opened successfully.\n");
        sqlite3_close(db);
    }

    const char *error;
    int erroffset;
    pcre *re = pcre_compile("hello", 0, &error, &erroffset, NULL);
    if (re) {
        printf("PCRE compiled successfully.\n");
        pcre_free(re);
    }
}
```

Pour gérer les dépendances de ce projet il est possible d'utiliser différents outils tels que CMake, Meson, Conan, etc.

### Meson

[Meson](https://mesonbuild.com/) est un système de build open-source conçu pour être rapide, facile à utiliser et extensible. Il est écrit en Python et est compatible avec de nombreux langages de programmation, y compris C, C++, Rust, Java, etc. Meson est particulièrement utile pour les projets C/C++ car il prend en charge la compilation croisée, la génération de fichiers de configuration et la gestion des dépendances. Il se base sur [Ninja](https://ninja-build.org/) pour la compilation. Il s'agit d'une alternative à Make plus moderne et plus rapide.

Commencez par installer Meson sur votre système :

```bash
sudo apt-get install meson ninja-build \
     libcurl4-openssl-dev libsqlite3-dev libpcre3-dev
```

Puis créer un fichier `meson.build` pour configurer le projet :

```text title="meson.build"
project('my_project', 'c', version: '0.1.0')

# Dépendances
libcurl = dependency('libcurl', version: '>=8.5')
sqlite = dependency('sqlite3', version: '>=3.1')
pcre = dependency('libpcre', version: '>=8.0')

# Sources
executable('my_project',
  sources: files('main.c'),
  dependencies: [libcurl, sqlite, pcre]
)
```

Enfin, configurez et compilez le projet avec Meson :

```bash
$ meson setup build
$ ninja -C build
```

Meson ne gère pas les dépendances tierces, il faut donc les installer manuellement. Dans notre cas, nous avons installé les dépendances avec `apt-get` avant de configurer le projet.

### Conan

[Conan](https://conan.io/) est un gestionnaire de dépendances C/C++ open-source, décentralisé et multiplateforme. Il permet de gérer les dépendances de vos projets C/C++ en automatisant le processus de téléchargement, de compilation et d'installation des bibliothèques tierces. Il est particulièrement utile sous Windows où la gestion des dépendances est souvent plus complexe.

Conan est écrit en Python et est compatible avec de nombreux systèmes de build, tels que CMake, Make, Visual Studio, Xcode, etc. Pour l'installer sur votre système utilisez la commande suivante :

```bash
pip install conan
```

Imaginons que nous voulons créer un projet qui dépend des bibliothèques SQlite, Curl et PCRE. Le projet aura la structure suivante :

```
project/
├── CMakeLists.txt
├── conanfile.txt
├── main.c
└── build/  (créé après la configuration)
```

Le fichier `conanfile.txt` contiendra les dépendances du projet :

```plaintext
[requires]
libcurl/8.9.1
sqlite3/3.43.2
pcre/8.45

[generators]
CMakeToolchain
CMakeDeps

[options]
libcurl/*:shared=True
sqlite3/*:shared=True
pcre/*:shared=True
```

Enfin le fichier `CMakeLists.txt` contiendra les instructions pour inclure les bibliothèques dans le projet :

```cmake
cmake_minimum_required(VERSION 3.15)
project(MyProject C)

include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake)

add_executable(my_project main.c)

find_package(CURL REQUIRED)
find_package(sqlite3 REQUIRED)
find_package(PCRE REQUIRED)

target_link_libraries(my_project CURL::libcurl sqlite3::sqlite3 PCRE::PCRE)
```

Commencez par compiler les dépendances avec Conan :

```
conan profile detect --force
detect_api: Found cc=gcc- 13.2.0
detect_api: gcc>=5, using the major as version
detect_api: gcc C++ standard library: libstdc++11

Detected profile:
[settings]
arch=x86_64
build_type=Release
compiler=gcc
compiler.cppstd=gnu17
compiler.libcxx=libstdc++11
compiler.version=13
os=Linux
```

```bash
$ conan install . --output-folder=build --build=missing
...
======== Computing dependency graph ========
sqlite3/3.43.2: Not found in local cache, looking in remotes...
sqlite3/3.43.2: Checking remote: conancenter
sqlite3/3.43.2: Downloaded recipe revision c850734dc9724ee9aa9e5d95efd0b100
pcre/8.45: Not found in local cache, looking in remotes...
pcre/8.45: Checking remote: conancenter
pcre/8.45: Downloaded recipe revision 64cdfd792761c32817cd31d7967c3709
bzip2/1.0.8: Not found in local cache, looking in remotes...
bzip2/1.0.8: Checking remote: conancenter
bzip2/1.0.8: Downloaded recipe revision 457c272f7da34cb9c67456dd217d36c4
...
conanfile.txt: Generating aggregated env files
conanfile.txt: Generated aggregated env files: ['conanbuild.sh', 'conanrun.sh']
Install finished successfully
```

Ensuite, configurez le projet avec CMake :

```bash
$ cmake -B build
```
