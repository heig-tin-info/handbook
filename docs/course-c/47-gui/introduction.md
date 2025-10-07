# Introduction

## Qu'est-ce qu'une interface graphique ?

L'interface graphique, couramment désignée sous l'acronyme GUI (*Graphical User Interface*), est la couche visuelle par laquelle un utilisateur interagit avec un système informatique. Contrairement aux interfaces en ligne de commande (CLI, *Command Line Interface*), où l'utilisateur doit saisir des commandes textuelles, une GUI propose une interaction plus intuitive, fondée sur des éléments visuels tels que des fenêtres, des icônes, des menus et des boutons.

À la naissance de l'informatique, les interactions étaient principalement réservées à des spécialistes capables de comprendre et de manipuler des commandes complexes. L'avènement des interfaces graphiques, au début des années 1980, a marqué un tournant fondamental dans l'accessibilité des systèmes informatiques, ouvrant la voie à une démocratisation rapide de ces technologies.

Le Smaky, développé par le professeur Jean-Daniel Nicoud au LAMI de l'EPFL, est l'un des premiers ordinateurs grand public à proposer une interface graphique. Commercialisé dès 1978, il devient aussi le premier ordinateur personnel à intégrer une souris en standard, elle-même inspirée de celle conçue en 1962 par Douglas Engelbart. Séduit par l'idée, Nicoud la perfectionne au sein de son laboratoire. André Guignard, également à l'origine du robot [Khepera](https://en.wikipedia.org/wiki/Khepera_mobile_robot), réalise pour lui la première souris optomécanique, fabriquée par Depraz puis commercialisée par Logitech.

![Souris Depraz](/assets/images/depraz.png)

Depuis lors, les interfaces graphiques ont non seulement rendu les ordinateurs plus accessibles à un public non technique, mais elles ont également transformé l'expérience utilisateur. L'interface graphique permet de manipuler les objets numériques comme s'ils étaient des objets physiques. Cette analogie, que l'on appelle [métaphore d'interface](https://en.wikipedia.org/wiki/Interface_metaphor), est l'un des piliers de la conception des GUI. Par exemple, la corbeille, où l'on dépose les fichiers pour les supprimer, est une métaphore simple, mais efficace qui transforme un concept abstrait en une action que tout utilisateur peut comprendre.

En outre, les GUI facilitent les interactions complexes en cachant la complexité du code sous une couche de simplicité visuelle. Chaque clic sur un bouton, chaque interaction avec un menu déclenche des opérations en arrière-plan, rendant l'utilisation du système plus fluide et plus intuitive.

![Scarabé Julodimorpha bakewelli](/assets/images/beetle.png){ #beetle }

Donald Hoffman, dans son excellent TED Talk intitulé [Do we see reality as it is?](https://www.ted.com/talks/donald_hoffman_do_we_see_reality_as_it_is), aborde la question de la perception du réel. Il explique que notre cerveau ne perçoit pas la réalité telle qu'elle est, mais qu'il la modélise pour nous permettre de survivre. Les interfaces graphiques sont une forme de modélisation de la réalité numérique qui nous permet de manipuler des objets virtuels de manière intuitive.

En effet, lorsque l'on observe nos interfaces modernes, nous y voyons des boutons, des curseurs, des fenêtres. Est-ce la réalité de notre perception ? Si l'on prend une loupe et que l'on regarde de plus près, on se rend compte que ces éléments ne sont que des pixels colorés sur un écran : c'est la réalité de l'interface graphique, mais qui, à cette échelle de perception ne nous permet pas de comprendre ce que nous manipulons.

Le scarabée Julodimorpha bakewelli illustre la complexité de la perception. Massif, brillant et brun, il présente un dimorphisme marqué : la femelle, incapable de voler, attend au sol tandis que le mâle la recherche dans les airs. Homo sapiens, dans un but festif, abandonne parfois de grandes bouteilles de bière ambrée dans l'Outback australien. Or ces bouteilles partagent les caractéristiques physiques des femelles scarabées. Les mâles se ruent alors sur ces contenants pour tenter de s'accoupler, délaissant leurs congénères réelles et mettant l'espèce en péril. L'Australie a dû modifier la forme de ses bouteilles pour préserver les scarabées.

Peut-on considérer un instant que ces scarabées perçoivent la réalité telle qu'elle est ? De leur point de vue, aucun doute n'est possible ; de notre perspective, la situation paraît risible et dénuée de sens. L'évolution leur a fourni un raccourci : une femelle, c'est tout ce qui est massif, brillant et brun — et plus c'est gros, mieux c'est. Ce point de vue peut naturellement être généralisé. Des êtres venus d'ailleurs nous voyant cliquer sur des boutons pour faire clignoter de petites lumières colorées pourraient eux aussi s'interroger sur notre perception du réel. La question est donc philosophique autant que technique.

Toutes ces considérations doivent nous amener à réfléchir à l'utilité même d'une interface graphique. Doit-elle être séduisante et donner l'illusion qu'elle se substitue au réel, ou au contraire rester avant tout fonctionnelle pour répondre à un besoin précis et offrir une interaction plus performante qu'une interface rudimentaire ?

La technologie et l'avènement de la souris ont façonné une nouvelle manière de penser l'interaction entre l'homme et la machine. L'histoire des interfaces graphiques remonte à 1963, avec la conception du « Sketchpad » par Ivan Sutherland, l'un des premiers systèmes à exploiter des concepts graphiques.

![sketchpad](/assets/images/sketchpad.png)

Cependant, c'est Xerox qui, dans les années 1970, avec son **Xerox Alto**, pose les bases des GUI modernes. La véritable révolution survient avec l'introduction des interfaces graphiques par Apple en 1984, via le Macintosh, suivi de près par Microsoft avec Windows. Ces systèmes d'exploitation grand public intègrent les concepts de fenêtres, d'icônes et de menus, offrant une alternative conviviale à l'interface en ligne de commande.

![Xerox Alto](/assets/images/xerox-alto.png)

Depuis, les interfaces graphiques n'ont cessé d'évoluer, s'adaptant aux nouvelles technologies (interfaces tactiles, commandes vocales) et aux besoins des utilisateurs. Aujourd'hui, les GUI se retrouvent non seulement sur les ordinateurs de bureau, mais aussi sur les appareils mobiles, les objets connectés et les systèmes embarqués.

Que seront-elles demain ? Réalité augmentée, intelligence artificielle et neurofeedback via des interfaces cerveau-ordinateur commencent déjà à émerger, notamment avec Neuralink.

## La technologie actuelle

Nous voyons que définir une interface graphique est un problème bien plus vaste qui conteste notre perception du réel, les objectifs pragmatiques d'un problème d'ingénierie, les innovations technologiques et les perspectives d'avenir. Néanmoins s'il est important de comprendre ces enjeux, il est tout aussi important de savoir comment construire une interface graphique avec les technologies actuelles.

### Types d'interfaces graphiques
Le défi technique de la construction d'une interface graphique, outre les critères d'efficacité et d'ergonomie, réside dans la portabilité. Tout au long de ce cours, nous abordons les problèmes de compatibilité entre les systèmes d'exploitation et les différentes technologies d'interfaces. On peut citer aujourd'hui plusieurs catégories fondamentales d'interfaces graphiques :

#### Interfaces spécialisées d'équipements

Les interfaces graphiques de commandes d'équipements professionnels se substituent aujourd'hui aux tableaux de bord et à leurs boutons physiques par des écrans tactiles et des interfaces graphiques configurables et évolutives. Ces interfaces permettent de contrôler des machines complexes, de visualiser des données en temps réel et de surveiller des processus industriels. On observe sur les deux figures ci-dessous une table de mixage traditionnelle et une table de mixage numérique ou la transition technologique est clairement visible.

![Table de mixage traditionnelle](/assets/images/sound-mixing.png)

![Table de mixage numérique Lawo](/assets/images/lawo.png)

Ces interfaces propriétaires n'ont pas vocation à être portables. Elles sont conçues pour un équipement spécifique et sont souvent développées dans des langages de haut niveau comme le C++, Java ou C#. Les composants graphiques sont fréquemment réalisés sur mesure pour répondre aux besoins précis du dispositif.

#### Interfaces portables de commande

De la même manière, dans la commande de robots industriels, les télécommandes physiques ont été remplacées par des interfaces graphiques sur tablettes. Les besoins sont plus génériques et les interfaces sont souvent développées en utilisant des technologies web (HTML5, CSS, JavaScript) ou des technologies multiplateformes comme Flutter ou React Native.

![Interface d'un robot Kuka](/assets/images/kuka-gui.png)

#### Interfaces de contrôle de systèmes embarqués

Lorsque le coût de développement et la puissance de calcul limitée des architectures embarquées deviennent un enjeu, les interfaces graphiques se réduisent parfois à un simple écran tactile. La société Decent Espresso a par exemple conçu une machine à café dotée d'une interface graphique qui rompt avec les codes traditionnels, où de gros boutons et cadrans physiques faisaient office de gage de qualité et de prestige.

![Interface d'une machine à café Decent](/assets/images/decent-espresso.jpg)

Le prestige représentant une part importante de l'expérience, l'interface graphique devient un élément clé qui doit être soigné tant au niveau de l'ergonomie que de l'esthétique et de la fluidité de l'interaction. Ces interfaces sont majoritairement développées à l'aide de technologies web ou multiplateformes (Qt, HTML, JavaScript).

#### Applications embarquées

![Embedded Wizard](/assets/images/embedded-wizard.png)

#### Applications mobiles

![Interface de commande du robot Spot de Boston Dynamics](/assets/images/spot-controller.png)

#### Applications PC multiplateformes

![AutoCAD 2025](/assets/images/autocad2025.jpg)

## Ergonomie

L'ergonomie des interfaces graphiques est au cœur de la conception des logiciels modernes. Il ne s'agit pas simplement d'esthétique, mais bien de la manière dont une interface facilite ou entrave l'utilisation. Une bonne interface doit être intuitive, efficace et accessible, permettant à l'utilisateur d'atteindre ses objectifs rapidement et sans frustration.

L'ergonomie, dans le cadre des interfaces graphiques, vise à optimiser l'interaction entre l'utilisateur et le logiciel. Une interface bien pensée doit respecter certains principes clés :

Clarté

: Les éléments visuels doivent être organisés de manière claire et lisible. Chaque bouton, chaque menu doit être facilement identifiable et ses fonctions explicites.

Cohérence

: Les interactions et les comportements des composants doivent être uniformes à travers l'interface. Par exemple, si un bouton annule une action dans une partie de l'application, il doit le faire dans toutes les autres. Un manque de cohérence bien connu concerne les paramètres de Windows : sous Windows 11, un clic sur « Paramètres avancés » ouvre parfois une fenêtre héritée des versions antérieures.

Simplicité

: L'interface doit éviter de surcharger l'utilisateur avec trop d'options ou d'informations. Un design épuré permet à l'utilisateur de se concentrer sur les tâches essentielles. Apple illustre bien cette philosophie avec ses interfaces minimalistes.

Accessibilité

: L'interface doit être accessible à tous les utilisateurs, y compris ceux ayant des limitations physiques ou cognitives. Cela inclut l'utilisation de tailles de police adéquates, de couleurs contrastées et la possibilité de naviguer à l'aide du clavier ou de dispositifs d'assistance.

## Le C et les interfaces graphiques

Je dois l'admettre, le C n'est pas le langage le plus adapté pour le développement d'interfaces graphiques. Les GUI modernes sont souvent construites en utilisant des langages de haut niveau comme C++, Java, C#, Python ou JavaScript, qui offrent des bibliothèques et des frameworks dédiés à la création d'interfaces basées sur des paradigmes objet, asynchrones et événementiels.

Les exemples d'applications graphiques complètes en C restent rares, hormis peut-être [Gimp](https://www.gimp.org/), logiciel de retouche d'images open source qui utilise GTK (GIMP Toolkit). La plupart des bibliothèques graphiques sont écrites en C++, ce qui limite l'offre pour le C sans la rendre inexistante.

La bibliothèque la plus connue pour le développement d'interfaces graphiques en C est GTK, qui est utilisée par de nombreuses applications open source, telles que GIMP, Inkscape, ou encore GNOME. GTK est une bibliothèque multiplateforme qui offre des composants graphiques, des outils de dessin, et une gestion des événements. Elle est écrite en C, mais elle propose des bindings pour de nombreux autres langages, comme Python ou JavaScript. GTK est un excellent choix si vous souhaitez développer des applications graphiques en C, de plus la bibliothèque est portable et bien documentée.

Une autre bibliothèque populaire est SDL, *Simple DirectMedia Layer*, bibliothèque multimédia utilisée pour le développement de jeux vidéo mais qui permet également de créer des interfaces graphiques. Écrite en C, elle propose des liaisons pour de nombreux langages (C++, Python, Lua, etc.). SDL est légère, portable et offre les fonctionnalités de base nécessaires à la création d'interfaces.

Un autre choix, un peu moins populaire mais qui mérite d'être cité pour sa longue histoire, est la bibliothèque [Allegro](https://www.allegro.cc/). Initialement créée pour les ordinateurs Atari dans les années 1990, Allegro est une bibliothèque multimédia offrant des fonctionnalités de dessin 2D, de son et de gestion des entrées utilisateur.

