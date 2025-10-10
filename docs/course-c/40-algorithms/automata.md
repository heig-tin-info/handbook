# Automates finis

Dans le contexte de l'algorithmique, il est pertinent d'aborder les automates finis. Ces machines abstraites peuvent se trouver dans un nombre limité d'états. Elles servent à modéliser des systèmes de transitions d'état, très utiles pour élaborer des algorithmes de traitement du langage naturel, de reconnaissance de formes ou encore d'analyse de données.

![Hiérarchie des automates](/assets/images/automata-classes.drawio)

Nous avions évoqué, en introduction de cet ouvrage, la [machine de Turing][turingmachine], modèle théorique capable d'exécuter n'importe quel algorithme. Bien que la très grande majorité des langages de programmation soient dits Turing-complets, il reste parfois plus judicieux de recourir à des automates finis pour certains problèmes spécifiques. Une règle pragmatique en informatique recommande d'aligner la complexité de l'outil sur celle du problème à résoudre. Autrement dit, si un problème possède une structure simple, il est plus efficace d'utiliser un modèle computationnel ou un langage de programmation d'une complexité comparable. Employer un outil plus puissant que nécessaire peut engendrer des inefficacités, des erreurs ou des solutions inutilement lourdes.

On rencontre les automates finis dans de très nombreux domaines, du distributeur automatique de boissons aux ascenseurs en passant par les feux de circulation.

Contrairement à un système Turing-complet, un automate fini ne peut pas réaliser n'importe quel algorithme. Sa structure et son nombre d'états limités restreignent ses capacités. Voici, par exemple, un automate simple qui modélise un ascenseur :

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

Un autre exemple classique d'automate fini est le problème de la chèvre, du chou et du loup. Un fermier doit transporter ces trois éléments d'une rive à l'autre d'une rivière. Il ne peut déplacer qu'un seul passager à la fois et ne doit jamais laisser la chèvre seule avec le loup ni le chou seul avec la chèvre. Le défi consiste à trouver une séquence de traversées qui respecte toutes ces contraintes.

Ce problème peut être modélisé par un automate fini. Chaque état est nommé d'après les éléments déjà arrivés. Par exemple, l'état CFS signifie que le chou, le fermier et le loup ont traversé. Les transitions précisent quels éléments passent d'une rive à l'autre. Notons que l'on désigne le chou par `S` (comme *salade*) afin d'éviter la confusion avec la chèvre. Voici le diagramme d'états :

![La chèvre, le loup et le chou](/assets/images/river-crossing.drawio)

### Implémentation

On commence généralement par définir les états et les transitions de l'automate. On ajoute volontairement une entrée [manglée](https://fr.wikipedia.org/wiki/D%C3%A9coration_de_nom) `COUNT` afin de connaître facilement le nombre d'éléments dans l'énumération.

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

L'objectif est de pouvoir déclencher les transitions simplement :

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

Les automates finis peuvent être implémentés de différentes manières. Une solution courante consiste à utiliser une instruction `switch-case`. Voici un exemple en C :

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

Une autre approche consiste à utiliser un tableau de transition. Cette représentation sépare la logique de transition de son implémentation. Voici un exemple :

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

Il existe deux grandes familles d'automates finis : les automates déterministes (DFA) et les automates non déterministes (NFA). Dans un DFA, la transition est entièrement déterminée par l'état courant et l'entrée reçue. Dans un NFA, plusieurs transitions peuvent coexister pour un même couple état/entrée, laissant au modèle le soin de choisir son chemin.

Pour un ordinateur, il est plus simple d'exécuter un automate déterministe qu'un automate non déterministe. Cependant, les NFA sont plus expressifs, car ils peuvent représenter des langages plus complexes. Heureusement, des algorithmes permettent de convertir un NFA en DFA équivalent, quitte à provoquer une explosion du nombre d'états.

Un cas typique d'utilisation de ces diagrammes d'états est la conception d'expressions régulières. Pour rappel, une expression régulière est une chaîne de caractères qui décrit un ensemble de chaînes. On les utilise pour rechercher des motifs parfois très complexes.

L'objectif n'est pas de rentrer dans le détail, mais de donner un aperçu de ce qu'il est possible de faire avec les automates finis. Admettons que l'on souhaite rechercher des motifs de texte contenant les lettres `A` et `B`. Plusieurs combinaisons sont envisageables : on peut rechercher `A` ou `B` (`#!re /A|B/`), ou bien `A` suivi de `B` (`#!re /AB/`). En utilisant l'étoile de [Kleene](https://fr.wikipedia.org/wiki/%C3%89toile_de_Kleene) `*`, on peut également accepter zéro ou plusieurs occurrences de `A` (`#!re /A*/`).

Dans ces exemples, à chaque état un caractère est capturé sur la chaîne de recherche (le curseur avance d'un caractère) :

![DFA simples](/assets/images/regex-nfas.drawio)

À partir de ces éléments simples, il est possible de construire une expression plus complexe comme `#!re /Z|X(X|Y)*/` : la lettre `Z` seule ou `X` suivi de `X` ou `Y`, répétés zéro ou plusieurs fois. Pour l'étoile de Kleene, la construction n'est pas toujours évidente. Pour résoudre ce problème, on introduit la notion de transition epsilon `ε`, qui permet de passer d'un état à un autre sans consommer de caractère. On peut en ajouter autant que nécessaire :

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
