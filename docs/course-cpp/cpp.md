---
epigraph:
    text: "C vous permet de vous tirer une balle dans le pied facilement ; C++ rend cela plus difficile, mais quand vous y arrivez, ça vous arrache toute la jambe."
    source: Bjarne Stroustrup
---
# C++

## Introduction

Dans le vaste univers des langages de programmation, il est des étoiles qui brillent d’un éclat singulier, non par leur simplicité, mais par la puissance et la profondeur qu’elles confèrent à ceux qui osent s’y aventurer. C++ est sans doute l’une de ces constellations. Langage aux multiples facettes, oscillant entre l’héritage brut de C et les abstractions sophistiquées de la programmation orientée objet, C++ trouve son origine dans les années 1980, sous la plume inspirée de **Bjarne Stroustrup**, un informaticien danois dont l’ambition était aussi pragmatique que visionnaire.

Dans les années 1970 et 1980, les langages de programmation n’étaient pas encore aussi variés et spécialisés qu’aujourd’hui. **C**, un langage impératif et structuré, dominait le paysage, notamment dans les domaines des systèmes d’exploitation et du développement de logiciels à hautes performances. Toutefois, malgré sa rapidité et son efficacité, **C** possédait des limitations flagrantes, en particulier dans la gestion des concepts abstraits et complexes propres aux grands systèmes logiciels. Stroustrup, alors chercheur aux laboratoires **Bell**, se trouvait confronté à une question existentielle : comment allier la performance brute d’un langage bas niveau, capable de manipuler le matériel avec une précision chirurgicale, à l’élégance et à la modularité d’un langage orienté objet, tel que Simula, qui était déjà prisé pour ses capacités à modéliser des systèmes complexes ?

L’idée de **C with Classes**, qui deviendra par la suite **C++**, était de conserver la robustesse de C tout en y introduisant les concepts de la programmation orientée objet (POO), un paradigme qui, à l’époque, commençait à démontrer son efficacité pour organiser le code, le rendre plus réutilisable, et gérer la complexité croissante des systèmes logiciels modernes.

![Bjarne Stroupstrup](/assets/images/bjarne-stroupstrup.png)

Le paradigme objet qui a fait sa grande entrée avec **Simula** en 1967, puis **Smalltalk** en 1972, était une révolution dans la manière de concevoir les programmes. Il permettait de regrouper les données et les fonctions qui les manipulent dans des entités cohérentes appelées **objets**, et de définir des relations entre ces objets, en termes d’héritage, de polymorphisme, et d’encapsulation. C++ allait donc s’inscrire dans cette lignée, en apportant sa propre vision de la POO, plus proche de C que de Simula, mais tout aussi puissante.

## Équilibre entre pouvoir et simplicité

Le dessein de Stroustrup n’était pas de créer un langage complètement nouveau, mais plutôt d’étendre un outil déjà existant, C, pour en faire un instrument plus flexible, plus puissant, capable de s’adapter à des applications variées, allant des systèmes d’exploitation aux simulations scientifiques. Cependant, il était clair dès le début que cet équilibre ne serait pas facile à atteindre. À la manière d’un architecte concevant une cathédrale où chaque voûte porte la promesse d’un effondrement potentiel, Stroustrup devait naviguer entre les contraintes de performances de bas niveau et la promesse d’une abstraction élevée.

**C++** introduisit donc des classes, l’héritage, l’encapsulation, et bientôt, des concepts comme les modèles (*templates*), qui allaient permettre d’abstraire le code tout en conservant une efficacité optimale. Toutefois, cette flexibilité et cette ambition eurent aussi leurs revers.

Toute naissance est imparfaite. Et C++, bien que prometteur, n’échappa pas aux vicissitudes de l’évolution. Parmi les premiers défis que les développeurs rencontrèrent en adoptant ce langage se trouvait ce qui allait être nommé avec un certain humour noir, le **“Most Vexing Parse”** — une des nombreuses subtilités de la syntaxe de C++ qui pouvait amener même les plus expérimentés à se gratter la tête. En raison de l’ambiguïté entre la déclaration de variables et la définition de fonctions, certaines constructions valides en apparence pouvaient se révéler incompréhensibles ou sources d’erreurs.

