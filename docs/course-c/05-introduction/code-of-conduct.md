---
epigraph:
    text: "Les programmes doivent être écrits pour être lus par des humains, et seulement accessoirement pour être exécutés par des machines."
    source: Harold Abelson
---
# Développement logiciel

**Objectifs**

- Cerner les valeurs et les bonnes pratiques du développement logiciel.
- Saisir l'importance d'apprendre par soi-même.
- Mesurer le rôle pivot de l'anglais en informatique.
- Comprendre l'apport fondamental de la communauté des développeurs et développeuses.

Devenir développeuse ou développeur logiciel, que ce soit par métier ou par passion, ne se limite pas à écrire du code. Cette discipline requiert une finesse d’exécution, le respect de règles, de consensus partagés et l’appropriation de bonnes pratiques.

J’ai souvent observé, dans les milieux académiques comme professionnels, des personnes se revendiquant expertes ou professeures transmettre à leurs élèves ou collègues des pratiques dogmatiques nourries de croyances personnelles ou d’habitudes désuètes. Or l’informatique est une [[discipline]] vivante, fondée sur la collaboration, l’écoute et l’introspection. Il est donc primordial d’avoir l’esprit ouvert et de cultiver l’humilité.

On ne développe pas sur la base de certitudes figées, mais en s’appuyant sur des principes et des valeurs qui évoluent avec le temps et changent selon le contexte. Un ou une [[développeur·euse]] web n’adoptera pas les mêmes approches qu’un scientifique utilisant Python ou qu’une personne spécialisée dans l’embarqué.

Dans le cadre de projets personnels, il est possible de coder seul·e. Mais en entreprise, vous faites partie d’une équipe. Le code que vous écrivez doit pouvoir perdurer après votre départ. Il doit rester lisible, maintenable, testable et évolutif. Il doit se conformer aux standards de l’entreprise, respecter les conventions de codage, les bonnes pratiques, les règles de sécurité et les normes de qualité. Il doit être documenté, commenté, versionné et archivé. Bref, il doit pouvoir être partagé, diffusé, échangé. Des méthodes de travail éprouvées existent pour cela, et nous les aborderons dans ce cours.

Cependant, les valeurs humaines fondamentales du développement logiciel transcendent les considérations purement techniques et méthodologiques. Elles restent stables, comme celles qui régissent la société depuis des millénaires : ouverture d’esprit, humilité, [[curiosité]], rigueur, [[patience]], persévérance, écoute, entraide et partage.

## Les règles évoluent

En [[1750]] av. J.-C., le roi [[Hammurabi de Babylone]] a gravé sur une stèle de basalte le premier code de lois connu de l’histoire. Ce code, qui comprend 282 lois, régissait la vie quotidienne en [[Mésopotamie]]. Bien que ces lois soient considérées comme un jalon important vers une justice équitable, elles imposaient des sanctions souvent sévères : châtiments corporels, mutilations, esclavage, voire exécutions. La célèbre [[loi du talion]], "œil pour œil, dent pour dent", en est un exemple emblématique.

