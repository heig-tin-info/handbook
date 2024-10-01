# Microcontrôleur

## Introduction

Un microcontrôleur est un ordinateur sur une puce. Il est composé d'un processeur, de mémoire et de périphériques d'entrée/sortie. Les microcontrôleurs sont utilisés dans de nombreux systèmes embarqués, tels que les télécommandes, les jouets, les appareils électroménagers, les instruments de mesure, les systèmes de contrôle de moteurs etc. Nous avons déjà évoqué la [machine à café][coffee-maker] en début de cours qui est un bon exemple de système embarqué.

## Style de programmation

D'ordinaire les petits microcontrôleurs sont programmés en langage C, néanmoins certaines possibilités du langage sont généralement prohibées. Par exemple, les pointeurs de fonction sont rarement utilisés, les fonctions récursives sont à proscrire, les allocations dynamiques de mémoire sont interdites, etc. Les microcontrôleurs ont des ressources limitées et le programmeur doit en tenir compte.

L'allocation dynamique est interdite car elle peut entraîner des fuites de mémoire ou de la fragmentation.

L'exécution du programme est très souvent dite [bare-metal](https://fr.wikipedia.org/wiki/Bare_metal), c'est-à-dire sans système d'exploitation. Le programme est exécuté directement sur le microcontrôleur sans aucune couche intermédiaire. Cela permet d'avoir un contrôle total sur le matériel. Mais cela rend le programme non préemptif, c'est-à-dire qu'il n'y a pas de gestionnaire de tâches qui peut interrompre le programme en cours d'exécution.

Prenons l'exemple d'une montre à aiguille équipée d'un microcontrôleur à ultra basse consommation comme le [Epson S1C17](https://global.epson.com/products_and_drivers/semicon/products/micro_controller/16bit/). Il ne serait pas raisonnable d'utiliser des boucles d'attentes actives (c'est-à-dire de compter un cerain nombre d'instructions correspondant à une seconde), au lieu de cela, il est préférable d'utiliser un timer pour réveiller le microcontrôleur toutes les secondes. Ce timer est un périphérique matériel qui génère une interruption toutes les secondes. L'interruption, via une table des vecteurs d'interruption, appelle une fonction qui met à jour l'affichage de la montre. Aussi, c'est principalement dans cette fonction qu'aura lieu la majorité du programme, et il n'est pas rare d'avoir un programme de cette forme:

```c
void timer_isr() {
    update_display();
    sleep(); // Suspend l'exécution du programme jusqu'à une interruption
}

int main() {
    init_device();
    init_timer(timer_isr);
    enable_low_power_mode();
    for(;;) {} // Boucle infinie
}
```

## Interruptions

Dans un système embarqué ou un microcontrôleur, une [[interruption]] est un mécanisme qui permet à un processeur de **suspendre temporairement l’exécution du programme en cours** afin de répondre à un événement particulier, souvent externe ou d'une urgence particulière. En d'autres termes, l'interruption interrompt le flux normal d'instructions pour traiter un événement prioritaire, comme si quelqu’un frappait à la porte pendant que vous lisez un livre captivant. Il faut alors poser le livre pour ouvrir la porte.

Voici comment cela se passe, étape par étape, de manière plus technique :

1. **Détection de l'événement** : Une interruption est déclenchée par un événement spécifique. Cela peut être, par exemple, l'appui sur un bouton, l'arrivée d'une donnée par un port série, ou encore une alarme temporelle. Ces événements sont surveillés en arrière-plan, pendant que le microcontrôleur poursuit normalement l'exécution de son programme, c'est à dire exécuter les instructions les unes après les autres.

2. **Suspension du programme principal** : Lorsqu'une interruption est détectée, le microcontrôleur interrompt son programme principal. Il mémorise l'endroit précis où il s’est arrêté (l’adresse de l’instruction suivante) dans une **pile** (ou *stack*). Cela permet de reprendre exactement là où il s'était arrêté une fois l’interruption gérée.

