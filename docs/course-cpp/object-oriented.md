# Orienté objet

## Un voyage vers l'abstraction structurée

À l'aube de la programmation informatique, le code n'était qu'une suite d'instructions linéaires, un simple flux séquentiel qui, dans les meilleurs des cas, reproduisait des schémas logiques simples. Mais au fur et à mesure que les systèmes devenaient plus complexes, l'organisation de ces instructions demandait plus de structure, plus de modularité. C'est là que les **paradigmes** de programmation commencèrent à émerger.

## Une manière de penser la programmation

Un **paradigme** en informatique peut être défini comme un modèle ou un style de programmation. Il impose une manière spécifique de penser et d’organiser le code, de résoudre des problèmes en suivant des règles bien définies. Le paradigme impératif, par exemple, ordonne les instructions, pas à pas, tandis que le paradigme fonctionnel privilégie les expressions mathématiques pures. Chaque paradigme propose un point de vue différent, un cadre conceptuel particulier pour aborder la résolution des problèmes.

Parmi ces paradigmes, un se distingue par sa capacité à modéliser des systèmes complexes en s’inspirant du monde réel : le paradigme **orienté objet**.

Le paradigme **orienté objet (OO)** propose une approche où le programme est conçu comme un ensemble d’entités autonomes appelées **objets**. Ces objets interagissent entre eux, chacun représentant une part spécifique du monde ou du problème à modéliser. L'idée sous-jacente est de rendre le code plus modulaire, réutilisable, et compréhensible en reflétant la structure des entités du monde réel ou de l'application simulée.

L'OO permet de représenter des concepts abstraits tout en conservant une organisation claire et hiérarchisée des données et des comportements. Cette approche est apparue en réponse à la complexité croissante des systèmes logiciels et des besoins d'une meilleure gestion de cette complexité.

Historiquement, l’OO trouve ses racines dans des langages pionniers comme **Simula** (années 1960), qui introduit les concepts d’objets et de classes, et **Smalltalk** (années 1970), qui formalise cette approche. Ces langages marquèrent un tournant dans la façon de concevoir les programmes. Par la suite, des langages comme **Java**, **Python**, et **C#**, ainsi que **C++**, portèrent ce paradigme à des niveaux plus élevés de popularité et de sophistication.

L'OO repose sur quelques concepts clés qui constituent son fondement et qui permettent d’organiser le code de manière robuste, modulaire et extensible :

**Objet**

: Un objet est une entité indépendante qui possède un état (sous forme de données ou attributs) et des comportements (sous forme de méthodes ou fonctions). Il est l’élément fondamental du paradigme objet, l’unité de base avec laquelle on construit tout le système.

**Classe**

: Une classe est un modèle, ou un plan, qui définit les attributs et les comportements des objets. Elle permet de créer plusieurs objets similaires partageant la même structure et les mêmes fonctionnalités. Les objets sont ainsi des **instances** d’une classe.

**Encapsulation**

: Ce principe consiste à cacher les détails internes d'un objet et à n'exposer que ce qui est nécessaire pour son utilisation. Cela se traduit par la séparation des données privées, que l’on protège, et des méthodes publiques qui permettent d’interagir avec l’objet. L’encapsulation réduit les interférences non souhaitées avec l’état interne de l’objet et améliore la robustesse du code.

**Abstraction**

: L’abstraction consiste à représenter uniquement les aspects essentiels d’un objet tout en ignorant les détails superflus. C’est une forme de simplification du code, permettant de manipuler les objets à un niveau élevé sans se soucier de leur implémentation détaillée.

**Héritage**

: L’héritage permet de créer de nouvelles classes à partir de classes existantes, en réutilisant et en spécialisant leurs propriétés et méthodes. Une classe dérivée (ou sous-classe) hérite ainsi des attributs et comportements d’une classe parente tout en pouvant les étendre ou les modifier. Cela favorise la réutilisation du code et la création de hiérarchies d'objets.

**Polymorphisme**

: Le polymorphisme permet à des objets de différentes classes de répondre à un même message ou appel de méthode de manières distinctes. Il peut être de deux types :

- **polymorphisme statique** (ou surcharge), lorsque plusieurs méthodes partagent le même nom mais présentent des signatures différentes ;
- **polymorphisme dynamique** (ou substitutivité), lorsqu’une sous-classe redéfinit une méthode afin de modifier le comportement tout en conservant la même interface.

Ces concepts, bien que simples en apparence, offrent une immense flexibilité pour modéliser des systèmes logiciels complexes tout en assurant une gestion claire de la structure et du comportement des objets.

## Les limites d’une approche manuelle

Avant l'avènement des langages orientés objet, le langage **C**, bien qu’efficace pour la programmation système, ne possédait pas ces abstractions de haut niveau. Cependant, certains programmeurs créatifs réussirent à simuler certains concepts de l’OO dans C, bien que d’une manière moins naturelle et plus complexe.

Prenons l'exemple des **structures** en C. Une structure (ou `struct`) est un regroupement de données sous un même type. On peut y voir une ébauche d’objet : elle permet d’associer plusieurs données liées sous un seul type composite. Par exemple :