![Code d'Hammurabi (1750 av. J.-C.)](/assets/images/hammurabi.png)

Ce qu’il faut retenir de cette analogie avec le développement logiciel, c’est que, tout comme les conventions sociales, les règles et les consensus en informatique changent avec le temps. Les bonnes pratiques d’aujourd’hui seront probablement différentes demain.

Hélas, l’inertie des institutions, des entreprises et des individus conduit à la perpétuation d’habitudes et à l’établissement de dogmes sans que l’on s’en aperçoive. Il est donc indispensable de faire preuve d’ouverture d’esprit, de remise en question et de curiosité pour s’adapter à un monde en perpétuelle évolution.

En d’autres termes, ce que je vous transmets aujourd’hui n’est pas une vérité absolue. Mon propos est teinté par mon vécu, mes expériences et mes valeurs. Il vous appartient donc de le questionner et d’y réfléchir avec esprit critique.

## L'Anglais

![La langue, une barrière](/assets/images/english.png)

En programmation, quel que soit le langage utilisé, l’anglais est omniprésent. Les mots-clés des langages sont majoritairement issus de l’anglais, et bon nombre d’outils de développement sont exclusivement disponibles dans cette langue. Pourquoi cela ? Tout comme un article de journal local n’intéressera que peu de lectrices et lecteurs à l’autre bout du globe, un code informatique doit pouvoir être réutilisé pour réduire les coûts de développement et s’affranchir des barrières linguistiques.

On réutilise ainsi volontiers un algorithme écrit par un programmeur japonais ou une bibliothèque de calcul matriciel développée en Amérique du Sud. Pour que chacune et chacun puisse corriger, maintenir ou améliorer le code des autres, une langue commune s’impose, et l’anglais est naturellement devenu cette langue.

Dans ce cours, bien que rédigé en français, l’anglais sera privilégié pour les exemples de code et les noms des symboles (variables, constantes, etc.). Les termes techniques seront traduits lorsqu’un consensus existe ; à défaut, l’anglicisme restera la référence. Parler de « feu d’alerte » à la place de *warning* ferait perdre la nuance technique. J’opte donc, même au risque de froisser l’Académie, pour préserver les usages établis parmi les développeuses et développeurs.

Un autre point mérite d’être souligné : la consultation quasi constante d’Internet par toute personne qui programme pour y puiser exemples, conseils ou assistance dans l’utilisation d’outils développés par d’autres. La majorité de ces ressources sont en [[anglais]].

!!! tip "Apprenez les langues"

    Ne négligez pas les cours de langues. Partez à l’étranger, lisez des livres en anglais, regardez des films en version originale, écoutez des podcasts, des conférences et des tutoriels en anglais : cela vous ouvrira d’innombrables portes.

    Sans cette compétence, trouver un emploi peut s’avérer bien plus difficile, car les entreprises sont souvent internationales et les équipes de développement multiculturelles.

## Apprendre à pêcher

![Un père et son fils pêchant](/assets/images/fisherman.png)

Un jeune homme part en mer avec son père et lui demande : « Papa, j’ai faim, comment ramènes-tu du poisson ? » Le père, fier, lance sa ligne et lui rapporte un beau poisson. Plus tard, alors que le jeune homme revient d’une balade sur l’estran, il demande : « Papa, j’ai faim, me ramènerais-tu du poisson ? » Le père sort de son étui sa plus belle canne, l’équipe d’un hameçon et, d’un geste précis, ramène encore une belle prise. Pendant longtemps, le fils mange ainsi à sa faim grâce à la patience de son père.

Un jour pourtant, alors que le fils s’impatiente l’estomac vide, le père lui annonce : « Il est temps pour toi d’apprendre à pêcher. Je pourrais continuer à t’apporter du poisson, mais ce ne serait pas t’aider. Voici donc cette canne et cet hameçon. »

Le jeune homme tente de reproduire les gestes de son père, sans parvenir à attraper le poisson qui le rassasierait. Il réclame de l’aide, que son père refuse : « C’est par la pratique, avec la faim au ventre, que tu apprendras à prendre du poisson. Persévère et tu deviendras un meilleur pêcheur que moi ; ainsi la lignée mangera toujours à sa faim. »

La morale de cette histoire s’applique parfaitement à la programmation : confier aux plus expérimentés l’écriture des algorithmes difficiles ou se contenter d’observer les corrigés pour se dire « j’ai compris, ce n’est pas si compliqué » est une erreur, car pêcher et expliquer comment pêcher n’est pas la même chose.

Cet ouvrage se veut donc un guide pour apprendre à apprendre le développement logiciel, et non un manuel exhaustif du langage. Le standard C99/C11 est accessible en ligne, tout comme le K&R qui demeure l’ouvrage de référence pour découvrir le C. Inutile de paraphraser ces ressources : Internet regorge déjà de réponses pour tous les publics, du profane curieux au hacker passionné.


## Une affaire de consensus

En informatique, tout comme dans la société, il existe des religieux, des prosélytes, des dogmatiques, des fanatiques, des contestataires et des maximalistes. Leurs querelles portent souvent sur les outils qu'ils utilisent ou sur des pratiques dont on ne doit pas dévier. Ils débattent parfois âprement des conventions de codage, de l'encodage des fichiers, du choix de la [fin de ligne](https://fr.wikipedia.org/wiki/Fin_de_ligne), de l'interdiction du `goto`, ou encore du strict respect des règles [MISRA](https://fr.wikipedia.org/wiki/MISRA_C).

Ces "guerres de croyances", qui perdurent parfois depuis des générations, se nourrissent d’un manque d’ouverture d’esprit et d’un attachement dogmatique à des habitudes. Cela s’explique souvent par le biais d’[ancrage mental](https://fr.wikipedia.org/wiki/Ancrage_(psychologie)) qui s’installe dès l’école, là où l'on inculque parfois des certitudes figées.

L'enseignant se doit d'être sensible à ces questions et doit encourager l'impartialité, ainsi qu'un état d'esprit ouvert, guidé par le bon sens de l'ingénieur.

Un exemple célèbre est celui des [guerres d'éditeurs](https://fr.wikipedia.org/wiki/Guerre_d%27%C3%A9diteurs) qui opposent, depuis les années 1970, les adeptes de `vi` aux fervents défenseurs d'`emacs`. Ces deux éditeurs de texte, extrêmement puissants et complexes à maîtriser, polarisent les opinions de manière radicale. Ces guerres, entretenues à l'origine par un esprit de plaisanterie, ont progressivement pris une tournure émotionnelle qui dépasse parfois le simple cadre de l'outil.

S’enfermer dans une zone de confort renforce le biais du [Marteau de Maslow](https://everlaab.com/marteau-de-maslow/), car lorsqu'on est un marteau, on finit par voir tous les problèmes comme des clous. Ce confort devient alors un ennemi qui freine le regard critique et le pragmatisme, pourtant essentiels. Il faut accepter l’existence de diverses approches pour résoudre un problème donné, car le développement logiciel, plus que tout autre domaine technique, est une aventure collaborative qui ne devrait jamais être soumise à des emprises émotionnelles.

Un programme se doit d'être **neutre**, **impartial**, et **minimaliste**. L’essentiel n’est pas de s'attarder sur des questions esthétiques comme la position des accolades, l’utilisation d'espaces ou de tabulations, ou le choix d’un éditeur sur un autre.

La clé de la bonne attitude c'est d'être à l'écoute du consensus et de ne pas sombrer au [biais d'attention](https://fr.wikipedia.org/wiki/Biais_d%27attention). Il faut non seulement être sensible au consensus local direct: son entreprise, son école, son équipe de travail, mais surtout au consensus planétaire dont l'accès ne peut se faire que par l'interaction directe avec la communauté de développeurs, soit par les forums de discussions (Reddit, stackoverflow), soit par le code lui-même. Vous avez un doute sur la bonne méthode pour écrire tel algorithme ou sur la façon dont votre programme devrait être structuré ? Plongez-vous dans le code des autres, multipliez vos expériences, observez les disparités et les oppositions, et apprenez à ne pas y être sensible.

Vous verrez qu'au début, un programme ne vous semble lisible que s'il respecte vos habitudes, la taille de vos indentations préférées, la police de caractère qui vous sied le mieux, l'éditeur qui supporte les ligatures...

Par la suite, et à la relecture de cette section, vous apprendrez à faire fi de cette zone de confort qui vous était si cher et que l'important n'est plus la forme, mais le fond. Vous aurez comme [Néo](https://fr.wikipedia.org/wiki/Neo_(Matrix)), libéré votre esprit et serez capable de voir la matrice sans filtre ni biais.

En somme, restez ouvert aux autres points de vue, cherchez à adopter le consensus majoritaire qui dynamise au mieux votre équipe de développement, qui s'encadre le mieux dans votre stratégie de croissance et de collaboration et surtout, abreuvez-vous de code, faites-en des indigestions, rêvez-en la nuit. Vous tradez du Bitcoin, allez lire [le code source](https://github.com/bitcoin/bitcoin), vous aimez Linux, plongez-vous dans le code source du [kernel](https://github.com/torvalds/linux), certains collègues ou amis vous ont parlé de Git, allez voir ses [entrailles](https://github.com/git/git)... Oui, tous ces projets sont écrits en C, n'est-ce pas merveilleux ?

## L'open source

Au début de l'informatique, les programmes étaient distribués avec leur code source, car les ordinateurs étaient rares et coûteux et que les utilisateurs étaient souvent des développeurs. Avec l'arrivée des ordinateurs personnels, les éditeurs de logiciels ont commencé à distribuer des programmes compilés, car les utilisateurs n'étaient plus des développeurs et que le code source était devenu un secret industriel monétisable. C'est ainsi que le logiciel propriétaire est né. Les éditeurs de logiciels ont tiré parti de cette situation pour verrouiller leurs clients dans un écosystème propriétaire, les empêchant de modifier le logiciel, de le partager ou de le vendre.

Dans les années 1980, Richard Stallman, un informaticien américain, a lancé le projet GNU pour créer un système d'exploitation libre, c'est-à-dire un système d'exploitation dont le code source est librement accessible, modifiable et redistribuable. Néanmoins la licence GPL (GNU Public License) qui protège le code source de GNU est très contraignante et ne permet pas de créer des logiciels propriétaires basés sur du code source GPL. C'est un frein pour les entreprises qui souhaitent protéger leur propriété intellectuelle.

En 1991, Linus Torvalds, un étudiant finlandais, a créé le noyau Linux, qui est devenu le noyau du système d'exploitation GNU/Linux. Depuis lors, de nombreux logiciels libres ont été développés, notamment le navigateur web Firefox, le serveur web Apache, le système de gestion de base de données MySQL, le langage de programmation Python, le système de gestion de versions Git, etc.

Cette philosophie du logiciel libre a été popularisée par le hacker américain Eric Raymond dans son essai "La cathédrale et le bazar" qui décrit deux modèles de développement logiciel : le modèle de la cathédrale, où le code source est développé en interne par une équipe restreinte, et le modèle du bazar, où le code source est développé de manière collaborative par une communauté de développeurs.

L'expression *open source* s'est largement imposée dans le monde de l'informatique pour désigner les logiciels libres, car elle est plus neutre et moins idéologique que l'expression *logiciel libre*. De grandes sociétés comme Google, Facebook, Microsoft, IBM, Oracle, etc., ont adopté la philosophie du logiciel libre et contribuent activement à de nombreux projets open source. Par exemple, Google a développé le système d'exploitation Android, qui est basé sur le noyau Linux, et qui est utilisé par la plupart des smartphones dans le monde. Facebook a développé le framework React, qui est utilisé par de nombreux sites web pour créer des interfaces utilisateur interactives. Microsoft a racheté GitHub, la plateforme de développement collaboratif la plus populaire au monde, et a ouvert le code source de nombreux projets, notamment le framework .NET. IBM a racheté Red Hat, l'éditeur de la distribution Linux Red Hat Enterprise Linux, et contribue activement à de nombreux projets open source.

Mettre un logiciel ou une partie de logiciel en open source c'est permettre à d'autres développeurs de contribuer au projet, de corriger des bogues, d'ajouter des fonctionnalités, de traduire le logiciel dans d'autres langues, etc. C'est aussi un moyen de faire connaître son travail, de se faire un nom dans la communauté des développeurs, de trouver un emploi, de créer une entreprise, etc. Mais c'est aussi un moyen de partager ses connaissances, de contribuer à l'éducation, à la recherche, à la culture, à l'humanité.

L'open source est devenu un modèle économique viable pour de nombreuses entreprises, qui vendent des services autour de logiciels open source, comme le support, la formation, la personnalisation, l'hébergement, etc. C'est aussi un moyen de réduire les coûts de développement, de mutualiser les efforts, de partager les risques, de favoriser l'innovation et de promouvoir la transparence.

Pourquoi ne pas faire d'open source ? C'est une question que vous vous poserez tôt ou tard dans votre carrière de développeur. Vous avez peut-être peur de la concurrence, de la critique, du piratage, de la perte de contrôle, de la complexité, de l'engagement, de la responsabilité, de la réputation, de la légalité, de la sécurité, de la confidentialité, de la propriété intellectuelle, etc. De nombreuses sociétés ont fait le choix de protéger leur propriété intellectuelle en gardant leur code source secret, mais cela à un coût. Les logiciels doivent être protégés par des licences, des brevets, le code doit être crypté, les serveurs doivent être sécurisés, les employés doivent être surveillés, les clients doivent être contrôlés, etc. C'est un cercle vicieux qui peut conduire à la paranoïa, à la méfiance.

## La communauté

Se passionner pour le développement logiciel c'est aussi se passionner pour la communauté des développeurs. Avant internet, les développeurs se rencontraient dans des clubs d'informatique, des associations d'utilisateurs, des conférences, des salons, des formations, des hackathons, des meetups, etc. Moi-même, à douze ans, je suis rentré au Mac Club de Genève. Un club d'informatique pour les passionnés de Macintosh. J'ai fait mes premiers pas sur internet avec des modem rudimentaires.

Avec internet, les développeurs se rencontrent maintenant sur des forums (Stack Overflow, Reddit...), des listes de diffusion, des chats, des blogs, des réseaux sociaux, des plateformes de développement collaboratif, etc.

GitHub a été créé en 2008 par Tom Preston-Werner, Chris Wanstrath, PJ Hyett et Scott Chacon pour faciliter le développement collaboratif de logiciels open source. GitHub est devenu la plateforme de développement collaboratif la plus populaire au monde, avec plus de 100 millions de dépôts de code source, plus de 40 millions de développeurs. On y trouve de tout, il suffit de chercher.

Pour les questions techniques, il y a Stack Overflow, un site de questions-réponses créé en 2008 par Jeff Atwood et Joël Spolsky. Stack Overflow est devenu le site de questions-réponses le plus populaire au monde, avec plus de 10 millions de questions, plus de 20 millions de réponses, plus de 10 millions de membres. Je vous encourage personnellement à y contribuer, cela commence par créer un compte, poser des questions, répondre à des questions, voter pour des questions, voter pour des réponses.

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

Enfin, je voudrais terminer cette introduction par un point essentiel du développement logiciel : la revue de code, qui est trop souvent négligée.

La revue de code est une pratique essentielle pour améliorer la qualité du code source, la productivité des développeurs, la sécurité des logiciels, la satisfaction des clients. La revue de code consiste à examiner le code source d'un développeur par un autre développeur pour détecter des erreurs, des anomalies, des incohérences, des inefficacités, des non-conformités, des risques, des opportunités. La revue de code peut être formelle ou informelle, manuelle ou automatique, individuelle ou collective, interne ou externe, systématique ou aléatoire, planifiée ou impromptue, etc.

Dans les entreprises c'est un des plus gros problèmes. Les développeurs n'aiment pas qu'on critique leur code, les chefs de projet n'aiment pas perdre du temps à examiner le code, les clients n'aiment pas payer pour la revue de code, les managers n'aiment pas les conflits entre développeurs, les commerciaux n'aiment pas les retards de livraison, les juristes n'aiment pas les risques de litige. Les gens manquent d'humilité et d'ouverture d'esprit. Pourtant, s'ouvrir à la critique, cela permet de s'améliorer et d'apprendre.

## Conclusion

En résumé, devenir développeur logiciel, que ce soit en tant que professionnel ou par passion, est bien plus qu’une simple question d'écriture de code. C'est un art qui demande une compréhension profonde des principes, des bonnes pratiques et des valeurs fondamentales qui régissent cette discipline en constante évolution. Trop souvent, les dogmes académiques et les habitudes obsolètes polluent l'apprentissage et la pratique, au détriment de l'esprit collaboratif et critique indispensable à la réussite dans ce domaine.

Le développement logiciel ne repose pas sur des acquis immuables, mais sur des principes adaptatifs et des valeurs humaines intemporelles telles que l'ouverture d'esprit, l'humilité, la curiosité, la rigueur, la patience, la persévérance, l'écoute, l'entraide et le partage. Ces valeurs, qui ont permis à l'humanité de prospérer, sont tout aussi essentielles dans le monde du développement logiciel.

Il est crucial de comprendre que le code que vous écrivez aujourd'hui doit pouvoir être compris, maintenu et évolué par d'autres demain. Ainsi, il doit respecter les standards de l'entreprise, les conventions de codage, les bonnes pratiques et les règles de sécurité. Cela nécessite un engagement envers des méthodes de travail éprouvées, mais aussi une attitude de remise en question constante et d'ouverture à l'innovation.

L'anglais, langue universelle de la programmation, est un outil indispensable pour naviguer dans cet univers globalisé. Il permet de partager des connaissances, d'accéder à des ressources et de collaborer avec des développeurs du monde entier. Ne sous-estimez pas l'importance de maîtriser cette langue pour votre carrière.

Apprendre à pêcher plutôt qu'à se faire donner du poisson est une leçon clé dans l'apprentissage du développement logiciel. La pratique, la persévérance et l'expérimentation personnelle sont indispensables pour acquérir les compétences nécessaires et devenir autonomes.

L'informatique est aussi une affaire de consensus. Les guerres de croyances et les dogmes ne font que limiter la croissance et l'innovation. Adopter une attitude pragmatique et ouverte, en se basant sur le consensus de la communauté mondiale des développeurs, est essentiel pour progresser et s'épanouir dans ce métier.

L'open source incarne parfaitement l'esprit de partage et de collaboration qui est au cœur du développement logiciel. Il permet non seulement de contribuer à des projets d'envergure mondiale, mais aussi de se faire un nom, d'apprendre des autres et de donner en retour.

Enfin, la communauté des développeurs est une ressource inestimable. Participer activement à des forums, des plateformes collaboratives, des conférences et des meetups enrichit non seulement vos compétences, mais aussi votre réseau professionnel.
