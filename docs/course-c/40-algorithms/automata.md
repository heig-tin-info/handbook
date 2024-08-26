# Automates finis

Dans le contexte de l'algorithmique, il est intéressant de d'aborder les automates finis. Les automates finis sont des machines abstraites qui peuvent être dans un nombre fini d'états. Ils sont utilisés pour modéliser des systèmes de transitions d'états très utile dans l'élaboration d'algorithmes notament pour le traitement de langage naturel, la reconnaissance de formes, où l'analyse de données.

![Hiérarchie des automates](/assets/images/automata-classes.drawio)

Nous avions abordé en introduction de cet ouvrage la [machine de Turing][turing-machine], ce modèle théorique permettant de réaliser n'importe quel algorithme. Bien que la très grande majorité des langages de programmation sont dit Turing-complet, il est parfois plus intéressant d'utiliser des automates finis pour des problèmes spécifiques car il existe une règle en informatique qui dit qu'il est généralement optimum d'aligner la complexité d'un langage avec la complexité du problème à résoudre. L'idée sous-jacente est que si un problème a une structure ou une complexité faible, il est généralement plus efficace de le résoudre avec un modèle computationnel ou un langage de programmation dont la complexité est alignée avec celle du problème. Utiliser un outil plus puissant ou plus complexe que nécessaire peut entraîner des inefficacités, des erreurs, ou des solutions surdimensionnées.

On rencontre les automates finis dans de très nombreux domaines, du distributeur automatique de boisson aux ascenceurs en passant par les feux de circulation.

Contrairement à un système turing-complete, un automate fini ne peut pas réaliser n'importe quel algorithme. Il est limité par sa structure et son nombre fini d'états. Voici l'exemple d'un automate fini simple qui modélise un ascenseur :

![Ascenseur](/assets/images/elevator-states.drawio)

Ces états peuvent également être représentés par un tableau de transition :

| État actuel   | Entrée       | État suivant  | Sortie                                  |
| ------------- | ------------ | ------------- | --------------------------------------- |
| Arrêté        | Ouvrir porte | Porte ouverte | La porte s'ouvre                        |
| Arrêté        | Appel        | En mouvement  | Se déplace à l'étage                    |
| En mouvement  | Arrêt        | Porte ouverte | Arrivé à l'étage, la porte s'ouvre      |
| En mouvement  | Arrivé       | Arrêté        | Arrive à l'étage                        |
| Porte ouverte | Fermer porte | Arrêté        | La porte se ferme                       |
| Porte ouverte | Appel        | En mouvement  | La porte se ferme, se déplace à l'étage |

## La chèvre et le chou

Un autre exemple classique d'automate fini est le problème de la chèvre, du chou et du loup. Il s'agit d'un problème de logique dans lequel un fermier doit transporter une chèvre, un chou et un loup d'une rive à l'autre d'une rivière. Le fermier ne peut transporter qu'un seul élément à la fois et ne peut pas laisser la chèvre seule avec le loup ou le chou seul avec la chèvre. Le problème est de trouver une séquence de déplacements qui permet de transporter les trois éléments d'une rive à l'autre sans enfreindre les règles.

Ce problème peut être modélisé par un automate fini. Chaque état est nommé selon les éléments présents sur la rive d'arrivée. Par exemple l'état CFS signifie que la chèvre, le loup et le fermier sont sur la rive d'arrivée. Les transitions indiquent les éléments qui transitent d'une rive à l'autre. Notons que l'on appelle `S` le chou (comme Salade), pour éviter la confusion avec la chèvre. Voici le diagramme d'états :

![La chèvre, le loup et le chou](/assets/images/river-crossing.drawio)

### Implémentation

Généralement on commence par définir les états et les transitions de l'automate. On ajoute volontairement une entrée [manglée](https://fr.wikipedia.org/wiki/D%C3%A9coration_de_nom) `COUNT` pour facilement connaître le nombre d'éléments dans l'énumération.

