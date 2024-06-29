# La programmation

![L'un des premiers ordinateurs: l'Eniac](../assets/images/eniac.jpg)

Il ne serait pas raisonnable de vous enseigner la programmation C sans au préalable définir ce qu'est la programmation et quelle est son origine. La programmation intervient après une étape plus générale impliquant un ou plusieurs algorithmes.

**Algorithmique et Programmation**, il y donc deux questions à éclaircir :

1. Qu'est-ce que l'algorithmique ?
2. Qu'est-ce que la programmation ?

## Algorithmique

L'algorithmique et non l'*algorithmie*, est la science qui étudie la production de règles et techniques impliquées dans la définition et la conception d'[algorithmes](https://fr.wikipedia.org/wiki/Algorithme). Nous verrons l'algorithmique plus en détail dans le chapitre {numref}`algorithms`. Retenons pour l'heure que l'algorithmique intervient tous les jours :

- dans une recette de cuisine,
- le tissage de tapis persans,
- les casse-tête ([Rubik's Cube](https://fr.wikipedia.org/wiki/Rubik%27s_Cube)),
- les tactiques sportives,
- les procédures administratives.

Dans le contexte mathématique et scientifique qui nous intéresse ici, citons l'[algorithme d'Euclide](https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide) datant probablement de 300 av. J.-C. est un algorithme permettant de déterminer le [plus grand commun diviseur](https://fr.wikipedia.org/wiki/Plus_grand_commun_diviseur) (PGCD). Voici la description de l'algorithme :


![Algorithme de calcul du PGCD d'Euclide.](../assets/figures/dist/algorithm/euclide-gcd.svg)


!!! exercise "Algorithme d'Euclide"

    Appliquer l'algorithme d'Euclide aux entrées suivantes. Que vaut $a$
    , $b$ et $r$ ?

    $$a = 1260, b = 630$$


## Programmation

La machine Jacquard est un [métier à tisser](https://fr.wikipedia.org/wiki/M%C3%A9tier_%C3%A0_tisser) mis au point par Joseph Marie Jacquard en 1801. Il constitue le premier système mécanique programmable avec cartes perforées.

![Mécanisme Jacquard au Musée des arts et métiers de Paris.](../assets/images/loom.jpg){ width="80%" }


Les cartes perforées contiennent donc la suite des actions guidant les crochets permettant de tisser des motifs complexes. L'automatisation d'un travail qui jadis était effectué manuellement causa une vague de chômage menant à la [Révolte des canuts](https://fr.wikipedia.org/wiki/R%C3%A9volte_des_canuts) en 1831.

La [programmation](https://fr.wikipedia.org/wiki/Programmation_informatique) définit toute activité menant à l'écriture de programmes. En informatique, un programme est un ensemble ordonné d'instructions codées avec un langage donné et décrivant les étapes menant à la solution d'un problème. Il s'agit le plus souvent d'une écriture formelle d'un algorithme.
```

Les informaticiens-tisserands responsables de la création des cartes perforées auraient pu se poser la question de comment simplifier leur travail en créant un langage formel pour créer des motifs complexes et dont les composants de base se répètent d'un travail à l'autre. Prenons l'exemple d'un ouvrier spécialisé en [héraldique](https://fr.wikipedia.org/wiki/H%C3%A9raldique) et devant créer des motifs complexes de blasons. Nul n'est sans savoir que l'héraldique a son langage parfois obscur et celui qui le maîtrise voudrait par exemple l'utiliser au lieu de manuellement percer les cartes pour chaque point de couture. Ainsi l'anachronique informaticien-tisserand souhaitant tisser le motif des armoiries duc de Mayenne (c.f. figure ci-dessous) aurait sans doute rédigé un programme informatique en utilisant sa langue. Le programme aurait pu ressembler à ceci :

```text
Écartelé, en 1 et 4 :
    coupé et parti en 3,
        au premier fascé de gueules et d'argent,
        au deuxième d'azur semé de lys d'or
            et au lambel de gueules,
        au troisième d'argent à la croix potencée d'or,
            cantonnée de quatre croisettes du même,
        au quatrième d'or aux quatre pals de gueules,
        au cinquième d'azur semé de lys d'or
            et à la bordure de gueules,
        au sixième d'azur au lion contourné d'or,
            armé,
            lampassé et couronné de gueules,
        au septième d'or au lion de sable,
            armé,
            lampassé de gueules,
        au huitième d'azur semé de croisettes d'or
            et aux deux bar d'or.
    Sur le tout d'or à la bande de gueules
        chargé de trois alérions d'argent
    le tout brisé d'un lambel de gueules ;
        en 2 et 3 contre-écartelé en 1 et 4 d'azur,
        à l'aigle d'argent, becquée,
        languée et couronnée d'or et en 2 et 3 d'azur,
        à trois fleurs de lys d'or,
        à la bordure endentée de gueules et d'or.
```


Notons que *de gueules* signifie *rouge*. Le [drapeau suisse](https://fr.wikipedia.org/wiki/Drapeau_et_armoiries_de_la_Suisse) est donc *de gueules, à la croix alésée d'argent*.

![Armoiries des ducs de Mayenne](../assets/images/armoiries.svg){ width="200px" }

## Calculateur

Un calculateur du latin *calculare*: calculer avec des cailloux, originellement appelé [abaque](<https://fr.wikipedia.org/wiki/Abaque_(calcul)>) était un dispositif permettant de faciliter les calculs mathématiques.

Les [os d'Ishango](https://fr.wikipedia.org/wiki/Os_d%27Ishango) datés de 20'000 ans sont des artéfacts archéologiques attestant la pratique de l'arithmétique dans l'histoire de l'humanité.

Si les anglophones ont détourné le verbe *compute* (calculer) en un nom *computer*, un ordinateur est généralement plus qu'un simple calculateur, car même une calculatrice de poche doit gérer en plus des calculs :

- l'interface de saisie (pavé numérique);
- l'affichage du résultat (écran à cristaux liquide).


## Ordinateur

Le terme ordinateur est très récent, il daterait de 1955, créé par Jacques Perret à la demande d'IBM France (c.f [2014: 100 ans d'IBM en France](http://centenaireibmfrance.blogspot.com/2014/04/1955-terme-ordinateur-invente-par-jacques-perret.html)).

> « Le 16 IV 1955
> Cher Monsieur,
> Que diriez-vous d’ordinateur? C’est un mot correctement formé, qui se trouve même dans le Littré comme adjectif désignant Dieu qui met de l’ordre dans le monde. Un mot de ce genre a l’avantage de donner aisément un verbe ordiner, un nom d’action ordination. L’inconvénient est que ordination désigne une cérémonie religieuse ; mais les deux champs de signification (religion et comptabilité) sont si éloignés et la cérémonie d’ordination connut, je crois, de si peu de personnes que l’inconvénient est peut-être mineur. D’ailleurs votre machine serait ordinateur (et non-ordination) et ce mot est tout à fait sorti de l’usage théologique. Systémateur serait un néologisme, mais qui ne me paraît pas offensant ; il permet systématisé ; — mais système ne me semble guère utilisable — Combinateur a l’inconvénient du sens péjoratif de combine ; combiner est usuel donc peu capable de devenir technique ; combination ne me paraît guère viable à cause de la proximité de combinaison. Mais les Allemands ont bien leurs combinats (sorte de trusts, je crois), si bien que le mot aurait peut-être des possibilités autres que celles qu’évoque combine.
>
> Congesteur, digesteur évoquent trop congestion et digestion. Synthétiseur ne me paraît pas un mot assez neuf pour désigner un objet spécifique, déterminé comme votre machine.
>
> En relisant les brochures que vous m’avez données, je vois que plusieurs de vos appareils sont désignés par des noms d’agent féminins (trieuse, tabulatrice). Ordinatrice serait parfaitement possible et aurait même l’avantage de séparer plus encore votre machine du vocabulaire de la théologie. Il y a possibilité aussi d’ajouter à un nom d’agent un complément : ordinatrice d’éléments complexes ou un élément de composition, par exemple : sélecto-systémateur. Sélecto-ordinateur a l’inconvénient de deux o en hiatus, comme électro-ordonnatrice.
>
> Il me semble que je pencherais pour ordonnatrice électronique. Je souhaite que ces suggestions stimulent, orientent vos propres facultés d’invention. N’hésitez pas à me donner un coup de téléphone si vous avez une idée qui vous paraisse requérir l’avis d’un philologue.
>
> Vôtre
> Jacques Perret »

## Historique

87 av. J.-C.

: La [machine d'Anticythère](https://fr.wikipedia.org/wiki/Machine_d%27Anticyth%C3%A8re) considéré comme le premier calculateur analogique pour positions astronomiques.

1642

: [La pascaline](https://fr.wikipedia.org/wiki/Pascaline): machine d'arithmétique de Blaise Pascal, première machine à calculer


1834

: Machine à calculer programmable de Charles Babbage


1937

: l'[Automatic Sequence Controlled Calculator Mark I](https://fr.wikipedia.org/wiki/Harvard_Mark_I) d'IBM, le premier grand calculateur numérique.

  - 4500 kg
  - 6 secondes par multiplication à 23 chiffres décimaux
  - Cartes perforées


1950

: L'ENIAC, de Presper Eckert et John William Mauchly

  - 160 kW
  - 100 kHz
  - Tubes à vide
  - 100'000 additions/seconde
  - 357 multiplications/seconde



1965

: Premier ordinateur à circuits intégrés, le [PDP-8](https://fr.wikipedia.org/wiki/PDP-8)

  - 12 bits
  - mémoire de 4096 mots
  - Temps de cycle de 1.5 µs
  - [Fortran](https://fr.wikipedia.org/wiki/Fortran) et BASIC



2018

: Le [Behold Summit](<https://fr.wikipedia.org/wiki/Summit_(superordinateur)>) est un superordinateur construit par IBM.

  - 200'000'000'000'000'000 multiplications par seconde
  - simple ou double précision
  - 14.668 GFlops/watt
  - 600 GiB de mémoire RAM
