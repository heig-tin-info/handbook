# Le code de conduite

Être développeur logiciel que ce soit professionnellement ou comme loisir, ce n'est pas simplement écrire du code. Il y a l'art et la manière de le faire, il y a des règles à respecter, des consensus à suivre et des bonnes pratiques à adopter.

J'ai vu trop souvent dans le milieu académique et professionnel, des soit disant experts ou professeurs qui inclulquent à leurs élèves ou collègues des pratiques dogmatiques basées sur des croyances personnelles ou des habitudes anciennes. L'informatique est une discipline avant tout basée sur la collaboration, l'écoute, l'introspection. Il est donc essentiel d'avoir l'esprit ouvert, et de faire preuve d'humilité.

On ne développe pas sur des acquis et des croyances figés mais sur des principes et des valeurs qui évoluent avec le temps et qui dépendent du milieu. Un développeur web ne développera pas de la même manière qu'un scientifique en Python ou un développeur embarqué.

Les valeurs humaines fondamentales du développement logiciel sont :

- L'ouverture d'esprit
- L'humilité
- La curiosité
- La rigueur
- La patience
- La persévérance
- L'écoute
- L'entraide
- Le partage

## L'Anglais

![La langue une barrière](../assets/figures/english.png)

En programmation, quel que soit le langage utilisé, la langue **anglaise** est omniprésente. D'une part les mots clés des langages de programmation sont majoritairement empruntés à l'anglais, mais souvent les outils de développement ne sont disponibles qu'en anglais. Il existe une raison à cela. Un article de journal publié dans une revue locale sera certainement lu par madame Machin et monsieur Bidule, mais n'aura aucun intérêt pour les habitants de l'antipode néo-zélandais. En programmation, le code se veut **réutilisable** pour économiser des coûts de développement. On réutilise ainsi volontiers des algorithmes écrits par un vénérable japonais, ou une bibliothèque de calcul matriciel développée en Amérique du Sud. Pour faciliter la mise en commun de ces différents blocs logiciels et surtout pour que chacun puisse dépanner le code des autres, il est essentiel qu'une langue commune soit choisie et l'anglais est le choix le plus naturel.

Aussi dans cet ouvrage, l'anglais sera privilégié dans les exemples de code et les noms des symboles (variables, constantes ...), les termes techniques seront traduits lorsqu'il existe un consensus établi sinon l'anglicisme sera préféré. Il m'est d'ailleurs difficile, bien que ce cours soit écrit en français de parler de *feu d'alerte* en lieu et place de *warning*, car si l'un est la traduction ad hoc de l'autre, la terminologie n'a rien à voir et préfère, au risque d'un affront avec l'Académie, préserver les us et coutumes des développeurs logiciels.

Un autre point méritant d'être mentionné est la constante interaction d'un développeur avec internet pour y piocher des exemples, chercher des conseils, ou de l'aide pour utiliser des outils développés par d'autres. De nombreux sites internet, la vaste majorité en anglais, sont d'une aide précieuse pour le développeur. On peut ainsi citer :

## Apprendre à pêcher

![Un père et son fils pêchant](../assets/figures/fisherman.png)

Un jeune homme s'en va à la mer avec son père et lui demande: papa, j'ai faim, comment ramènes-tu du poisson? Le père fier, lance sa ligne à la mer et lui ramène un beau poisson. Plus tard, alors que le jeune homme revient d'une balade sur les estrans, il demande à son père: papa, j'ai faim, me ramènerais-tu du poisson? Le père, sort de son étui sa plus belle canne et l'équipant d'un bel hameçon lance sa ligne à la mer et ramène un gros poisson. Durant longtemps, le jeune homme mange ainsi à sa faim cependant que le père ramène du poisson pour son fils.

Un jour, alors que le fils invective son père l'estomac vide, le père annonce. Fils, il est temps pour toi d'apprendre à pêcher, je peux te montrer encore longtemps comment je ramène du poisson, mais ce ne serait pas t'aider, voici donc cette canne et cet hameçon.

Le jeune homme tente de répéter les gestes de son père, mais il ne parvient pas à ramener le poisson qui le rassasierait. Il demande à son père de l'aide que ce dernier refuse. Fils, c'est par la pratique et avec la faim au ventre que tu parviendras à prendre du poisson, persévère et tu deviendras meilleur pêcheur que moi, la lignée ainsi assurée de toujours manger à sa faim.