3. **Exécution de la routine d’interruption** : Après avoir suspendu l’exécution du programme principal, le microcontrôleur saute vers une fonction spéciale appelée **Routine de Service d’Interruption** ou **ISR** (*Interrupt Service Routine*). Cette routine est un petit programme dédié qui est conçu pour traiter l’événement en question. Par exemple, si un bouton a été pressé, l’ISR peut augmenter un compteur ou effectuer une autre action spécifique.

4. **Reprise du programme principal** : Une fois l’interruption traitée, le microcontrôleur restaure son état précédent grâce aux informations stockées dans la pile. Il reprend alors l’exécution du programme principal exactement là où il s'était arrêté, comme si de rien n'était.

### Pourquoi est-ce si utile ?

Les interruptions permettent au microcontrôleur de réagir **immédiatement** à des événements extérieurs sans avoir à constamment vérifier leur occurrence (ce que l’on appelle le *polling*, un processus inefficace et gourmand en ressources). Grâce aux interruptions, un microcontrôleur peut effectuer plusieurs tâches de manière efficace sans négliger aucun événement important.

Imaginons que vous devez surveiller en permanence si la pizza est cuite. Si l'algorithme est de faire pause après avoir dégommé 5 zombies à cet addictif jeu pour allez prendre connaissance de la cuisson, ce n'est pas efficace. Au contraire, en réglant un compte à rebours (*timer*) sur 10 minutes, il suffit de se laisser interrompre après le décompte...

### Les types d'interruptions

Il existe généralement deux types d'interruptions :

**Interruptions matérielles**

: Elles sont générées par des événements extérieurs au processeur, tels qu'un signal provenant d'un capteur, un bouton poussoir, ou une transmission de données par un périphérique. Dans un ordinateur personnel, les interruptions matérielles peuvent être générées par des périphériques tels que le clavier, la souris, le disque dur, etc.

**Interruptions logicielles**

: Ces interruptions sont générées par le programme lui-même, souvent pour organiser des tâches complexes ou pour indiquer qu’une certaine tâche est terminée. En C ABI on peut générer une interruption logicielle en utilisant l’instruction `raise(SIGINT)` par exemple.

### Un coût

Les interruptions ne sont pas gratuites. Elles ont un coût en termes de temps de traitement et de ressources. Lorsqu'une interruption se produit, le microcontrôleur doit :

