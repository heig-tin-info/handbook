# Introduction

## Qu’est-ce qu’une interface graphique ?

L'interface graphique, couramment désignée sous l’acronyme GUI (Graphical User Interface), est la couche visuelle par laquelle un utilisateur interagit avec un système informatique. Contrairement aux interfaces en ligne de commande (CLI *Client Line Interface*), où l’utilisateur doit saisir des commandes textuelles, une GUI propose une interaction plus intuitive, fondée sur des éléments visuels tels que des fenêtres, des icônes, des menus et des boutons.

À la naissance de l’informatique, les interactions étaient principalement réservées à des spécialistes capables de comprendre et de manipuler des commandes complexes. L’avènement des interfaces graphiques, au début des années 1980, a marqué un tournant fondamental dans l’accessibilité des systèmes informatiques, ouvrant la voie à une démocratisation rapide de ces technologies.

Le Smaky, développé par le professeur Jean-Daniel Nicoud au LAMI à l'EPFL, est un des premiers ordinateurs grand public à proposer une interface graphique. Il a été commercialisé dès 1978. C'est le premier ordinateur personnel à disposer d'une souris en standard laquelle a été développée en 1962 par Douglas Engelbart. Nicoud ayant été séduit par l'idée l'a perfectionnée au sein de son laboratoire. C'est André Guignard aussi l'origine du robot [Khepera](wiki:khepera) qui développa pour Nicoud la première souris opto-mécanique fabriquée par Depraz et commercialisée par Logitech.

![Souris Depraz](/assets/images/depraz.png)

Depuis lors, les interfaces graphiques ont non seulement rendu les ordinateurs plus accessibles à un public non technique, mais elles ont également transformé l'expérience utilisateur. L'interface graphique permet de manipuler les objets numériques comme s'ils étaient des objets physiques. Cette analogie, que l'on appelle [métaphore d'interface](wiki:metaphore d'interface), est l'un des piliers de la conception des GUI. Par exemple, la corbeille, où l’on dépose les fichiers pour les supprimer, est une métaphore simple mais efficace qui transforme un concept abstrait en une action que tout utilisateur peut comprendre.

En outre, les GUI facilitent les interactions complexes en cachant la complexité du code sous une couche de simplicité visuelle. Chaque clic sur un bouton, chaque interaction avec un menu déclenche des opérations en arrière-plan, rendant l’utilisation du système plus fluide et plus intuitive.

