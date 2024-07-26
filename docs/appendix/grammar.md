# Grammaire C

[Yacc](https://fr.wikipedia.org/wiki/Yacc_(logiciel)) (*Yet Another COmpiler-Compiler*) est un logiciel utilisé pour écrire des analyseurs syntaxiques de code. Il prend en entrée une grammaire.

Parce que les informaticiens ont de l'humour, Yacc à son pendant GNU [Bison](https://en.wikipedia.org/wiki/GNU_Bison) plus récent (1985) mais toujours activement développé.

Voici à titre d'information la définition formelle du langage C99 :

```text
--8<-- "docs/assets/src/c99.y
```

A partir de cette grammaire, Bison génère un fichier `c99.tab.c` qui contient le code C de l'analyseur syntaxique.

Pour la créer vous-même, vous pouvez utiliser la commande suivante :

```bash
bison -d -o c99.tab.c c99.y
```
