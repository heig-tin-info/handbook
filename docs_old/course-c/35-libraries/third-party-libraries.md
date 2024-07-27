## Autres bibliothèques

- GNU C Library ([glibc](https://www.gnu.org/software/libc/))
  - C11
  - POSIX.1-2008
  - IEEE 754-2008

### POSIX C Library

Le standard C ne définit que le minimum vital et qui est valable sur toutes les architectures pour autant que la *toolchain* soit compatible **C99**. Il existe néanmoins toute une collection d'autres fonctions manquantes :

- La communication entre les processus (deux programmes qui souhaitent communiquer entre eux)

  - `<sys/socket.h>`
  - `<sharedmemory.h>`

- La communication sur le réseau e.g. internet

  - `<sys/socket.h>`
  - `<arpa/inet.h>`
  - `<net/if.h>`

- Les tâches

  - `<thread.h>`

- Les traductions de chaînes p.ex. français vers anglais

  - `<iconv.h>`

- Les fonctions avancées de recherche de texte

  - `<regex.h>`

- Le log centralisé des messages (d'erreur)

  - `<syslog.h>`

Toutes ces bibliothèques additionnelles ne sont pas nécessairement disponibles sur votre ordinateur ou pour le système cible, surtout si vous convoitez une application *bare-metal*. Elles dépendent grandement du système d'exploitation utilisé, mais une tentative de normalisation existe et se nomme [POSIX](https://en.wikipedia.org/wiki/POSIX) (ISO/IEC 9945).

Généralement la vaste majorité des distributions Linux et Unix sont compatibles avec le standard POSIX et les bibliothèques ci-dessus seront disponibles à moins que vous ne visiez une architecture différente de celle sur laquelle s'exécute votre compilateur.

Le support POSIX sous Windows (Win32) n'est malheureusement que partiel et il n'est pas standardisé.

Un point d'entrée de l'API POSIX est la bibliothèque `<unistd.h>`.

### GNU GLIBC

La bibliothèque portable [GNULIB](https://www.gnu.org/software/gnulib/) est la bibliothèque standard référencée sous Linux par `libc6`.

### Windows C library

La bibliothèque Windows [Windoes API](https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list) offre une interface au système de fichier, au registre Windows, aux imprimantes, à l'interface de fenêtrage, à la console et au réseau.

L'accès à cet API est offert par un unique point d'entrée [windows.h](https://en.wikipedia.org/wiki/Windows.h) qui regroupe certains en-têtes standards (`<stdarg.h>`, `<string.h>`, ...), mais pas tous (😔) ainsi que les en-têtes spécifiques à Windows tels que :

`<winreg.h>`

: Pour l'accès au registre Windows

`<wincon.h>`

: L'accès à la console

La documentation est disponible en ligne depuis le site de Microsoft, mais n'est malheureusement pas complète et souvent il est difficile de savoir sur quel site trouver la bonne version de la bonne documentation. Par exemple, il n'y a aucune documentation claire de `LSTATUS` pour la fonction [RegCreateKeyExW](https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regcreatekeyexw) permettant de créer une entrée dans la base de registre.

Un bon point d'entrée est le [Microsoft API and reference catalog](https://msdn.microsoft.com/library).

Quelques observations :

- Officiellement Windows est compatible avec C89 (ANSI C) (c.f. [C Language Reference](https://docs.microsoft.com/en-us/cpp/c-language/c-language-reference?view=vs-2019))
- L'API Windows n'est pas officiellement compatible avec C99, mais elle s'en approche, il n'y pas ou peu de documents expliquant les différences.
- Microsoft n'a aucune priorité pour développer son support C, il se focalise davantage sur C++ et C#, c'est pourquoi certains éléments du langage ne sont pas ou peu documentés.
- Les [types standards Windows](https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types) différent de ceux proposés par C99. Par exemple, `LONG32` remplace `int32_t`.
