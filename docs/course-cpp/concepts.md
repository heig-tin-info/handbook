# Concepts C++

RVO (Return Value Optimization)

: Il s'agit d'une optimisation du compilateur qui permet d'éviter des copies inutiles lors du retour d'une valeur.

RAII (Resource Acquisition Is Initialization)

: Un très mauvais nom pour un concept très important. En C++, la ressource est acquise lors de l'initialisation d'un objet et libérée lors de sa destruction. Cela permet de garantir que la ressource est libérée même en cas d'exception.

SFINAE (Substitution Failure Is Not An Error)

:   Le SFINAE (Substitution Failure Is Not An Error) est une caractéristique des templates en C++ permettant une sélection conditionnelle de fonctions et de classes en fonction des types de paramètres fournis. SFINAE signifie que si, lors de la substitution des types dans un template, le code résultant est incorrect, cela n’entraîne pas d’erreur de compilation mais élimine simplement cette option de l'ensemble des solutions possibles.

    ```cpp
    template <typename T>
    typename std::enable_if<std::is_integral<T>::value>::type
    foo(T value) {
        // Cette fonction ne sera disponible que pour les types intégral (int, char, etc.)
    }

    template <typename T>
    typename std::enable_if<!std::is_integral<T>::value>::type
    foo(T value) {
        // Cette fonction ne sera disponible que pour les types non-intégral (double, float, etc.)
    }
    ```

Cette technique est souvent utilisée pour réaliser des sélections de fonctions en fonction de critères spécifiques, comme l’existence d’une méthode particulière ou l’évaluation de types lors de la compilation.

CRTP (Curiously Recurring Template Pattern)

: Un design pattern en C++ qui permet d'implémenter des classes de base qui dépendent de la classe dérivée.

Rule of Three

: En C++, si une classe définit un destructeur, un constructeur de copie ou un opérateur d'affectation, elle devrait probablement définir les trois.

Rule of Five

: En C++, si une classe définit un destructeur, un constructeur de copie, un opérateur d'affectation, un constructeur de déplacement ou un opérateur de déplacement, elle devrait probablement définir les cinq.

Rule of Zero

: En C++, si une classe ne gère pas de ressources, elle ne devrait pas définir de destructeur, de constructeur de copie ou d'opérateur d'affectation. Avec les outils modernes de C++ (comme les smart pointers et les conteneurs de la bibliothèque standard), il est possible d’éviter complètement de gérer manuellement les ressources. La "Rule of Zero" signifie que vous n'avez besoin de définir aucune des fonctions spéciales (constructeur de copie, destructeur, etc.) si vous utilisez des types RAII et les outils de la STL. La classe se concentrera uniquement sur sa logique métier, tandis que la bibliothèque standard gérera les ressources.

AS-IF Rule

: L’As-if rule est une règle d’optimisation en C++ qui permet aux compilateurs de transformer le code de manière à optimiser les performances, tant que le comportement observable du programme reste le même pour l’utilisateur. En d'autres termes, le compilateur peut modifier le code généré (par exemple, en supprimant des opérations redondantes, en modifiant l’ordre des instructions, ou en inlining des fonctions) tant que le résultat final est comme si le code original avait été exécuté sans modification.

Cela permet au compilateur d'appliquer des optimisations sans affecter l'exactitude de l'exécution du programme du point de vue de l'utilisateur.
