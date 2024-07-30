# Bases {#my-heading}

## Exercices de révision

\begin{description}
\item[\mintinline{text}|<storage-class>|]
Classe de stockage, elle n'est pas utile à ce stade du cours, nous aborderons plus tard les mots clés \mintinline{text}|extern|, \mintinline{text}|static| et \mintinline{text}|inline|.


\item[\mintinline{text}|<return-type>|]
Le type de retour de la fonction, s'agit-il d'un \mintinline{text}|int|, d'un \mintinline{text}|float| ? Le type de retour est anonyme, il n'a pas de nom et ce n'est pas nécessaire.


\item[\mintinline{text}|<function-name>|]
Il s'agit d'un identificateur (c.f. \ref{identifier}) qui représente le nom de la fonction. Généralement on préfère choisir un verbe, quelquefois associé à un nom~: \mintinline{text}|compute_norm|, \mintinline{text}|make_coffee|, ... Néanmoins, lorsqu'il n'y a pas d'ambigüité, on peut choisir des termes plus simples tels que \mintinline{text}|main|, \mintinline{text}|display| ou \mintinline{text}|dot_product|.


\item[\mintinline{text}|<parameter-type> <parameter-name>|]
La fonction peut prendre en paramètre zéro à plusieurs paramètres où chaque paramètre est défini par son type et son nom tel que~: \mintinline{text}|double real, double imag| pour une fonction qui prendrait en paramètre un nombre complexe.


\item[Prototype]
On clos la déclaration avec un \mintinline{text}|;|


\item[Implémentation]
On poursuit avec l'implémentation du code \mintinline{text}|{ ... }|



\end{description}
Après la fermeture de la parenthèse de la liste des paramètres, deux possibilités~:

\begin{description}
\item[Prototype]
On clos la déclaration avec un \mintinline{text}|;|


\item[Implémentation]
On poursuit avec l'implémentation du code \mintinline{text}|{ ... }|



\end{description}