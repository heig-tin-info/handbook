
# Processeur minimal

## Introduction

L'objectif est de proposer à titre purement pédagogique, un processeur minimaliste dont les objectifs sont les suivants :

1. Architecture inspirée de processeurs existants
2. ISA minimaliste pour faciliter la compréhension
3. Implémentable en logique combinatoire

Le travail est inspiré du LC-3 (*Little Computer 3*) qui est un processeur minimaliste conçu pour l'apprentissage de l'architecture des ordinateurs. Le LC-3 est un processeur 16-bit avec un jeu d'instructions réduit. Il est utilisé dans de nombreux cours d'architecture des ordinateurs pour enseigner les concepts de base de l'architecture des ordinateurs. Ici l'objectif est de simplifier encore l'architecture pour la rendre plus accessible à celui qui souhaite apprendre à programmer et qui est simplement curieux de comprendre comment fonctionne un processeur.

### ISA

Le choix de l'ISA (*Instruction Set Architecture*) est un élément clé dans la conception d'un processeur. Ce que nous savons c'est qu'un programme en mémoire sera plus facile à exécuter si une instruction est un multiple de la taille d'un mot (16-bit sur un processeur 16-bit), cela simplifie la logique de décodage des instructions. Néanmoins beaucoup de processeurs modernes ont des instructions de taille variable. Une des instruction les plus utilisée est celle de déplacement mémoire `MOV` qui est souvent utilisée pour copier un registre dans un autre.

Un simple calcul montre qu'un jeu d'instruction sur 4 bit et 8 registres nécessitent $opcode + source + destination = 4 + 3 + 3 = 10$ bits pour définir une instruction. Une addition pourrait se composer de $opcode + valeur gauche + valeur droite + destination = 4 + 3 + 3 + 3 = 13$ bits. Si on permet 16 registres, il faudrait 4 bits pour les registres, ce qui augmenterait la taille des instructions à 16-bit la limite sur notre architecture pour que les instructions soient multiples de la taille d'un mot. En outre nous serions ici limité à 16 instructions différentes.

POur information voici pour différentes architectures le nombre d'instructions disponibles:

Table: Nombre d'instructions pour différentes architectures

| Architecture            | Instructions |
| ----------------------- | ------------ |
| OISC                    | 1            |
| LC-3                    | 15           |
| 4004                    | 46           |
| 8080                    | 244          |
| 8051                    | 255          |
| ARM Cortex-M0 (ARMv6-M) | 56           |
| ARM Cortex-M3 (ARMv7-M) | 83           |
| ARM Cortex-A53 (ARMv8)  | >500         |
| x86-64                  | >1000        |

Le jeu d'instruction le plus réduit qui permet néanmoins de réaliser un processeur Turing complet est de une instruction comme sur l'OISC (*One Instruction Set Computer*) ou le CPU Zero. On peut en effet concevoir un processeur minimaliste avec l'instruction *Subtract and Branch if Negative* (SBN). C'est une instruction qui soustrait deux valeurs et saute à une adresse si le résultat est négatif. Avec cette seule instruction, il est possible de simuler toutes les opérations qui seraient normalement effectuées par un ensemble d'instructions plus riche comme l'addition, la soustraction, les comparaisons et les sauts conditionnels.

On peut également noter que la quantité d'instructions dans un processeur classifie également sa nature, on distingue les processeurs RISC (*Reduced Instruction Set Computer*) et CISC (*Complex Instruction Set Computer*). Les processeurs RISC ont un jeu d'instructions plus réduits réduit, ce qui les rend plus simples et plus rapides. Les processeurs CISC ont un jeu d'instructions plus riche, ce qui les rend plus complexes mais plus polyvalents. Il y eut longtemps le débat entre les deux architectures, mais de nos jours, les processeurs modernes sont hybrides, ils combinent les avantages des deux architectures.

Pour notre processeur nous faisons le choix d'avoir un minimum utile comme le `XOR` qui autrement devrait être simulé avec `(A OR B) AND NOT (A AND B)`.