![Scarabé Julodimorpha bakewelli](/assets/images/beetle.png){ #beetle }

Donald Hoffmann dans son excellent TED Talk intitulé [Do we see reality as it is?](https://www.ted.com/talks/donald_hoffman_do_we_see_reality_as_it_is) aborde la question de la perception de la réalité. Il explique que notre cerveau ne perçoit pas la réalité telle qu'elle est, mais qu'il la modélise pour nous permettre de survivre. Les interfaces graphiques sont une forme de modélisation de la réalité numérique qui nous permettent de manipuler des objets virtuels de manière intuitive.

En effet, lorsque l'on observe nos interfaces modernes, nous y voyons des boutons, des curseurs, des fenêtres. Est-ce la réalité de notre perception ? Si l'on prend une loupe et que l'on regarde de plus près, on se rend compte que ces éléments ne sont que des pixels colorés sur un écran : c'est la réalité de l'interface graphique mais qui, à cette échelle de perception ne nous permet pas de comprendre ce que nous manipulons.

Le scarabé Julodimorpha bakewelli est un exemple de la complexité de la réalité. Il est massif, brillant et brun. La femelle est incapable de voler. Le mâle vole, à sa recherche. Il convoite une femelle séduisante. Homo sapiens, dans un but similaire se réuni en groupe dans l'Outback australien accompagné de boissons fermentées qui une fois vites sont laissées à l'abandon. Or, il se trouve que ces bouteilles en verre sont massives, brillantes et brunes : une femelle séduisante. Les mâles scarabés se ruent sur les bouteilles pour tenter de s'accoupler comme illustré sur la figure ci-dessus. Ils perdent tout intérêt pour les femelles réelles et l'espèce a failli disparaître. L'Australie a dû modifier ses bouteilles pour sauver ses scarabées.

Pourrait-on considérer une seconde que ces scarabés perçoivent la réalité telle qu'elle est ? Du point de vue du scarabé il n'y a aucun doute mais de notre perception la situation nous apparait comme risible et dénuée de sens. L'évolution leur a fourni un raccourci; une femelle, c'est tout ce qui est massif, brillant et brun, et plus c'est gros, mieux c'est. Le point de vue peut naturellement être généralisé et des êtres venus d'ailleurs qui nous observeraient nous humains à cliquer sur des boutons pour faire clignoter de petites lumières colorées agencées en grille pourraient se demander si nous percevons la réalité telle qu'elle est. Vous voyez que la question est bien plus philosophique et profonde.

Toute ces considéreation doivent nous amener à s'interroger sur la nature même de l'utilité d'une interface graphique. Doit être elle séduisante et donner l'illusion qu'elle se substitue au réel ou doit être être fonctionnelle et servir un besoin précis d'être plus performante qu'une interface plus rudimentaire dans l'interaction entre l'homme et la machine ?

La technologie et l'avènement de la souris ont crafté une nouvelle manière de penser l'interaction entre l'homme et la machine. L’histoire des interfaces graphiques remonte à 1963, avec la conception du "Sketchpad" par Ivan Sutherland, un des premiers systèmes à exploiter des concepts graphiques.

![sketchpad](/assets/images/sketchpad.png)

Cependant, c’est Xerox qui, dans les années 1970, avec son **Xerox Alto**, pose les bases des GUI modernes. La véritable révolution survient avec l’introduction des interfaces graphiques par Apple en 1984, via le Macintosh, suivi de près par Microsoft avec Windows. Ces systèmes d’exploitation grand public intègrent les concepts de fenêtres, d’icônes et de menus, offrant une alternative conviviale à l’interface en ligne de commande.

![Xerox Alto](/assets/images/xerox-alto.png)

Depuis, les interfaces graphiques n’ont cessé d’évoluer, s’adaptant aux nouvelles technologies (touches tactiles, interfaces vocales) et aux besoins des utilisateurs. Aujourd’hui, les GUI se retrouvent non seulement sur les ordinateurs de bureau, mais aussi sur les appareils mobiles, les objets connectés, et même les systèmes embarqués.

Que seront-elles demain ? La réalité augmentée, l'intelligence artificielle, le neurofeedback avec des interfaces cerveau-ordinateur qui commencent à émerger notament avec le Neuralink d'Elon Musk.

## La technologie actuelle

Nous voyons que définir une interface graphique est un problème bien plus vaste qui questionne notre perception du réelle, les objectifs pragmatiques d'un problème d'ingénierie, les innovations technologiques et les perspectives d'avenir. Néanmoins s'il est important de comprendre ces enjeux, il est tout aussi important de savoir comment construire une interface graphique avec les technologies actuelles.

### Types d'interfaces graphiques
Le défi technique de la construction d'une interface graphique outre les critères d'efficacité et d'ergonomie est la portabilité de l'interface. Tout au long de se cours, nous abordons les problèmes de compatibilité entre les systèmes d'exploitation et les différentes technologies d'interfaces. On peut citer aujourd'hui plusieurs catégories fondamentales d'interfaces graphiques :

#### Interfaces spécialisées d'équipements

Les interfaces graphiques de commandes d'équipements professionnels se substituent aujourd'hui aux tableaux de bord et leurs boutons physiques par des écrans tactiles et des interfaces graphiques configurables et évolutives. Ces interfaces permettent de contrôler des machines complexes, de visualiser des données en temps réel et de surveiller des processus industriels. On observe sur les deux figures ci-dessous une table de mixage traditionnelle et une table de mixage numérique ou la transition technologique est clairement visible.

![Table de mixage traditionnelle](/assets/images/sound-mixing.png)

![Table de mixage numérique Lawo](/assets/images/lawo.png)

Ces interfaces propriétaires n'ont pas vocation à être portable, elles sont conçues pour un équipement spécifique et sont souvent développées dans des langages haut niveau comme le C++ le Java ou le C#. Les composants graphiques sont souvent développés sur mesure pour répondre aux besoins spécifiques de l'équipement.

#### Interfaces portables de commande

De la même manière, dans la commande de robots industriels, les télécommandes physiques ont été remplacées par des interfaces graphiques sur tablettes. Les besoins sont plus génériques et les interfaces sont souvent développées en utilisants des technologies web (HTML5, CSS, JavaScript) ou des technologies multiplateformes comme Flutter ou React Native.

![Interface d'un robot Kuka](/assets/images/kuka-gui.png)

#### Interfaces de contrôle de systèmes embarqués

Là ou le coût de développement et la puissance de calcul limitée des architectures embarquée est un enjeu, les interfaces graphiques sont réduites à un simple écran tactile. La société Decent Espresso a développé par exemple une machine à café avec une interface graphique brisant les codes des machines à café traditionnelles ou de gros boutons et cadrans physiques étaient gage de qualité et de prestige.

![Interface d'une machine à café Decent](/assets/images/decent-espresso.jpg)

Le prestige étant une part importante du besoin de l'équipement, l'interface graphique est un élément clé qui doit être soigné tant au niveau de l'ergonomie que de l'esthétisme et de la fluidité de l'interaction. Ces interfaces sont majoritairement développées en utilisant des technologies web ou des technologies multiplateformes (QT, HTML, JavaScript).

#### Applications embarquées

![Embedded Wizard](/assets/images/embedded-wizard.png)

#### Applications mobiles

![Interface de commande du robot Spot de Boston Dynamics](/assets/images/spot-controller.png)

#### Applications PC multiplateformes

![AutoCAD 2025](/assets/images/autocad2025.jpg)

### Technologies

- Kivy
- Qt
- GTK
- wxWidgets
- FLTK
- Dear ImGui
- Tkinter
- JavaFX
- Libui
- Motif / X11 Toolkit
- Embedded Wizard

## Principe de conception

### Ergonomie

L’ergonomie des interfaces graphiques est au cœur de la conception des logiciels modernes. Il ne s'agit pas simplement d'esthétique, mais bien de la manière dont une interface facilite ou entrave l’utilisation par l’utilisateur. Une bonne interface doit être intuitive, efficace et accessible, permettant à l’utilisateur d’atteindre ses objectifs rapidement et sans frustration.

L'ergonomie, dans le cadre des interfaces graphiques, vise à optimiser l'interaction entre l’utilisateur et le logiciel. Une interface bien pensée doit respecter certains principes essentiels :

Clarté

: Les éléments visuels doivent être organisés de manière claire et lisible. Chaque bouton, chaque menu, doit être facilement identifiable et ses fonctions, explicites.

Cohérence

: Les interactions et les comportements des composants doivent être uniformes à travers l’interface. Par exemple, si un bouton annule une action dans une partie de l'application, il doit le faire dans toutes les autres.

Simplicité

: L’interface doit éviter de surcharger l’utilisateur avec trop d’options ou d’informations. Un design épuré permet à l’utilisateur de se concentrer sur les tâches essentielles.

Accessibilité

: L’interface doit être accessible à tous les utilisateurs, y compris ceux ayant des limitations physiques ou cognitives. Cela inclut l'utilisation de tailles de police adéquates, de couleurs contrastées et la possibilité de naviguer à l’aide du clavier ou de dispositifs d’assistance.

### Interactivité

L’interactivité désigne la manière dont l’utilisateur interagit avec l’interface et comment celle-ci réagit à ses actions. Une interface doit non seulement être réactive, mais aussi donner des retours clairs à l’utilisateur. Selon les utilisation l'utilisateur à besoin d'une réactivité immédiate comme un retour haptique ou visuel pour une assurance de la prise en compte de son action.

2.2.2 Portabilité La diversité des plateformes (Windows, macOS, Linux, Android, iOS) pose un défi majeur en matière de portabilité des interfaces. Développer une interface graphique qui fonctionne de manière native sur plusieurs systèmes d’exploitation peut vite devenir un casse-tête technique. Certaines bibliothèques comme GTK ou Qt offrent une certaine abstraction pour rendre les interfaces portables, mais cela se fait parfois au prix de la performance ou d'une personnalisation limitée sur chaque plateforme. Le dilemme repose alors sur le choix entre une approche native pour chaque plateforme (offrant une meilleure intégration mais au prix d'un effort de développement multiplié) ou une approche multiplateforme plus simple à maintenir, mais potentiellement moins performante.

2.2.3 Qualité visuelle La qualité visuelle de l’interface est un autre facteur clé. Les utilisateurs s'attendent à des interfaces élégantes, modernes, et souvent riches en détails graphiques. Cependant, cela peut rapidement accroître la complexité du développement. Par exemple, des éléments graphiques haute définition ou des animations fluides nécessitent un matériel graphique performant. Le dilemme consiste ici à trouver un équilibre entre la qualité visuelle et les performances. Il est souvent nécessaire d'offrir plusieurs niveaux de qualité graphique pour accommoder différents types d'appareils.

2.2.4 Simplicité du développement La simplicité de développement est un facteur déterminant dans le choix des technologies employées pour créer une interface graphique. Certaines bibliothèques offrent une abstraction qui permet de créer rapidement des interfaces graphiques sans trop se soucier des détails techniques, mais au prix d’une certaine flexibilité. D'autres solutions, comme les API bas-niveau telles que OpenGL, offrent une grande liberté et des performances optimisées, mais nécessitent beaucoup plus de temps et d’expertise pour être mises en œuvre. Le dilemme est de savoir s’il faut opter pour une solution rapide et simple, souvent suffisante pour des applications modestes, ou pour une approche plus complexe mais optimisée pour des usages avancés.

2.2.5 Coût des licences Un dernier facteur non négligeable est le coût des licences. De nombreuses bibliothèques graphiques sont gratuites et open-source, comme GTK ou SDL2, mais certaines, comme Qt, peuvent nécessiter des licences commerciales pour des projets propriétaires. Ces coûts doivent être pris en compte lors du choix d'une solution, particulièrement pour les entreprises à budget limité. Le dilemme ici réside dans le choix entre une solution open-source, souvent gratuite mais possiblement moins adaptée à des besoins spécifiques, ou une solution commerciale offrant un support et des fonctionnalités plus avancées, mais à un coût financier.
