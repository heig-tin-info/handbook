# Quelques notes

Ce document contient quelques notes éparses sur la programmation et l'informatique destinées à être intégrées dans le cours.

## En vrac

Les langages de bas niveau sont ceux qui collent au jeu d'instructions de la machine.

Les programmes sont des briques de construction qui peuvent être combinées pour former des programmes plus complexes.

Définition du problème -> Modélisation -> Algorithmes -> Implémentation -> Test

Un modèle de données est une abstraction utilisée pour décrire des problèmes. Cette abstraction spécifie les valeurs qui peuvent être attribuées aux objets et les opérations valides sur ces objets. La structure de données, quant à elle, est une construction du langage de programmation, permettant de représenter un modèle de données.

Les opérations logiques sont introduites par l'[algèbre de Boole](https://fr.wikipedia.org/wiki/Alg%C3%A8bre_de_Boole_(logique)) et permettent de combiner plusieurs grandeurs binaires en utilisant des opérations. Cette algèbre est à la base de la logique numérique et de la conception des circuits logiques. Elle a été inventée par [George Boole](https://fr.wikipedia.org/wiki/George_Boole), un mathématicien et logicien anglais. Il définit dans son traité *An Investigation of the Laws of Thought* les opérations logiques suivantes :

Une algèbre de Boole est un domaine muni des constantes 0, 1 et des opérations d'inversion, de somme et de produit. Nous noterons l'inverse par une barre au-dessus de l'opérande inversé, la somme par `_` et le produit par `^`. Ces opérations ont les propriétés suivantes :

1. La somme et le produit sont associatifs, commutatifs et idempotents.
2. Le produit est distributif sur la somme, et la somme est distributive sur le produit.
3. 0 est l'élément neutre de la somme, 1 est l'élément neutre du produit.
4. 0 est l'élément absorbant du produit, 1 est l'élément absorbant de la somme.
5. \( x \vee \bar{x} = 1 \) (loi du tiers exclu), \( x \wedge \bar{x} = 0 \) (principe de contradiction), \( \bar{\bar{x}} = x \).
6. \( x \wedge y = x \_ y \), \( x \_ y = x \wedge y \) (lois de De Morgan).