```c
struct Point {
    int x;
    int y;
};
```

Pour ajouter du comportement à cette structure, des **pointeurs de fonctions** peuvent être utilisés afin d'associer des fonctions spécifiques à des structures. Voici comment un embryon de méthode pourrait être implémenté en C :

```c
struct Point {
    int x;
    int y;
    void (*move)(struct Point* self, int dx, int dy);
};

void move_point(struct Point* self, int dx, int dy) {
    self->x += dx;
    self->y += dy;
}

int main() {
    struct Point p = {0, 0, move_point};
    p.move(&p, 5, 10); // Déplace le point
}
```

Ici, on simule une méthode `move` à l’aide d’un pointeur de fonction, ce qui permet à un objet (la structure `Point`) d’avoir un comportement, à la manière d’un objet dans un langage OO. Toutefois, cette approche présente des limites considérables :

**Manque de sécurité**

: Rien ne garantit que les fonctions seront correctement associées aux structures. Le typage est plus lâche, et le programmeur doit manuellement gérer ces associations, augmentant le risque d'erreurs.

**Absence d’héritage et de polymorphisme**

: En C, il n’y a pas de moyen natif de créer des hiérarchies de types ou de surcharger des fonctions. Toute tentative d'imiter cela implique des bricolages fastidieux.

Ainsi, bien que C permette une certaine approximation de l'OO, il ne fournit pas les abstractions nécessaires pour exploiter pleinement ce paradigme.

## Les classes, une abstraction naturelle

Avec l’introduction de **C++**, ces approximations manuelles deviennent superflues. Le langage fournit directement des **classes**, qui englobent non seulement des données, mais aussi les méthodes qui leur sont associées. Une classe en C++ remplace la structure et le pointeur de fonction, tout en introduisant l’encapsulation, l’héritage, et le polymorphisme.

Voici un exemple équivalent en C++ :

```cpp
struct Point {
    int x, y;

    Point(int x = 0, int y = 0) {
        this->x = x;
        this->y = y;
    }

    void move(int dx, int dy) {
        x += dx;
        y += dy;
    }
};

int main() {
    Point p(0, 0);
    p.move(5, 10);  // Déplace le point
}
```

Dans cet exemple, la classe `Point` encapsule les données (`x`, `y`) et les comportements (`move`) en une seule entité cohérente. L'utilisation des constructeurs permet d'initialiser directement l'objet, et la gestion du comportement devient plus intuitive et sécurisée.

En résumé, le passage de **C** à **C++** représente un saut qualitatif immense dans la gestion des abstractions. Tandis que C permettait de bricoler des objets avec des structures et des pointeurs de fonction, C++ offre un cadre natif pour la programmation orientée objet, avec toutes les garanties et la souplesse que cela implique. Ce qui était laborieux et sujet à erreurs dans C devient naturel, élégant et puissant dans C++.

## Le vocabulaire orienté objet

La programmation orientée objet (OO) repose sur un ensemble de concepts clés qui forment un langage commun, essentiel pour comprendre et manipuler les systèmes logiciels modernes. Ce vocabulaire constitue la pierre angulaire de la conception OO et permet d'aborder la complexité de manière structurée et modulaire. Voici un aperçu des termes les plus importants de ce paradigme.

### Classe

Une **classe** est un modèle ou un plan qui définit la structure et le comportement des objets. Elle décrit les attributs (ou propriétés) et les méthodes (ou fonctions) que ses instances, appelées objets, posséderont. Voici un exemple de classe en C++:

```cpp
class Animal {
public:
    string nom;
    int age;
    void eat() { cout << "L'animal mange" << endl; }
};
```

Ici, la classe `Animal` définit deux attributs, `nom` et `age`, ainsi qu'une méthode `eat`.

### Instance

Une **instance** est créée à partir d'une classe. Chaque instance possède ses propres valeurs pour les attributs de la classe et peut exécuter les méthodes définies par celle-ci. Si la classe est le plan d'une maison, une instance est une maison réelle construite selon ce plan.

### Objet

Un **objet** est une **instance** d'une classe. Il représente une entité réelle ou abstraite avec laquelle le programme peut interagir. Chaque objet possède son propre état (valeurs des attributs) et peut exécuter les comportements définis par sa classe.

```cpp
Animal chat;
chat.nom = "Mimi";
chat.eat();
```

Dans cet exemple, `chat` est un objet de la classe `Animal` qui possède ses propres valeurs pour `nom` et `age`.

### Attribut

Les **attributs** (ou **champs**, **propriétés**) sont les variables définies dans une classe qui représentent l'état ou les caractéristiques de l'objet. Chaque objet a ses propres copies de ces attributs.

```cpp
int age;   // attribut qui stocke l'âge d'un objet de la classe Animal
```

### Méthode

Une **méthode** est une fonction définie à l'intérieur d'une classe, qui représente un comportement ou une action que les objets de cette classe peuvent accomplir. Les méthodes peuvent manipuler les attributs de l'objet ou interagir avec d'autres objets.