Table: Instructions pour notre CPU-Zero

| Instruction   | Description                                            |
| ------------- | ------------------------------------------------------ |
| `NOP`         | Opération nulle, ne fait rien                          |
| `ADD Rx, Ry`  | Additionne Ry à Rx, le résultat dans Rx                |
| `ADD Rx, #n`  | Additionne n à Rx, n entre 0 et 15                     |
| `SUB Rx, Ry`  | Soustrait Ry à Rx, le résultat dans Rx                 |
| `SUB Rx, #n`  | Soustrait n à Rx, n entre 0 et 15                      |
| `RSH Rx, Ry`  | Décale à droite Rx de Ry bits                          |
| `LSH Rx, Ry`  | Décale à gauche Rx de Ry bits                          |
| `AND Rx, Ry`  | `ET` logique entre Rx et Ry, résultat dans Rx          |
| `OR Rx, Ry`   | `OU` logique entre Rx et Ry, le résultat dans Rx       |
| `XOR Rx, Ry`  | `OU EXCLUSIF` logique entre Rx et Ry, résultat dans Rx |
| `JNZ Rx, Ry`  | Si Rx est non nul, saute à l'instruction Ry            |
| `JZ Rx, Ry`   | Si Rx est nul, saute à l'instruction Ry                |
| `MOV Rx, #n`  | Copie la valeur n dans Rx, n entre 0 et 15             |
| `MOV Rx, Ry`  | Copie le registre Ry dans Rx                           |
| `MOV Rx, @Ry` | Copie la valeur pointée par le registre Ry dans Rx     |
| `MOV @Rx, Ry` | Copie la valeur de Rx dans la mémoire pointée par Ry   |

### Architecture

Sur la figure suivante, on propose une architecture minimale d'un processeur avec un jeu d'instructions réduit:

![Architecture minimale](/assets/images/cpu-zero.drawio)

Notre ALU (*Arithmetic Logic Unit*) serait implémenté en logique combinatoire, c'est-à-dire que les opérations sont effectuées en un seul cycle d'horloge. L'ALU est composée de deux entrées `A` et `B` et d'une sortie `C`. Les opérations possibles sont:

Table : Opérations de l'ALU

| Opcode | Opération     |
| ------ | ------------- |
| `000`  | $C = A + B$   |
| `001`  | $C = A - B$   |
| `010`  | $C = A and B$ |
| `011`  | $C = A or B$  |
| `100`  | $C = A xor B$ |
| `101`  | $C = A >> B $ |
| `110`  | $C = A << B $ |
| `111`  | $C = 0$       |


```
00 A
01 B
02 (C)
03 OP
04 ST
05 PC
06 ADDR
07 DATA
10 R0
11 R1
12 R2
13 R3
14 R4
15 R5
16 R6 (INPUT)
17 R7 (OUTPUT)

DST is most of the time in the ACC, except in C=B, so we have 4 bits available.

La logique de commande prend

0. ST.state = LOAD
1. PC contient l'adresse de l'instruction à exécuter.
2. PC -> ADDR
3. DATA -> OP
4. ST.state = FETCH, EXECUTE and STORE
5. OP.tmp -> RMUX
6. -> B
7. OP.src -> @RMUX
8. @RMUX -> A
9. OP.state =
8. C -> @RMUX
9. OP.state = INC-PC
9. OP = ADD PC, 1
10. fetch, execute and store
11. Go 0

// After operation, introduire registre PI (Program Increment)
// Vaut 1, sauf dans le cas d'un saut
ADD PC, 1  // Standard after operation
ADD PC, Rx // Jump to Rx
```

Fixons quelques caractéristiques de notre processeur minimal :

