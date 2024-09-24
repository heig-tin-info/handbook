# Systèmes à microcontrôleurs

## Introduction

## Les microcontrôleurs

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

## Ports

## Timers