```cpp
void manger() {
    cout << "L'animal mange" << endl;
}
```

### Encapsulation

L'**encapsulation** consiste à restreindre l'accès direct aux attributs d'un objet et à contrôler cet accès via des méthodes. Cela permet de protéger l'état interne de l'objet et de définir clairement les points d'interaction avec celui-ci. En C++, cela se traduit par l'utilisation de **modificateurs d'accès** comme `public`, `private`, et `protected`.
**Exemple :**
```cpp
class Animal {
private:
    string nom;  // Attribut privé

public:
    void setNom(string n) { nom = n; }  // Méthode publique pour modifier l'attribut
    string getNom() { return nom; }     // Méthode publique pour accéder à l'attribut
};
```

Dans cet exemple, l'attribut `nom` est privé, et ne peut être directement modifié ou lu que via les méthodes publiques `setNom` et `getNom`.

### Abstraction

L'**abstraction** est le concept de simplification en se concentrant sur les caractéristiques essentielles d'un objet tout en cachant les détails non pertinents. Cela permet de manipuler des objets à un niveau conceptuel, sans se soucier de leur implémentation interne. En C++, les **classes abstraites** et les **interfaces** sont utilisées pour fournir des modèles conceptuels sans implémentation concrète immédiate.

```cpp
class Forme {
public:
    virtual double aire() = 0;  // Méthode virtuelle pure, définissant un comportement sans implémentation
};
```

Cette classe `Forme` représente une abstraction de toute forme géométrique sans se préoccuper de sa nature exacte. Les sous-classes devront fournir leur propre implémentation de la méthode `aire`.

### Héritage

L'**héritage** est un mécanisme qui permet à une classe de dériver d'une autre classe. La classe dérivée hérite des attributs et méthodes de la classe parent, tout en pouvant ajouter ou redéfinir ses propres fonctionnalités. Cela favorise la réutilisation du code et permet de créer des hiérarchies de classes.

```cpp
class Chien : public Animal {  // Chien hérite d'Animal
public:
    void aboyer() {
        cout << "Le chien aboie" << endl;
    }
};
```

Ici, `Chien` hérite des attributs et méthodes de `Animal`, tout en ajoutant son propre comportement `aboyer`.

### Polymorphisme

Le **polymorphisme** est la capacité d'une méthode ou d'un objet à se comporter de manière différente en fonction du contexte. Il permet à une classe dérivée de redéfinir des méthodes de la classe parent. Le polymorphisme peut être **statique** (surcharge de méthodes) ou **dynamique** (via l'utilisation de méthodes virtuelles).

```cpp
class Animal {
public:
    virtual void faireDuBruit() { cout << "L'animal fait du bruit" << endl; }
};

class Chien : public Animal {
public:
    void faireDuBruit() override { cout << "Le chien aboie" << endl; }
};

Animal* a = new Chien();
a->faireDuBruit();  // Appelle la méthode faireDuBruit() de la classe Chien
```

Grâce au polymorphisme dynamique, même si `a` est de type `Animal`, l'appel de la méthode `faireDuBruit()` exécutera celle de `Chien`.

### Constructeur et Destructeur

Un **constructeur** est une méthode spéciale appelée lors de la création d'un objet. Il initialise les attributs de l'objet. Un **destructeur** est une méthode appelée lors de la destruction de l'objet, qui permet de libérer des ressources ou de nettoyer l'état.

```cpp
class Animal {
public:
    Animal() { cout << "L'animal est créé" << endl; }  // Constructeur
    ~Animal() { cout << "L'animal est détruit" << endl; }  // Destructeur
};
```

### Interface et classe abstraite

Une **interface** est une classe qui ne contient que des méthodes virtuelles pures, c’est-à-dire des méthodes sans implémentation, que les classes dérivées doivent implémenter. Une **classe abstraite** est une classe qui peut contenir à la fois des méthodes implémentées et des méthodes virtuelles pures.

```cpp
class IAnimal {
public:
    virtual void faireDuBruit() = 0;  // Interface : méthode pure
};
```

Toute classe qui implémente cette interface doit fournir une implémentation de `faireDuBruit()`.

### Surcharge

La **surcharge** est une forme de polymorphisme statique où plusieurs méthodes peuvent partager le même nom mais avec des signatures différentes (paramètres distincts).

```cpp
class Math {
public:
    int additionner(int a, int b) { return a + b; }
    double additionner(double a, double b) { return a + b; }  // Surcharge de la méthode
};
```

### Redéfinition

La **redéfinition** est le fait qu’une classe dérivée puisse fournir sa propre version d'une méthode définie dans une classe parent. Cela se fait généralement via les **méthodes virtuelles**.

```cpp
class Animal {
public:
    virtual void faireDuBruit() { cout << "L'animal fait du bruit" << endl; }
};

class Chat : public Animal {
public:
    void faireDuBruit() override { cout << "Le chat miaule" << endl; }  // Redéfinition
};
```