- L'architecture est 16-bit, donc le bus d'adresse et de données sont de 16-bit. Cela signifie que le processeur peut adresser $2^16 = 65536$ adresses mémoire différentes, et que les données sont stockées sur des `short` de 16 bits.
- Il n'y a qu'un bus pour les données et les adresses, ce qui signifie que le bus de données et le bus d'adresse sont partagés et qu'ils ont la même largeur.
- L'adresse `0x0000` est le point d'entrée du programme, c'est là qu'au démarrage du processeur, le programme commence à s'exécuter.
- L'adresse `0xFFFE` est l'entrée standard, c'est une queue. Lorsque le buffer est vide, la valeur lue est `0x00FF`.
- L'adresse `0xFFFF` est la queue de sortie, l'affichage de la sortie, chaque valeur écrite est imprimée en ASCII sur une imprimante, les valeurs sont donc des caractères ASCII de 8 bits.

Le processeur dispose de registres

- `A` : Accumulateur, première entrée de l'ALU
- `B` : Deuxième entrée de l'ALU (temporaire)
- `C` : Résultat de l'ALU
- `R0 à R7` : registres généraux de 16 bits
- `OP` : instruction en cours d'exécution
- `ST` : statut de l'ALU (zéro, négatif, carry, overflow)
- `PC` : pointeur d'instruction, il contient l'adresse de la prochaine instruction à exécuter
- `ADDR` : adresse de la mémoire à laquelle on veut accéder
- `DATA` : valeur lue ou que l'on souhaite écrire dans la mémoire

Une machine t'état est utilisée pour contrôler le processeur. Elle permet de générer les signaux de contrôle suivants:

- `RD` : active la lecture de la mémoire pointée par `ADDR`
- `WR` : active l'écriture dans la mémoire pointée par `ADDR`
- `LPC` : latch `PC`
- `LA` : latch la valeur sur le bus dans `A`
- `LB` : latch la valeur sur le bus dans `B`
- `LC` : Expose sur le bus la valeur de `C`
- `LAOP` : latch l'OP
- `LST` : Expose le status sur le bus
- `LREGxxx` : latch le registre

## Cycle d'exécution

Ce CPU n'a pas de pipeline néanmoins différentes étapes sont nécessaires pour exécuter une instruction. Pour des raisons de logique et de timing, chaque étapes est effectuées en un cycle d'horloge.

1. `PC` contient l'adresse de l'instruction à exécuter.
2. `LPC` expose l'adresse sur le bus.
3. `READ` lis une valeur en mémoire et la place dans `DATA`
4. `LOP` latch l'`OP` avec la valeur de `DATA`
5. `LREGxxx` and `LA` to transfer the register from the bus to `A`
6. `LREGxxx` and `LB` to transfer the register from the bus to `B`
7. `LC` expose the result of the ALU on the bus
8. `LREGxxx` and `LC` to transfer the result of the ALU to the register
9. `PC` copied on `A` using `LPC` and `LA`
10. `LOGIC` exposes `ADD1` instruction on the bus
11. `ALU` is configured to add one to the `PC`
12. `C` is latched into `PC`




| Opcode     | Instruction | Exemple     | Description                           |
| ---------- | ----------- | ----------- | ------------------------------------- |
| 0b0000xxxx | ADD         |             |                                       |
| 0b0001xxxx | SUB         |             |                                       |
| 0b0010xxxx | AND         |             |                                       |
| 0b0011xxxx | OR          |             |                                       |
| 0b0100xxxx | XOR         |             |                                       |
| 0b0101xxxx | JNZ         | 0b0101'xxxx | Saut relatif de B (PC += B) si A != 0 |
| 0b01100rrr | MOV A, Rx   | 0b0110'0001 | MOV A, R1                             |
| 0b01101rrr | MOV B, Rx   | 0b0111'0010 | MOV B, R2                             |
| 0b0111xrrr | MOV Rx, C   | 0b0111'1000 | MOV R0, C                             |
| 0b10rrrsss | MOV Rx, Ry  | 0b1000'0010 | MOV R0, R2                            |
| 0b11rrrsss | MOV Rx, @Ry | 0b1100'0010 | MOV R0, @(R2, R3)                     |