La morale de cette histoire est plus que jamais applicable en programmation, confier aux expérimentés l'écriture d'algorithmes compliqués, ou se contenter d'observer les réponses des exercices pour se dire: j'ai compris ce n'est pas si compliqué, est une erreur, car pêcher ou expliquer comment pêcher n'est pas la même chose.

Aussi, cet ouvrage se veut être un guide pour apprendre à apprendre le développement logiciel et non un guide exhaustif du langage, car le standard C99/C11 est disponible sur internet ainsi que le K&R qui reste l'ouvrage de référence pour apprendre C. Il est donc inutile de paraphraser les exemples donnés quand internet apporte toutes les réponses, pour tous les publics du profane réservé au hacker passionné.

## Une affaire de consensus

En informatique comme dans la société humaine, il y a les religieux, les prosélytes, les dogmatiques, les fanatiques, les contestataires et les maximalistes.
Le plus souvent les motifs de fâcheries concernent les outils que ces derniers utilisent et ceux dont on doit taire le nom. Ils se portent parfois sur les conventions de codage à respecter, l'encodage des fichiers, le choix de l'[EOL](https://fr.wikipedia.org/wiki/Fin_de_ligne), l'interdiction du `goto`, le respect inconditionnel des règles [MISRA](https://en.wikipedia.org/wiki/MISRA_C).
Il existe ainsi de longues guerres de croyances, parfois vielles de plusieurs générations et qui perdurent souvent par manque d'ouverture d'esprit et surtout parce que la bonne attitude à adopter n'est pas enseignée dans les écoles supérieures là où les dogmes s'établissent et pénètrent les esprits dociles, faute au biais d'[ancrage mental](<https://fr.wikipedia.org/wiki/Ancrage_(psychologie)>).
L'enseignant devrait être sensible à ces aspects fondamentaux et devrait viser l'impartialité en visant l'ouverture l'esprit et le culte du bon sens de l'ingénieur.

Citons par exemple les [guerres d'éditeurs](https://fr.wikipedia.org/wiki/Guerre_d%27%C3%A9diteurs) qui date des années 1970 et qui opposent les défenseurs de l'éditeur `vi` aux inconditionnels d'`emacs`. Il s'agit de deux éditeurs de texte très puissants et à la courbe d'apprentissage raide qui séparent les opinions tant leur paradigme de fonctionnement est aporétique. Ces guerres sont d'abord entretenues par plaisir de l'amusement, mais les foules de convertis ne s'aperçoivent pas toujours de l'envergure émotionnelle que prend l'affaire dans son ensemble et force est de constater qu'avec le temps ils ne parviennent plus à percevoir le monde tel qu'il est, à force d'habitudes.

S'enterrer dans une zone de confort renforce le biais du [Marteau de Maslow](https://everlaab.com/marteau-de-maslow/), car lorsque l'on est un marteau, on ne voit plus les problèmes qu'en forme de clou. Cette zone de confort devient un ennemi et barre l'accès au regard critique et au pragmatisme qui devrait prévaloir. Car accepter l'existence de différentes approches possibles d'un problème donné est essentiel, car plus que dans tout autre domaine technique, le développement logiciel est avant tout une aventure collaborative qui ne devrait jamais être sous le joug d'une quelconque emprise émotionnelle.

Un programme se doit d'être le plus neutre possible, impartial et minimaliste. Il n'est pas important de se préoccuper des affaires cosmétiques telles que la position des accolades dans un programme, le choix d'utiliser des espaces versus des tabulations horizontales, ou le besoin d'utiliser tel ou tel outil de développement parce qu'il est jugé meilleur qu'un autre.

La clé de la bonne attitude c'est d'être à l'écoute du consensus de ne pas sombrer au [biais d'attention](https://en.wikipedia.org/wiki/Attentional_bias). Il faut non seulement être sensible au consensus local direct: son entreprise, son école, son équipe de travail, mais surtout au consensus planétaire dont l'accès ne peut se faire que par l'interaction directe avec la communauté de développeurs, soit par les forums de discussions (Reddit, stackoverflow), soit par le code lui-même. Vous avez un doute sur la bonne méthode pour écrire tel algorithme ou sur la façon dont votre programme devrait être structuré ? Plongez-vous dans le code des autres, multipliez vos expériences, observez les disparités et les oppositions, et apprenez à ne pas y être sensible.

Vous verrez qu'au début, un programme ne vous semble lisible que s'il respecte vos habitudes, la taille de vos indentations préférées, la police de caractère qui vous sied le mieux, l'éditeur qui supporte les ligatures, car admettez-le `ﬁ` est infiniment plus lisible que `fi`. Par la suite, et à la relecture de cette section, vous apprendrez à faire fi de cette zone de confort qui vous était si chère et que l'important n'est plus la forme, mais le fond. Vous aurez comme [Néo](<https://fr.wikipedia.org/wiki/Neo_(Matrix)>), libéré votre esprit et serez capable de voir la matrice sans filtre, sans biais.

En somme, restez ouvert aux autres points de vues, cherchez à adopter le consensus majoritaire qui dynamise au mieux votre équipe de développement, qui s'encadre le mieux dans votre stratégie de croissance et de collaboration et surtout, abreuvez-vous de code, faites-en des indigestions, rêvez-en la nuit. Vous tradez du Bitcoin, allez lire [le code source](https://github.com/bitcoin/bitcoin), vous aimez Linux, plongez-vous dans le code source du [kernel](https://github.com/torvalds/linux), certains collègues ou amis vous ont parlé de Git, allez voir ses [entrailles](https://github.com/git/git)... Oui, tous ces projets sont écrits en C, n'est-ce pas merveilleux ?

## L'open source

Au début de l'informatique, les programmes étaient distribués avec le code source, car les ordinateurs étaient rares et coûteux et que les utilisateurs étaient souvent des développeurs. Avec l'arrivée des ordinateurs personnels, les éditeurs de logiciels ont commencé à distribuer des programmes compilés, car les utilisateurs n'étaient plus des développeurs et que le code source était devenu un secret industriel. C'est ainsi que le logiciel propriétaire est né. Les éditeurs de logiciels ont profité de cette situation pour verrouiller leurs clients dans un écosystème propriétaire, les empêchant de modifier le logiciel, de le partager ou de le vendre.

Dans les années 1980, Richard Stallman, un informaticien américain, a lancé le projet GNU pour créer un système d'exploitation libre, c'est-à-dire un système d'exploitation dont le code source est librement accessible, modifiable et redistribuable. Néanmoins la license GPL (GNU Public License) qui protège le code source de GNU est très contraignante et ne permet pas de créer des logiciels propriétaires basés sur du code source GPL. C'est un frein pour les entreprises qui souhaitent protéger leur propriété intellectuelle.

En 1991, Linus Torvalds, un étudiant finlandais, a créé le noyau Linux, qui est devenu le noyau du système d'exploitation GNU/Linux. Depuis lors, de nombreux logiciels libres ont été développés, notamment le navigateur web Firefox, le serveur web Apache, le système de gestion de base de données MySQL, le langage de programmation Python, le système de gestion de versions Git, etc.

Cette philosophie du logiciel libre a été popularisée par le hacker américain Eric Raymond dans son essai "La cathédrale et le bazar" qui décrit deux modèles de développement logiciel : le modèle de la cathédrale, où le code source est développé en interne par une équipe restreinte, et le modèle du bazar, où le code source est développé de manière collaborative par une communauté de développeurs.

L'expression *open source* s'est largement imposée dans le monde de l'informatique pour désigner les logiciels libres, car elle est plus neutre et moins idéologique que l'expression *logiciel libre*. De grandes sociétés comme Google, Facebook, Microsoft, IBM, Oracle, etc. ont adopté la philosophie du logiciel libre et contribuent activement à de nombreux projets open source. Par exemple, Google a développé le système d'exploitation Android, qui est basé sur le noyau Linux, et qui est utilisé par la plupart des smartphones dans le monde. Facebook a développé le framework React, qui est utilisé par de nombreux sites web pour créer des interfaces utilisateur interactives. Microsoft a racheté GitHub, la plateforme de développement collaboratif la plus populaire au monde, et a ouvert le code source de nombreux projets, notamment le framework .NET. IBM a racheté Red Hat, l'éditeur de la distribution Linux Red Hat Enterprise Linux, et contribue activement à de nombreux projets open source.

Mettre un logiciel ou une partie de logiciel en open source c'est permettre à d'autres développeurs de contribuer au projet, de corriger des bugs, d'ajouter des fonctionnalités, de traduire le logiciel dans d'autres langues, etc. C'est aussi un moyen de faire connaître son travail, de se faire un nom dans la communauté des développeurs, de trouver un emploi, de créer une entreprise, etc. Mais c'est aussi un moyen de partager ses connaissances, de contribuer à l'éducation, à la recherche, à la culture, à l'humanité.

L'open source est devenu un modèle économique viable pour de nombreuses entreprises, qui vendent des services autour de logiciels open source, comme le support, la formation, la personnalisation, l'hébergement, etc. C'est aussi un moyen de réduire les coûts de développement, de mutualiser les efforts, de partager les risques, de favoriser l'innovation et de promouvoir la transparence.

Pourquoi ne pas faire d'open source ? C'est une question que vous vous poserez tôt ou tard dans votre carrière de développeur. Vous avez peut-être peur de la concurrence, de la critique, du piratage, de la perte de contrôle, de la complexité, de l'engagement, de la responsabilité, de la réputation, de la légalité, de la sécurité, de la confidentialité, de la propriété intellectuelle, etc. De nombreuses sociétés ont fait le choix de protéger leur propriété intellectuelle en gardant leur code source secret, mais cela à un coût. Les logiciels doient être protégés par des licences, des brevets, le code doit être crypté, les serveurs doivent être sécurisés, les employés doivent être surveillés, les clients doivent être contrôlés, etc. C'est un cercle vicieux qui peut conduire à la paranoïa, à la méfiance.

## La communauté

Se passionner pour le développement logiciel c'est aussi se passionner pour la communauté des développeurs. Avant internet, les développeurs se rencontraient dans des clubs d'informatique, des associations d'utilisateurs, des conférences, des salons, des formations, des hackathons, des meetups, etc. Avec internet, les développeurs se rencontrent sur des forums, des listes de diffusion, des chats, des blogs, des réseaux sociaux, des plateformes de développement collaboratif, etc.

GitHub a été créé en 2008 par Tom Preston-Werner, Chris Wanstrath, PJ Hyett et Scott Chacon pour faciliter le développement collaboratif de logiciels open source. GitHub est devenu la plateforme de développement collaboratif la plus populaire au monde, avec plus de 100 millions de dépôts de code source, plus de 40 millions de développeurs. On y trouve de tout, il suffit de chercher.

Pour les questions techniques, il y a Stack Overflow, un site de questions-réponses créé en 2008 par Jeff Atwood et Joel Spolsky. Stack Overflow est devenu le site de questions-réponses le plus populaire au monde, avec plus de 10 millions de questions, plus de 20 millions de réponses, plus de 10 millions de membres. Je vous encourage personnellement à y contribuer, cela commence par créer un compte, poser des questions, répondre à des questions, voter pour des questions, voter pour des réponses.

Voici quelques liens utiles :

[Stack Overflow](https://stackoverflow.com/)

: Aujourd'hui le plus grand portail de questions/réponses dédié à la programmation logicielle

[GitHub](https://github.com/)

: Un portail de partage de code

[Google Scholar](https://scholar.google.ch/)

: Un point d'entrée essentiel pour la recherche d'articles scientifiques

[Man Pages](https://linux.die.net/man/)

: La documentation (*man pages*) des commandes et outils les plus utilisés dans les environnements macOS/Linux/Unix et POSIX compatible.

## La revue de code

La revue de code est une pratique essentielle pour améliorer la qualité du code source, la productivité des développeurs, la sécurité des logiciels, la satisfaction des clients. La revue de code consiste à examiner le code source d'un développeur par un autre développeur pour détecter des erreurs, des anomalies, des incohérences, des inefficacités, des non-conformités, des risques, des opportunités. La revue de code peut être formelle ou informelle, manuelle ou automatique, individuelle ou collective, interne ou externe, systématique ou aléatoire, planifiée ou impromptue, etc.

Dans les entreprises c'est un des plus gros problème. Les développeurs n'aiment pas qu'on critique leur code, les chefs de projet n'aiment pas perdre du temps à examiner le code, les clients n'aiment pas payer pour la revue de code, les managers n'aiment pas les conflits entre développeurs, les commerciaux n'aiment pas les retards de livraison, les juristes n'aiment pas les risques de litige. Les gens manquent d'humilité et d'ouverture d'esprit. Pourtant, s'ouvrir à la critique, cela permet de s'améliorer et d'apprendre.