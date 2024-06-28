# Fiches d'unités de cours

Les fiches d'unités sont les documents de référence pour les cours d'info1 et d'info2, ici présentées sous forme de données brutes au format **YAML**.

(info1)=

## Informatique 1

```{literalinclude} ../../units/info1.yaml
:language: yaml
```

### Panification du semestre d'hiver

```{eval-rst}
+---------+------------+-------------------------+---------------------------+
| Semaine | Académique | Cours                   | Labo                      |
+=========+============+=========================+===========================+
|   38    | 1          | Introduction            | 00 Familiarisation        |
+---------+------------+-------------------------+---------------------------+
|   39    | 2          | Numération              | 01 Premier pas en C       |
+---------+------------+-------------------------+---------------------------+
|   40    | 3          | Fondements du C         | 02 Équation quadratique   |
+---------+------------+-------------------------+---------------------------+
|   41    | 4          | Variables, opérateurs   | 03 Fléchettes             |
+---------+------------+-------------------------+---------------------------+
|   42    | 5          | Types, entrées sorties  | 04 Pneus                  |
+---------+------------+-------------------------+---------------------------+
|   43    | Vacances d'automne                                               |
+---------+------------+-------------------------+---------------------------+
|   44    | 6          | Entrées sorties         | 05 Monte-Carlo            |
+---------+------------+-------------------------+---------------------------+
|   45    | 7          | **TE1**                 | 06 Tables Multiplications |
+---------+------------+-------------------------+---------------------------+
|   46    | 8          | Structure de contrôles  | 07 Chaînes (par équipe)   |
+---------+------------+-------------------------+---------------------------+
|   47    | 9          | Fonctions               | 08 Nombre d'Armstrong     |
+---------+------------+-------------------------+---------------------------+
|   48    | 10         | Tableaux et structures  | 09 Sudoku                 |
+---------+------------+-------------------------+                           |
|   49    | 11         | Programmes et processus |                           |
+---------+------------+-------------------------+---------------------------+
|   50    | 12         | Algorithmique           | **Labo Test**             |
+---------+------------+-------------------------+---------------------------+
|   51    | 13         | Pointeurs               | 10 Galton                 |
+---------+------------+-------------------------+---------------------------+
|   52    | Vacances de Noël                                                 |
+---------+                                                                  |
|    1    |                                                                  |
+---------+------------+-------------------------+---------------------------+
|    2    | 14         | Ergonomie et dialogues  | 12 Tableau des scores     |
+---------+------------+-------------------------+                           |
|    3    | 15         | **TE2**                 |                           |
+---------+------------+-------------------------+                           |
|    4    | 16         | Exercices de révision   |                           |
+---------+------------+-------------------------+---------------------------+
|   5     | **Préparation Examens**                                          |
+---------+------------+-------------------------+---------------------------+
|   6     | **Examens**                                                      |
+---------+------------+-------------------------+---------------------------+
|   7     | Relâches                                                         |
+---------+------------+-------------------------+---------------------------+
```

(info2)=

## Informatique 2

```{literalinclude} ../../units/info2.yaml
:language: yaml
```

### Panification du semestre de printemps

```{eval-rst}
+---------+------------+-------------------------+---------------------------+
| Semaine | Académique | Cours                   | Labo                      |
+=========+============+=========================+===========================+
|    8    | 1          | Introduction            | GitHub - WSL              |
+---------+------------+-------------------------+---------------------------+
|    9    | 2          | Fichiers                | Proust (partie 1)         |
+---------+------------+-------------------------+---------------------------+
|   10    | 3          | Allocation dynamique    | Proust (partie 2)         |
+---------+------------+-------------------------+---------------------------+
|   11    | 4          | Allocation dynamique    | Météo (partie 1)          |
+---------+------------+-------------------------+---------------------------+
|   12    | 5          | Compilation séparée     | Météo (partie 2)          |
+---------+------------+-------------------------+---------------------------+
|   13    | 6          | Préprocesseur           | Tableau dynamique (1/2)   |
+---------+------------+-------------------------+---------------------------+
|   14    | 7          | Unions, champs de bits  | Tableau dynamique (2/2)   |
+---------+------------+-------------------------+---------------------------+
|   15    | 8          | Usage bibliothèques     | Stéganographie            |
+---------+------------+-------------------------+---------------------------+
|   16    | Vacances de Pâques                                               |
+---------+------------+-------------------------+---------------------------+
|   17    | 9          | **TE1**                 | Wave (partie 1)           |
+---------+------------+-------------------------+---------------------------+
|   18    | 10         | Algorithmique Big-O     | Wave (partie 2)           |
+---------+------------+-------------------------+---------------------------+
|   19    | 11         | Tris                    | Quick-Sort / Merge-Sort   |
+---------+------------+-------------------------+---------------------------+
|   20    | 12         | Queues et piles         | Tries                     |
+---------+------------+-------------------------+---------------------------+
|   21    | 13         | Sockets                 | **Labo Test**             |
+---------+------------+-------------------------+---------------------------+
|   22    | 14         | **TE2**                 | Shunting-yard             |
+---------+------------+-------------------------+---------------------------+
|   23    | 15         | Arbres binaires         | Tries (partie 1)          |
+---------+------------+-------------------------+---------------------------+
|   24    | 16         | Exercices de révision   | Tries (partie 2)          |
+---------+------------+-------------------------+---------------------------+
|   25    | Préparation Examens                                              |
+---------+------------+-------------------------+---------------------------+
|   26    | Examens                                                          |
+---------+------------+-------------------------+---------------------------+
```

## Modalités d'évaluation et de validation

Le cours se compose de :

- Travaux écrits notés (coefficient 100%)
- Quiz notés ou non (coefficient 10% ou 0%)
- Séries d'exercices
- Travaux pratiques, 2 à 3 labos notés (laboratoires)
- Labo test noté comptabilisé comme un labo

La note finale est donnée par l'expression :

$$
\text{final} =
\frac{
\sum\limits_{t=1}^\text{T}{\text{TE}_t} +
10\% \cdot \sum\limits_{q=1}^\text{Q}{\text{Quiz}_q}
}{
4 \cdot (\text{T} + 10\% \cdot \text{Q})
}
+
\frac{1}{4 L}
\sum\limits_{l=1}^L
\text{Labo}_l
+
\frac{1}{2}
\text{Exam}
$$

L'équivalent en C :

```c
#define QUIZ_WEIGHT (.1) // Percent
#define EXAM_WEIGHT (.5) // Percent

typedef struct notes {
    size_t size;
    float values[];
} Notes;

float sum(Notes *notes) {
    float s = 0;
    for (int i = 0; i < notes->size; i++)
        s += notes->values[i];
    return s;
}

float mark(Notes tes, Notes quizzes, Notes labs, float exam) {
    return (
    sum(tes) + QUIZ_WEIGHT * sum(quizzes)
    ) / (
        (EXAM_WEIGHT / 2.) * (tes.size + QUIZ_WEIGHT * quizzes.size)
    ) +
            (EXAM_WEIGHT / 2.) * sum(labs) / labs.size +
        EXAM_WEIGHT * exam;
}
```

Les règles sont :

- En cas d'absence à un quiz, la note de 1.0 est donnée.
- En cas de plagiat, le [dilemme du prisonnier](https://fr.wikipedia.org/wiki/Dilemme_du_prisonnier#:~:text=Le%20dilemme%20du%20prisonnier%2C%20%C3%A9nonc%C3%A9,est%20jou%C3%A9%20qu'une%20fois.) s'applique.
- Le quiz le plus mauvais ne compte pas.
