# ABI

Une *Application Binary Interface* (ABI) est une interface entre deux modules de code binaire, souvent un programme et une bibliothèque, au niveau de l'assembleur. L'ABI définit comment les fonctions, les données et les structures sont organisées et accessibles dans le code binaire. Elle spécifie des conventions pour les appels de fonctions, la gestion de la mémoire, le format des données, etc.

Nous avons vu par exemple que l'appel d'une fonction en C peut être réalisé en utilisant la pile. Mais comment est-ce que cela fonctionne derrière les coulisses ? L'ABI définit comment les arguments sont passés à une fonction, comment les valeurs de retour sont retournées, comment les variables locales sont stockées, etc. Elle définit quels sont les registres qui doivent être sauvegardés avant un appel de fonction et ceux qui sont utilisés pour passer des arguments. En somme, c'est une convention qui permet à des modules de code binaire de communiquer entre eux.

En outre, sur un système d'exploitation, un programme communique avec le noyau du système d'exploitation en utilisant des appels système. L'ABI définit comment ces appels système sont réalisés. Par exemple, sur Linux, les appels système sont réalisés en utilisant le registre `eax` pour passer le numéro de l'appel système et les arguments sont passés dans les registres `ebx`, `ecx`, `edx`, `esi`, `edi`, `ebp`. Le résultat de l'appel système est retourné dans le registre `eax`.

L'ABI est donc spécifique à une architecture matérielle et à un système d'exploitation. Par exemple, l'ABI pour les programmes Linux sur une architecture x86-64 est différente de celle pour les programmes Windows sur la même architecture. Cela signifie que les programmes compilés pour une architecture et un système d'exploitation ne peuvent pas être exécutés sur une autre architecture ou un autre système d'exploitation car ces conventions ne sont pas respectées. C'est pourquoi il est important de connaître l'ABI de la plateforme cible lors de la compilation d'un programme.

## ELF

Le format de fichier exécutable et de liaison (Executable and Linkable Format, ELF) est un format de fichier binaire standard pour les fichiers exécutables, les fichiers objet, les bibliothèques partagées et les fichiers de base de données de débogage. Il est utilisé sur la plupart des systèmes d'exploitation Unix et Unix-like, y compris Linux, Solaris, FreeBSD, etc.

Lorsque vous compilez un programme avec GCC, le compilateur génère un fichier binaire au format ELF. Vous pouvez en avoir la preuve avec la commande `file` sur un programme compilé avec gcc sous Linux:

```bash
$ file a.out
a.out: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
BuildID[sha1]=2066ecb2b4fed0b91adbcc63d0e7c13a8bea14a8,
for GNU/Linux 3.2.0, not stripped
```

On peut également consulter le contenu d'un fichier ELF avec la commande `readelf`:

```bash
$ readelf -h a.out
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Position-Independent Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x1060
  Start of program headers:          64 (bytes into file)
  Start of section headers:          13968 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         13
  Size of section headers:           64 (bytes)
  Number of section headers:         31
  Section header string table index: 30
```

Ce que l'on constate c'est que le format ELF est composé de plusieurs parties, notamment un en-tête ELF, des en-têtes de programme, des en-têtes de section, des tables de symboles, des réimplantations dynamiques, etc. Chaque partie a un rôle spécifique dans la gestion des fichiers binaires et des bibliothèques partagées. Dans cet exemple on observe que cet `elf` est pour l'ABI UNIX - System V.

Le **System V** est une version d'Unix développée par AT&T et commercialisée par Sun Microsystems. Elle a été l'une des premières versions d'Unix à être largement utilisée dans l'industrie. Le format ELF est donc un standard pour les systèmes Unix et Unix-like qui suit les conventions de l'ABI System V.

Sous Windows, le format de fichier exécutable est le format Portable Executable (PE) qui est différent du format ELF. Cela signifie que les programmes compilés pour Windows ne peuvent pas être exécutés sur un système Unix et vice versa sans une couche de compatibilité spécifique.

Sous macOS, le format de fichier exécutable est le format Mach-O (Mach Object) qui est également différent du format ELF. Cela signifie que les programmes compilés pour macOS ne peuvent pas être exécutés sur un système Unix ou Windows sans une couche de compatibilité spécifique.

## EABI

L'ABI embarqué (Embedded ABI, EABI) est une version de l'ABI conçue pour les systèmes embarqués, c'est-à-dire des systèmes informatiques spécialisés qui sont intégrés dans des appareils électroniques. Les systèmes embarqués sont souvent limités en termes de ressources matérielles et logicielles, ce qui nécessite des conventions spécifiques pour les appels de fonctions, la gestion de la mémoire, le format des données, etc.