```c
typedef enum {
    STATE_IDLE,
    STATE_MOVING,
    STATE_DOOR_OPEN,
    _STATE_COUNT
} State;

typedef enum {
    INPUT_OPEN_DOOR,
    INPUT_CALL,
    INPUT_STOP,
    INPUT_ARRIVAL,
    INPUT_CLOSE_DOOR,
    _INPUT_COUNT
} Input;

void openDoor() { printf("The door opens.\n"); }
void closeDoor() { printf("The door closes.\n"); }
void moveElevator() { printf("The elevator is moving.\n"); }
void stopElevator() { printf("The elevator stops.\n"); }
```

L'objectif est de pouvoir émettre des transitions simplement:

```c
int main() {
    State currentState = STATE_IDLE;

    // Exemples de transitions
    currentState = transition(currentState, INPUT_CALL);
    currentState = transition(currentState, INPUT_STOP);
    currentState = transition(currentState, INPUT_CLOSE_DOOR);
    currentState = transition(currentState, INPUT_CALL);
    currentState = transition(currentState, INPUT_ARRIVAL);
}
```

Les automates finis peuvent être implémentés de différentes manières. Une solution courante est d'utiliser un `switch-case`. Voici l'exemple en C:

```c
State transition(State currentState, Input input) {
    switch (currentState) {
        case STATE_IDLE:
            switch (input) {
                case INPUT_OPEN_DOOR:
                    openDoor();
                    return STATE_DOOR_OPEN;
                case INPUT_CALL:
                    moveElevator();
                    return STATE_MOVING;
                default:
                    return currentState;
            }

        case STATE_MOVING:
            switch (input) {
                case INPUT_STOP:
                    stopElevator();
                    openDoor();
                    return STATE_DOOR_OPEN;
                case INPUT_ARRIVAL:
                    stopElevator();
                    return STATE_IDLE;
                default:
                    return currentState;
            }

        case STATE_DOOR_OPEN:
            switch (input) {
                case INPUT_CLOSE_DOOR:
                    closeDoor();
                    return STATE_IDLE;
                case INPUT_CALL:
                    closeDoor();
                    moveElevator();
                    return STATE_MOVING;
                default:
                    return currentState;
            }

        default:
            return currentState;
    }
}
```

Une autre approche est d'utiliser un table de transition. Cela permet de séparer la logique de transition de l'implémentation. Voici un exemple:

```c
typedef void (*ActionFunction)();

typedef struct transition {
    State nextState;
    ActionFunction action;
} Transition;

Transition stateTransitionTable[_STATE_COUNT][_INPUT_COUNT] = {
    [STATE_IDLE][INPUT_OPEN_DOOR] = {STATE_DOOR_OPEN, openDoor},
    [STATE_IDLE][INPUT_CALL] = {STATE_MOVING, moveElevator},
    [STATE_IDLE][INPUT_STOP] = {STATE_IDLE, NULL},
    [STATE_IDLE][INPUT_ARRIVAL] = {STATE_IDLE, NULL},
    [STATE_IDLE][INPUT_CLOSE_DOOR] = {STATE_IDLE, NULL},

    [STATE_MOVING][INPUT_OPEN_DOOR] = {STATE_MOVING, NULL},
    [STATE_MOVING][INPUT_CALL] = {STATE_MOVING, NULL},
    [STATE_MOVING][INPUT_STOP] = {STATE_DOOR_OPEN, openDoor},
    [STATE_MOVING][INPUT_ARRIVAL] = {STATE_IDLE, stopElevator},
    [STATE_MOVING][INPUT_CLOSE_DOOR] = {STATE_MOVING, NULL},

    [STATE_DOOR_OPEN][INPUT_OPEN_DOOR] = {STATE_DOOR_OPEN, NULL},
    [STATE_DOOR_OPEN][INPUT_CALL] = {STATE_MOVING, moveElevator},
    [STATE_DOOR_OPEN][INPUT_STOP] = {STATE_DOOR_OPEN, NULL},
    [STATE_DOOR_OPEN][INPUT_ARRIVAL] = {STATE_DOOR_OPEN, NULL},
    [STATE_DOOR_OPEN][INPUT_CLOSE_DOOR] = {STATE_IDLE, closeDoor},
};

State transition(State currentState, Input input) {
    Transition transition = stateTransitionTable[currentState][input];
    if (transition.action != NULL) {
        transition.action();
    }
    return transition.nextState;
}
```

## DFA et NFA

