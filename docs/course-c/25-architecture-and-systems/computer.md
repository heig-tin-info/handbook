# L'ordinateur personnel

Un ordinateur personnel ([[PC]] pour *Personal Computer*) est un appareil électronique de format relativement compact destiné à un usage individuel ou familial. Il se distingue des ordinateurs centraux (ou *mainframes*) et des serveurs, plutôt réservés à des tâches professionnelles ou collectives, souvent en raison de leur coût élevé et de leur encombrement. Quelle que soit la taille de la machine, ses composants essentiels demeurent pourtant identiques. On retrouve ainsi plusieurs éléments principaux :

Un **processeur** (ou **[[CPU]]** pour *Central Processing Unit*)

: Il constitue le cœur de calcul de l'ordinateur. Le processeur exécute les instructions des programmes et coordonne l'activité des autres composants matériels.

La **mémoire** (ou **[[RAM]]** pour *Random Access Memory*)

: Cette mémoire est **volatile**, c'est-à-dire qu'elle perd son contenu lorsque l'ordinateur est éteint, mais elle offre un accès extrêmement rapide. Elle stocke temporairement les données des programmes en cours d'exécution.

Un **disque dur** (ou **[[HDD]]** pour *Hard Disk Drive*)

: Il assure le stockage de masse et conserve les données de manière persistante entre deux mises sous tension.

Une **carte graphique** (ou **[[GPU]]**)

: Elle gère l'affichage des images à l'écran ainsi que les calculs 3D. Aujourd'hui, elle contribue également à accélérer les traitements parallèles, notamment pour l'entraînement des modèles de langage.

Une **carte mère** (*motherboard*)

: Elle relie entre eux l'ensemble des composants physiques de l'ordinateur et assure leur alimentation.

Un **chipset**

: Cet ensemble de circuits électroniques orchestre les communications entre les différents composants. Historiquement, il se divisait en deux parties : le **Northbridge** et le **Southbridge**.

