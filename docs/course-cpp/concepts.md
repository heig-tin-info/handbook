# Concepts C++

**RVO (Return Value Optimization)**

: Optimisation du compilateur qui évite des copies inutiles lorsqu’une fonction retourne une valeur en construisant directement le résultat à l’emplacement final.

**RAII (Resource Acquisition Is Initialization)**

: Nom malheureux pour une idée essentielle : en C++, on acquiert la ressource lors de l’initialisation d’un objet et on la libère dans son destructeur. Même en cas d’exception, la ressource est donc restituée correctement.

**SFINAE (Substitution Failure Is Not An Error)**

: Mécanisme de métaprogrammation qui permet au compilateur d’éliminer une surcharge de fonction ou une spécialisation de classe lorsqu’une substitution de types échoue, sans déclencher d’erreur de compilation. Seules les alternatives valides restent alors candidates.

    ```cpp
    template <typename T>
    std::enable_if_t<std::is_integral_v<T>>
    foo(T value) {
        // Cette fonction n’est disponible que pour les types entiers (int, char, etc.).
    }

    template <typename T>
    std::enable_if_t<!std::is_integral_v<T>>
    foo(T value) {
        // Cette fonction ne peut être appelée que pour les types non entiers (double, float, etc.).
    }
    ```

Ce principe est largement utilisé pour activer ou désactiver des portions de code selon l’existence d’une méthode, d’un membre ou d’une propriété de type évaluée à la compilation.

**CRTP (Curiously Recurring Template Pattern)**

: Modèle de conception dans lequel une classe de base prend la classe dérivée en paramètre de template. Il permet d’exprimer du polymorphisme statique et de factoriser du code commun.

**Rule of Three**

: Si une classe définit un destructeur, un constructeur de copie ou un opérateur d’affectation, elle doit probablement définir les trois pour gérer correctement la ressource sous-jacente.

**Rule of Five**

: Avec C++11 et suivants, si une classe définit l’une des fonctions spéciales (destructeur, constructeur de copie, opérateur d’affectation, constructeur de déplacement ou opérateur de déplacement), elle devrait généralement toutes les définir pour garantir une gestion cohérente des ressources.

**Rule of Zero**

: Idéalement, une classe qui ne gère pas directement de ressource ne définit aucune fonction spéciale. En s’appuyant sur les conteneurs de la bibliothèque standard et les pointeurs intelligents, on laisse C++ gérer automatiquement l’acquisition et la libération des ressources.

**As-if Rule**

: Principe qui autorise le compilateur à transformer le code tant que le comportement observable reste identique à celui du programme source. Le compilateur peut réordonner des instructions, supprimer des opérations redondantes ou insérer des optimisations, du moment que le résultat final perçu par l’utilisateur est inchangé.