Il existe deux types d'automates finis : les automates finis déterministes (DFA) et les automates finis non déterministes (NFA). Les DFA sont des automates finis dont les transitions sont déterminées par l'état actuel et l'entrée. Les NFA sont des automates finis dont les transitions peuvent être non déterministes, c'est-à-dire qu'il peut y avoir plusieurs transitions possibles pour un état et une entrée donnés.

Pour un ordinateur, il est plus facile de traiter un automate fini déterministe qu'un automate fini non déterministe. Cependant, les NFA sont plus puissants que les DFA, car ils peuvent représenter des langages plus complexes. Heureusement il existe des algorithmes pour convertir un NFA en un DFA équivalent, mais cela peut entraîner une explosion de l'espace d'état.

Un cas typique d'utilisation de ces diagrammes d'états sont les expressions régulières. Pour rappel, une expression régulière est une chaîne de caractère qui décrit un ensemble de chaînes de caractères. On les utilises pour rechercher des motifs complexes.

L'objectif n'est pas de rentrer dans le détail mais de vous donner un aperçu de ce qu'il est possible de faire avec les automates finis. Admettons que l'on souhaite rechercher des motifs de texte contenant les lettres `A` et `B`. On peut avoir plusieurs combinaisons par exemple on recherche soit un `A` ou un `B` `#!re /A|B/` ou bien un `A` suivi d'un `B` `#!re /AB/`. En utilisant l'étoile de [Kleene](https://fr.wikipedia.org/wiki/%C3%89toile_de_Kleene) `*` on peut également rechercher zéro ou plusieurs occurences de `A`: `#!re /A*/`.

Dans ces exemples, à chaque état un caractère est capturé sur la chaîne de recherche (le curseur avance d'un caractère) :

![DFA simples](/assets/images/regex-nfas.drawio)

À partir de ces éléments simples, il est possible de construire une expression plus complexe comme `#!re /Z|X(X|Y)*/` : la lettre `Z` seule ou bien `X` suivi de `A` ou `B` zéro ou plusieurs fois. Pour le cas de figure de l'étoile de Kleene, il n'est pas évident de constuire cette expression. Pour résoudre ce problème on introduit la notion de transition epsilon `ε` qui permet de passer d'un état à un autre sans consommer de caractère. On peut en mettre autant que l'on veut :

![NFA avec epsilon](/assets/images/regex-nfa.drawio)

Ce diagramme d'état peut être représenté sous forme de tableau de transition :

Table: Table de transition

|     | X   | Y   | Z   | ε     |
| --- | --- | --- | --- | ----- |
| >1  | 2   | -   | 5   | 1     |
| 2   | -   | -   | -   | 2,3,5 |
| 3   | 4   | 4   | -   | 3     |
| 4   | -   | -   | -   | 4,5   |
| (5) | -   | -   | -   | 5     |

Dans le but de simplifier on peut utiliser l'algorithme de [Thompson-McNaughton-Yamada](https://fr.wikipedia.org/wiki/Algorithme_de_Thompson) pour convertir l'automate non déterministe en un automate déterministe. Pour ce faire on utilise la table de transition suivante qui utilise les *epsilon-closures* :

Table: Table de transition simplifiée

|         | Xε*     | Yε*     | Zε* |
| ------- | ------- | ------- | --- |
| >1      | 2,3,(5) | -       | (5) |
| 2,3,(5) | 3,4,(5) | 3,4,(5) | -   |
| (5)     | -       | -       | -   |
| 3,4,(5) | 3,4,(5) | 3,4,(5) | -   |

Ceci nous donne un automate fini déterministe (DFA):

![DFA](/assets/images/regex-dfa.drawio)

### Implémentation

Si nous souhaitons implémenter un moteur d'expression régulières simple qui prend en compte les éléments suivants:

- `.` : n'importe quel caractère
- `|` : ou
- `( )` : groupe
- `*` : zéro ou plusieurs occurences
- `+` : une ou plusieurs occurences
- Les autres caractères sont littéraux

Les étapes de l'algorithmes sont les suivants:

1. Convertir l'expression d'entrée en un NFA
2. Appliquer l'algorithme de Thompson pour convertir le NFA en un DFA
3. Utiliser le DFA pour rechercher les motifs dans le texte