![Architecture d'un ordinateur](/assets/images/pc-architecture.drawio)

## La RAM

La [[mémoire vive]] est une mémoire de stockage temporaire ; on la qualifie parfois de mémoire non permanente. Le plus souvent, une barrette de mémoire est amovible et vient s'insérer directement sur la carte mère. Avec l'évolution de la technologie, ces modules sont carénés et munis d'un dissipateur thermique.

![2 x 16 GB DDR5 DIMM Corsair Vengeance](/assets/images/sdram-corsair-vengeance.avif){ width=50% }

Sous le capot, on peut voir les puces de mémoire:

![Crucial DDR4 16 GB](/assets/images/sdram.webp){ width=50% }

Cette barrette offre 16 Gibioctets de capacité, soit $16 \times 2^30 = 17\,179\,869\,184$ octets. Chaque octet étant composé de $8$ bits, on obtient $17\,179\,869\,184 \times 8 = 137\,438\,953\,472$ bits. Comme nous observons $4$ puces de mémoire, chacune d'elles contient donc $4$ Gibioctets.

Généralement, ces mémoires sont vendues en nombre de bits, soit ici 32 Gibibits.

Sur le circuit électronique, ou PCB (*Printed Circuit Board*), on distingue nettement les quatre puces de mémoire soudées. Le modèle présenté provient de la société Micron et porte la référence MT40A1G8.

Une mémoire volatile perd son contenu dès qu'elle n'est plus alimentée en électricité. La raison est simple : stocker un état électrique requiert de l'énergie afin d'accumuler des charges. Si l'on compare l'électricité à de l'eau, chaque bit de la mémoire devient un verre que l'on peut remplir ou vider. Pour connaître l'état du verre, il faut vérifier la présence d'eau, c'est-à-dire le vider. Plus le verre est grand, plus le temps nécessaire pour le remplir ou le vider augmente, ce qui engendre plusieurs inconvénients :

1. La vitesse de lecture est plus lente.
2. La quantité d'eau (courant) pour remplir le verre est plus grande.
3. L'encombrement est plus grand puisque le verre est plus volumineux.

Le choix technologique consiste donc à réduire la taille des verres. Ils deviennent si petits que l'eau qu'ils contiennent s'évapore très vite. Pour éviter la perte d'information, il faut les remplir en permanence : c'est l'opération de *rafraîchissement* de la mémoire. En pratique, environ toutes les 64 ms, le contrôleur réécrit automatiquement le contenu pour préserver les données ; cette opération reste transparente pour l'utilisatrice ou l'utilisateur.

Les caractéristiques de la mémoire sont les suivantes:

| Caractéristique           | Valeur | Unité |
| ------------------------- | ------ | ----- |
| Capacité                  | 32     | Gib   |
| Tension d'alimentation    | 1.2    | V     |
| Fréquence                 | 1600   | MHz   |
| Temps de rafraîchissement | 64     | ms    |
| Nombre de banques         | 16     |       |
| Technologie               | DDR4   |       |

### Technologies

Il existe plusieurs technologies de mémoire vive. Les plus courantes sont : SDRAM, DDR, DDR2, DDR3 et DDR4. Contrairement à la SDRAM, qui est une mémoire synchrone, les mémoires DDR (*Double Data Rate*) fonctionnent de manière asynchrone. Elles peuvent lire et écrire des données sur les flancs montant et descendant du signal d'horloge, ce qui double la bande passante disponible. À chaque génération, les performances progressent grâce à une fréquence plus élevée, à une densité accrue des puces et à une réduction de la tension d'alimentation.

[](){#light-speed}
### Vitesse de la lumière

![Autoroute de l'information](/assets/images/highway.png)

La vitesse de la lumière est de 299 792 458 m/s, valeur fixée par la définition du mètre. Il s'agit de la vitesse maximale atteignable dans l'univers. Pour donner un ordre de grandeur, un signal électrique se propage dans un câble à environ deux tiers de cette vitesse. Parcourir un mètre lui demande donc près de 5 ns.

Plus haut, nous avons vu que le bus de données de la mémoire est souvent large de 64 bits. On peut le comparer à une autoroute à 64 voies présentant toutefois quelques contraintes :

- Les voies sont unidirectionnelles : on ne circule que dans un sens.
- Les voies sont séparées par des barrières : impossible de changer de voie en cours de route.
- Les véhicules se déplacent à environ 540 millions de km/h et ne peuvent ni freiner, ni accélérer, ni s'arrêter.

Pour transmettre une information — par exemple un entier de 64 bits (`long long` en C) — il faut faire entrer un véhicule sur chacune des 64 voies. Chaque véhicule représente un bit. Pour que le message soit transmis correctement, les 64 véhicules doivent être alignés et atteindre la destination simultanément.

Sur la figure suivante, on voit le routage d'un circuit électronique. En rose, ce sont les composants physiques. À gauche un processeur et au milieu en bas deux circuits mémoire labélisés *DDR1* et *DDR2*. En bleu clair ce sont les lignes électriques qui relient les composants. On observe des tas de petites circonvolutions. Les lignes sont artificiellement rallongées pour que la longueur de chaque voie de l'autoroute soit la même, afin de garantir une vitesse de propagation identique pour chaque ligne de donnée.

![Routage d'une mémoire](/assets/images/sdram-layout.png)

Vous me direz, oui, mais 540 millions de km/h c'est super rapide et sur ce circuit les lignes ne font pas plus de 10 cm ce qui représente 600 ps pour parcourir la distance. Oui, mais voilà, on communique sur cette autoroute à 2000 MT/s (mégatransferts par seconde). Cela signifie que 2'000'000 de véhicules entrent sur chaque voie de l'autoroute chaque seconde. N'est-ce pas incroyable?

Malgré ces performances, la mémoire reste un goulot d'étranglement pour les processeurs. En effet, les processeurs sont de plus en plus rapides et les mémoires ne suivent pas le rythme. Un processeur qui calcule à 4 GHz peut exécuter 4 milliards d'instructions par seconde. Si chaque instruction nécessite un accès mémoire et que cet accès prend 100 cycles d'horloge, alors le processeur ne pourra exécuter que 40 millions d'instructions par seconde. Cela signifie que le processeur ne sera utilisé qu'à 1% de sa capacité.

## Le disque dur

![Disque dur](/assets/images/hdd.jpg)

Le disque dur est un dispositif de [[stockage de masse]]. Il se compose de plusieurs plateaux métalliques qui tournent à grande vitesse. Un bras mécanique se déplace au-dessus des surfaces magnétiques pour lire ou écrire les données. Comparés à la mémoire vive, les disques durs demeurent lents, mais ils sont privilégiés pour conserver les données de manière durable.

De nos jours, ils sont progressivement supplantés par des disques SSD (*Solid State Drive*) plus rapides et plus fiables. Les SSD reposent sur de la mémoire flash et ne contiennent aucune pièce mobile. Contrairement à la mémoire vive, il s'agit d'une mémoire non volatile : les données restent disponibles même lorsque l'alimentation est coupée.

![SSD de 2 TiB](/assets/images/ssd-990pro.avif){ width=50% }

On pourrait se demander pourquoi les SSD, capables de stocker beaucoup plus de données dans un volume identique, restent plus lents que la mémoire vive. La réponse tient à leur organisation interne en blocs, appelés *pages* et *clusters*. Pour lire ou écrire une donnée, il faut manipuler tout le bloc. Autrement dit, pour accéder à un seul octet, il est nécessaire de transférer 4'096 octets : c'est la notion de *page size*.

![Évolution du prix des HDD et SSD](/assets/images/ssd-hdd-price.drawio)

La communication entre le processeur et un disque SSD ou HDD passe par un protocole série appelé *SATA* (*Serial ATA*). Il autorise un débit maximal de 6 Gbit/s. Transférer un octet nécessite donc 8 bits, soit 8 ns. Cela paraît rapide, mais lire un bloc de 4'096 octets impose d'acheminer 32'768 bits, donc 32'768 × 8 ns = 262'144 ns, c'est-à-dire 262 µs. On se retrouve alors avec un temps d'accès 262'144 fois plus élevé que celui de la mémoire vive.

Pour interfacer le processeur avec le disque, on recourt à un contrôleur dédié. Ce circuit électronique pilote les accès disque et intègre généralement un microprocesseur, de la mémoire vive et de la mémoire flash.

## La carte mère

![Carte mère](/assets/images/motherboard.webp){ width=50% }

La carte mère constitue l'épine dorsale de l'ordinateur. Elle relie tous les composants entre eux grâce à un circuit imprimé sur lequel sont soudés les éléments actifs et une multitude de connecteurs.

Au centre de la carte mère se trouve le **chipset**, un ensemble de circuits électroniques qui gèrent les communications entre les différents composants. Historiquement, il se décomposait en deux parties : le *northbridge*, chargé des échanges entre processeur et mémoire vive, et le *southbridge*, responsable des périphériques de stockage et des ports USB. Depuis plusieurs années, le contrôleur mémoire est intégré au processeur et le chipset se rapproche d'un *southbridge* amélioré.

Le **chipset** est relié au processeur par un bus de données appelé **FSB** (*Front Side Bus*), qui assure la circulation des informations entre ces deux composants. Sa configuration est stockée dans une mémoire flash appelée **BIOS** (*Basic Input/Output System*), un logiciel qui permet de définir les paramètres de la carte mère.

Pendant longtemps, le BIOS proposait une interface très minimaliste : on le configurait au clavier sur un écran monochrome ne présentant que des caractères.

Aujourd'hui, le BIOS cède la place à l'**UEFI** (*Unified Extensible Firmware Interface*), un logiciel plus évolué qui offre une interface graphique. On peut désormais configurer la carte mère à la souris, voire au doigt sur un écran tactile.

## Le processeur

Le processeur fait figure de cerveau de l'ordinateur : il exécute les instructions des programmes. La figure suivante présente un processeur Intel i7-12700K au format LGA 1700, c'est-à-dire muni de 1 700 contacts pour se fixer sur la carte mère.

![Processeur Intel i7](/assets/images/cpu-i7.png)

Sur les 1 700 broches, on distingue plusieurs familles :

- Les broches d'alimentation représentent 40 à 60 % de l'ensemble et fournissent au processeur une tension d'environ 1,2 V.
- Le contrôleur mémoire (DDR4/DDR5) relie la mémoire vive au processeur et mobilise environ 5 à 15 % des broches.
- Les interfaces PCIe accueillent des cartes d'extension (graphique, réseau, son, etc.). Ce processeur gère jusqu'à 20 lignes différentielles, soit 40 broches.
- L'accès DMI constitue l'interface entre processeur et chipset. Un lien DMI 4.0 ×8 s'appuie sur 8 lignes (Rx/Tx), soit environ 16 broches.
- L'USB requiert quelques dizaines de broches supplémentaires.
- Le contrôleur graphique intégré (iGPU) expose des ports HDMI ou DisplayPort pour relier directement un écran au processeur.
- Des interconnexions spécifiques (I2C, SPI, etc.) complètent l'ensemble.

Si l'on consulte le SDM (*Software Developer Manual*) d'Intel, un document de 5 000 pages, on y découvre une foule d'informations passionnantes. Le chapitre consacré aux types numériques présente, par exemple, les différentes tailles d'entiers (`byte`, `word`, `dword`, `qword`), de flottants (`half`, `single`, `double`, `extended`) et de vecteurs (`xmm`, `ymm`, `zmm`, `kmm`). On y apprend que le processeur utilise le complément à deux pour les entiers et la norme IEEE 754 pour les flottants, qu'il fonctionne en *little-endian* et que ses registres sont larges de 64 bits. Le langage C demeure ainsi très proche de l'assembleur du processeur.

## Chipset

![Chipset](/assets/images/chipset-cpu.drawio)