De même, la gestion de la mémoire, héritée de C, restait un terrain miné. Alors que C++ proposait des mécanismes comme les destructeurs pour automatiser la libération des ressources, l’absence de *garbage collector* (collecteur de déchets) natif, à l’instar de Java ou C#, signifiait que l’erreur humaine demeurait un facteur crucial dans la gestion des ressources : n'avez-vous jamais oublié un *free* après un *malloc* en C ?

Ces "erreurs de jeunesse" ne faisaient pas qu'alourdir la tâche du programmeur ; elles rappelaient aussi que **C++ n'était pas un langage de novices**. Il exigeait discipline, rigueur, et une compréhension intime de ses mécanismes internes. Il y avait une beauté dans cette complexité, un plaisir intellectuel pour ceux qui maîtrisaient ses arcanes.

Malgré ses débuts tumultueux, C++ gagna rapidement en popularité. Sa capacité à être à la fois bas niveau et abstrait en faisait l’outil privilégié pour de nombreux domaines, des moteurs de jeux vidéo aux simulations financières. Mais, comme tout langage en évolution rapide, il nécessitait un cadre rigoureux pour éviter le chaos. C’est ainsi qu’en 1998, l'ISO standardisa officiellement C++, posant les bases de ce qui deviendrait une longue lignée de versions standardisées.

Voici les principales étapes de cette évolution :

**C++98** (ISO/IEC 14882:1998)

: La première norme officielle de C++, qui formalise les ajouts du langage, notamment les templates et les exceptions.

**C++03** (ISO/IEC 14882:2003)

: Une révision mineure visant à corriger des erreurs et clarifier certaines ambiguïtés dans C++98.

**C++11** (ISO/IEC 14882:2011)

: Une révolution pour le langage, avec l’ajout des expressions lambda, des smart pointers, des threads natifs, et de nombreuses améliorations en termes de performance et de simplicité d’utilisation.

**C++14** (ISO/IEC 14882:2014)

: Une révision de C++11, qui affine certains concepts et introduit quelques nouvelles fonctionnalités mineures.

**C++17** (ISO/IEC 14882:2017)

: Un standard qui introduit des fonctionnalités plus avancées comme `std::optional`, `std::variant`, et des améliorations pour le travail avec les chaînes de caractères.

**C++20** (ISO/IEC 14882:2020)

: Une mise à jour majeure, avec des concepts, des coroutines, et des ranges, renforçant encore davantage les capacités de programmation générique et moderne de C++.

**C++23**

: Dernier en date au moment de cet écrit, qui continue d’affiner et de simplifier l’expérience des développeurs, en intégrant des fonctionnalités comme des modules et des améliorations pour la concurrence.

À travers chaque standardisation, C++ a su évoluer sans jamais renier ses principes fondateurs : performance, flexibilité et un contrôle précis des ressources.

## Un héritage à double tranchant

En conclusion, C++ n’est pas un langage pour ceux qui cherchent la facilité. Il est le produit d’une vision grandiose, où chaque ligne de code peut atteindre des sommets de performance, mais où chaque erreur peut avoir des conséquences drastiques. Ses **subtilités syntaxiques**, ses **mécanismes de mémoire** et sa **philosophie de contrôle total** sont autant de défis que de promesses pour le programmeur aguerri.

Mais c’est aussi un langage vivant, évoluant constamment avec ses utilisateurs, capable d'adapter ses structures aux paradigmes modernes tout en conservant sa puissance brute. C++, en somme, est à l’image de son créateur, Bjarne Stroustrup : une œuvre à la fois rationnelle et passionnée, où le code devient plus qu’un outil — il devient un art.
