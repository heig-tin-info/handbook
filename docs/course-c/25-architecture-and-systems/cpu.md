# CPU

## Avant 1970

- **1945 :** **Architecture de Von Neumann** – Modèle théorique de base des ordinateurs modernes.
- **1954 :** **Transistors** – Remplacement des tubes à vide dans les processeurs (IBM 704).
- **1964 :** **Architecture CISC (Complex Instruction Set Computing)** – Premier processeur CISC avec l'IBM System/360.
- **1965 :** **Processeur 16-bit** – Introduction des premières architectures 16-bit (PDP-11, IBM System/360).
- **1968 :** **Premier microprocesseur** (Intel 4004) – Microprocesseur 4-bit, basé sur la technologie MOS (Metal-Oxide Semiconductor).

## Années 1970

- **1970 :** **Mémoire cache** (IBM System/360 Model 85) – Premier usage de la mémoire cache pour réduire les temps d'accès.
- **1972 :** **Introduction du FPU** (Floating Point Unit) avec les processeurs **Intel 8008** et **8080** pour supporter les opérations en virgule flottante.
- **1974 :** **Processeur 8-bit** – Intel 8080 introduit les processeurs 8-bit.
- **1978 :** **Intel 8086** – Premier processeur 16-bit et introduction de la segmentation pour adresser la mémoire.

## Années 1980

- **1980 :** **Cache de niveau L1** – Apparition de la première forme de cache de niveau L1 dans les processeurs (IBM System/370).
- **1982 :** **Mode protégé et segmentation** (Intel 80286) – Amélioration de la gestion mémoire avec des niveaux de privilèges.
- **1985 :** **32-bit** et **mémoire virtuelle** (Intel 80386) – Extension de l'architecture x86 vers un adressage 32-bit.
- **1986 :** **Instruction pipelining** – Utilisation de pipeline avec des étapes plus nombreuses pour augmenter le parallélisme (Intel 80386).
- **1989 :** **Cache de niveau L2** – Les premiers systèmes commencent à adopter des caches de niveau L2 (ajouté en externe au processeur).

## Années 1990

- **1991 :** **Pipeline 5 étapes** – Introduit avec l'Intel 80486 pour améliorer les performances du traitement parallèle.
- **1993 :** **Coprocesseur mathématique intégré** (Intel Pentium) – Le FPU est directement intégré dans le CPU.
- **1995 :** **Prédiction d'embranchement** – Optimisation du flux d'instructions (Intel Pentium Pro).
- **1995 :** **Architecture superscalaire** – Le Pentium Pro peut exécuter plusieurs instructions par cycle.
- **1996 :** **Cache L2 sur la puce** – Cache L2 intégré directement sur le processeur.
- **1997 :** **Technologie MMX** – Extension multimédia pour accélérer les calculs graphiques (Intel Pentium MMX).
- **1998 :** **SSE (Streaming SIMD Extensions)** – Amélioration des performances pour les opérations vectorielles (Intel Pentium III).

## Années 2000

- **2000 :** **Bus à 64-bit externe** (Intel Pentium 4) – Bus externe permettant de gérer plus de mémoire.
- **2000 :** **Architecture Netburst** (Pentium 4) – Augmentation des pipelines jusqu'à 20 étapes pour viser de hautes fréquences.
- **2001 :** **SSE2 (Streaming SIMD Extensions 2)** – Instructions SIMD améliorées pour manipuler les données en virgule flottante (Intel Pentium 4).
- **2004 :** **SSE3** – Troisième extension SIMD (Intel Prescott).
- **2004 :** **Cache L3** – Premier cache de niveau 3 utilisé dans les processeurs Itanium 2 et Xeon.
- **2004 :** **Technologie 64-bit x86-64** (AMD Opteron et Intel Xeon EM64T) – Introduction du support 64-bit avec AMD, suivi par Intel.
- **2006 :** **Processeurs multi-cœurs** – Premier processeur double cœur avec Intel Core Duo.
- **2006 :** **Hyper-threading** – Technologie Intel permettant à un cœur physique de gérer deux threads en simultané.
- **2008 :** **Turbo Boost** – Fréquence d'horloge dynamique pour augmenter temporairement la performance (Intel Core i7).
- **2008 :** **Smart Cache** – Partage dynamique du cache entre les cœurs pour améliorer l'efficacité.

## Années 2010

- **2010 :** **QuickPath Interconnect (QPI)** – Remplacement du bus front-side par une technologie d'interconnexion point à point (Intel Nehalem).
- **2010 :** **Intel Quick Sync Video** – Accélération matérielle de l'encodage et du décodage vidéo (Intel Sandy Bridge).
- **2011 :** **AVX (Advanced Vector Extensions)** – Introduction des instructions AVX pour améliorer les performances dans les calculs scientifiques (Intel Sandy Bridge).
- **2013 :** **AVX2** – Extension des instructions AVX avec des performances encore améliorées (Intel Haswell).
- **2014 :** **Mode de réduction de puissance (Intel Skylake)** – Introduction de modes d'économie d'énergie sophistiqués (C-states, P-states).
- **2017 :** **AVX-512** – Instructions vectorielles 512-bit pour des opérations massivement parallèles (Intel Skylake-X).
- **2019 :** **Intel Deep Learning Boost** – Instructions pour accélérer l'inférence en machine learning (Intel Cascade Lake).

## Années 2020

- **2021 :** **Intel Hybrid Technology** (Alder Lake) – Mélange de cœurs performants et efficaces dans une architecture hybride (P-cores et E-cores).
- **2021 :** **Support des instructions 128-bit et au-delà** avec l'évolution des instructions SIMD et AVX-512.
- **2021 :** **Photolithographie en EUV** (Extreme Ultraviolet Lithography) – Avancée majeure dans le processus de fabrication des puces, utilisée pour créer des transistors toujours plus petits (par exemple les nœuds de 5 nm et 7 nm).

## Fonctionnalités spécifiques supplémentaires

- **Cache L1, L2, L3 :** Le cache L1 est apparu dans les années 1980, le cache L2 est apparu dans les années 1990 (d'abord externe, puis intégré), et le cache L3 est devenu standard dans les années 2000.
- **Précision simple, double, étendue (Extended Precision) :** Apparue avec les coprocesseurs mathématiques (x87 FPU), et les extensions SSE ont introduit la gestion des calculs en virgule flottante sur des registres 128-bit.
- **Virtualisation (Intel VT-x, AMD-V) :** Support pour l'exécution de machines virtuelles directement via le matériel, introduit dans les années 2000.
- **Technologies de réduction de consommation d'énergie (Intel SpeedStep, AMD Cool'n'Quiet)** : Ces technologies permettent au processeur de diminuer sa consommation en adaptant dynamiquement sa fréquence et son voltage.
- **Pipelines avec plusieurs niveaux (Netburst)** : La microarchitecture Netburst d'Intel Pentium 4 introduit des pipelines de plus de 30 niveaux pour viser des fréquences élevées, bien que cela ait compromis les performances générales.
- **Micro-opérations et scheduling** : Les architectures modernes décomposent les instructions complexes en micro-opérations (Intel Core) pour mieux les planifier via un scheduler intégré.

Cette liste devrait fournir une vision beaucoup plus complète et détaillée de l'évolution des processeurs et des technologies qui les accompagnent depuis leurs débuts jusqu'à aujourd'hui.