1. sauver le contexte du processeur (tous les registres utilisés par C et l'état du programme) ;
2. sauver l'adresse de l'instruction suivante à exécuter ;
3. vider les pipelines d'instructions ;
4. exécuter la routine d'interruption ;
5. vider les pipelines d'instructions à nouveau ;
6. restaurer le contexte du processeur ;
7. reprendre l'exécution du programme principal.

Il est de coutume de dire qu'une interruption doit être la plus courte possible, mais une interruption d'une seule ligne de code en coûte déjà plusieurs dizaines.

Dans un contexte de microncontrôleur il n'est pas rare de devoir désactiver les interruptions pendant certaines opérations critiques, comme la modification d'une structure de données partagée entre l'ISR et le programme principal. Cela évite les problèmes de concurrence et de corruption de données. Il n'est pas rare non plus d'exécuter l'intégralité du programme dans une ISR.

Voici un exemple de code pour une montre à pile:

```c
struct clock {
    int hours;
    int minutes;
    int seconds;
} clock;

interrupt void timer_isr() {
    update_display(clock);
    if (++clock.seconds == 60) {
        clock.seconds = 0;
        if (++clock.minutes == 60) {
            clock.minutes = 0;
            if (++clock.hours == 24)
                clock.hours = 0;
        }
    }
    sleep();
}

int main() {
    init_device();
    init_timer(timer_isr, 1'000'000 /* us */);
    enable_low_power_mode();
    sleep(); // Suspend l'exécution du programme jusqu'à une interruption
    for(;;) {} // Boucle infinie
}
```

On observe d'une part l'utilisation d'un contexte global (variable globale) pour stocker l'heure, et d'autre part l'exécution de l'intégralité du programme dans l'ISR. Cela est possible car le programme est très simple et ne nécessite pas de traitement en dehors de l'ISR.

La variable globale est ici inévitable car il n'est généralement pas possible de passer des arguments à une ISR.

### Conclusion

Les interruptions sont une clé de voûte des systèmes embarqués modernes, leur permettant de traiter des événements en temps réel sans sacrifier les performances. Elles constituent une forme de gestion multitâche simplifiée, car elles donnent au microcontrôleur la capacité de suspendre son travail pour traiter un événement imprévu, puis de reprendre là où il s'était arrêté, un peu comme un pianiste capable d’interrompre son morceau pour répondre à une note inattendue, avant de reprendre son jeu avec la même fluidité.

Qu'il s'agisse de microcontrôleur, de système embarqué ou d'ordinateur personnel, les interruptions sont centrales pour garantir une réactivité et une efficacité maximales.

Si je devais conclure sur une note littéraire : les interruptions sont comme ces moments où la réalité frappe à la porte de la contemplation, exigeant une réponse immédiate et pressante, avant que la marche des choses ne reprenne son cours, inexorablement.

## Timers

Un *timer* est un **compteur interne** au microcontrôleur qui s’incrémente de manière régulière, en fonction d’un signal d’horloge. Ce signal d’horloge provient souvent d’un oscillateur externe, comme un [quartz](https://fr.wikipedia.org/wiki/Quartz_(%C3%A9lectronique)). Les timers sont utilisés pour mesurer le temps qui s’écoule, générer des intervalles précis ou déclencher des événements à des moments définis. En ce sens, ils sont un peu comme des horloges invisibles, comptant patiemment les cycles de l’oscillateur pour déclencher une action lorsque le moment est venu.

Dans un microcontrôleur, les oscillateurs ou quartz fournissent la cadence à laquelle toutes les opérations internes se déroulent. Ce sont eux qui dictent la fréquence à laquelle le microcontrôleur exécute ses instructions. Par exemple, un quartz de 16 MHz signifie que le microcontrôleur exécute des cycles d'horloge à la fréquence de 16 millions de fois par seconde.

En pratique cet oscillateur passe par une PLL (*Phase-Locked Loop*) qui permet de multiplier la fréquence de l'oscillateur pour obtenir une fréquence plus élevée. Un microcontrôleur avec un oscillateur de 20 MHz pourrait très bien être cadencé à 400 MHz.

Ceci étant, pour mesurer des intervalles de temps plus longs (comme une seconde, une milliseconde, etc.), un microcontrôleur a besoin de **compter** un certain nombre de ces cycles d'horloge. Le timer est donc ce mécanisme interne qui s'incrémente à chaque cycle d'horloge, et il peut être configuré pour déclencher une action après un certain nombre de cycles.

Imaginons que vous vouliez mesurer **une seconde** avec un microcontrôleur cadencé à **100 MHz**. Une seconde représente 100 millions de cycles. Un timer configuré pour s’incrémenter à chaque cycle d’horloge pourra compter jusqu’à 100 millions, et une fois arrivé à ce chiffre, il déclenchera une action, par exemple une interruption, pour signaler que l’intervalle de temps est écoulé.

Cependant, atteindre un tel compte d’un seul coup n’est pas toujours pratique. C'est pourquoi les microcontrôleurs utilisent souvent des *prescalers*, qui divisent la fréquence de l’horloge pour permettre au timer de fonctionner à des fréquences plus basses. Par exemple, avec un prescaler de 8, l'horloge d'entrée pour le timer sera réduite à 12.5 MHz (100 MHz / 8), ce qui permet de compter plus lentement et donc plus précisément pour des intervalles de temps plus longs. Néanmoins, pour obtenir une seconde cela reste compliqué.

Il est un cas particulier ou on utilise des quartz à la fréquence singulière de **32.768 kHz**. Les modules RTC (Real-Time Clock, ou horloge temps réel) parfois intégrés à un microcontrôleur permettent de calculer automatiquement l'heure, la date, l'exquinoxe... sans passer par le CPU, et donc sans le réveiller s'il dort. Cette fréquence de **32.768 kHz** est une fréquence qui, une fois divisée par $2^15$ (32'768 = $2^15$), donne précisément **1 Hz**, soit un cycle par seconde. Cela signifie qu’un timer qui fonctionne avec un quartz de 32.768 kHz et qui divise son signal d’horloge par 32 768 peut fournir un tic par seconde, ce qui est idéal pour maintenir le temps avec une grande précision.

### Fonctionnement

Le *timer* est un périphérique souvent indépendant du processeur principal, qui possède des registres de configuration, et des lignes d'interruptions.

Le timer est alimenté par le signal d'horloge du microcontrôleur (souvent après un passage par un prescaler, qui divise la fréquence). À chaque cycle de l'horloge, le compteur interne du timer s’incrémente. Un **Seuil de comparaison** peut être configuré pour déclencher une action lorsqu’il atteint une valeur spécifique (ce qu’on appelle un *match*). Par exemple, on peut configurer un timer pour qu’il déclenche une interruption toutes les 1000 millisecondes (1 seconde), ou après un certain nombre de cycles d'horloge.Lorsque le timer atteint cette valeur prédéfinie, il déclenche soit une **interruption**, soit une autre action définie (mise à jour d'une variable, allumage d'un LED, etc.).

### Cas d'utilisation

Les timers dans un microcontrôleur sont utilisés pour une variété d’applications :

**Générer des signaux périodiques**

: Les timers peuvent produire des signaux réguliers, utiles pour des tâches comme la génération de **PWM** (Pulse Width Modulation) pour contrôler la vitesse d’un moteur ou la luminosité d'une LED.

**Mesurer des intervalles de temps**

: Ils peuvent mesurer des délais précis, essentiels pour des protocoles de communication comme UART ou I2C.

**Créer des horloges temps réel**

: Comme évoqué avec les quartz de 32.768 kHz, les timers peuvent être utilisés pour maintenir le temps, même lorsque le reste du microcontrôleur est inactif.

**Déclencher des événements asynchrones**

: Par exemple, tu peux demander à un timer de générer une interruption toutes les millisecondes pour effectuer une mise à jour d’affichage ou une action récurrente dans ton programme.

## Ports

Un port sur un microcontrôleur représente une interface de communication physique entre le monde extérieur (les périphériques, les capteurs, les actionneurs, etc.) et le microcontrôleur lui-même. En termes simples, il s’agit d’un ensemble de broches ou de *pins* sur le microcontrôleur, que l’on peut configurer pour envoyer ou recevoir des signaux électriques. Ces signaux, souvent des tensions logiques (0 ou 1, basse ou haute tension), permettent au microcontrôleur d’interagir avec l’extérieur.

Un port est souvent groupé en plusieurs broches, généralement 8 (on parle alors d’un port sur 8 bits, mais il peut aussi y en avoir 16 ou d'autres configurations). Chaque broche d’un port peut être contrôlée indépendamment pour être configurée en entrée ou en sortie.

Chaque broche d’un port peut généralement être configurée en deux modes principaux : **entrée** ou **sortie**. On parle alors d'un GPIO (*General Purpose Input/Output*) pour une broche qui peut être configurée en entrée ou en sortie.

Dans le microcontrôleur, les ports sont contrôlés par des **registres** (variables internes à l’architecture). On trouve généralement trois types de registres associés à chaque port :

**Registre de direction**

: Ce registre permet de configurer chaque broche d’un port en mode entrée ou sortie.

**Registre de données**

: Ce registre contient les données que tu envoies ou lis sur les broches. Si la broche est en mode sortie, ce registre détermine si tu envoies un signal haut ou bas. Si la broche est en mode entrée, il lit la valeur du signal reçu.

**Registre d'état**

: Ce registre permet de lire l'état actuel des broches configurées en mode entrée. Si tu as un bouton ou un capteur connecté à une broche d’entrée, tu pourras vérifier son état via ce registre.

Souvent, il n'est pas possible de modifier l'état d'un bit d'un port de manière indépendante. On aura alors recours à l'algèbre de Boole pour modifier un bit sans modifier les autres.

```c
// Mettre à 1 le bit 2 du port B
PORTB |= (1 << 2);

// Mettre à 0 le bit 2 du port B
PORTB &= ~(1 << 2);

// Inverser le bit 2 du port B
PORTB ^= (1 << 2);
```
