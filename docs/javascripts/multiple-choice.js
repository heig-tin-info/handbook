document.addEventListener("DOMContentLoaded", function() {
    // Sélectionner tous les éléments de la liste
    const taskItems = document.querySelectorAll(".task-list-item");

    // Ajouter un événement de clic à chaque élément de la liste
    taskItems.forEach(item => {
        const checkbox = item.querySelector("input[type='checkbox']");
        checkbox.disabled = false; // Réactiver la case à cocher

        item.addEventListener("click", function() {
            // Déterminer si c'est la bonne réponse (input checked dans le HTML initial)
            const isCorrect = checkbox.checked;

            if (isCorrect) {
                item.classList.add("correct");
            } else {
                item.classList.add("incorrect");
            }

            // Désactiver à nouveau la case à cocher après le clic pour éviter les modifications ultérieures
            checkbox.disabled = true;
        });
    });
});