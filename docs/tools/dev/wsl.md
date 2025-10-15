# Windows Subsystem for Linux

Windows Subsystem for Linux est un outil qui permet d'exécuter des applications Linux sur Windows. Il est disponible sur Windows 10 et Windows Server 2019.

Face à l'augmentation de la popularité de Linux, Microsoft a décidé de créer un outil permettant d'exécuter des applications Linux sur Windows. Cela permet aux développeurs de travailler sur des projets Linux sans avoir à quitter Windows.

Cela tombe bien, la plupart des outils de développement sont disponibles sur Linux. Par exemple, vous pouvez utiliser des outils comme Git, Node.js, Python, Ruby, etc.

## F.A.Q Résolution des problèmes

### J'ai oublié mon mot de passe ?

Si vous êtes sur un vrai linux et que vous avez oublié votre mot de passe utilisateur, vous pouvez utiliser le compte `root`, et si vous avez oublié le mot de passe de `root` vous êtes dans la mouise.

Sur Windows, il n'y a pas de mot de passe `root`, et pour entrer dans ce mode voici les étapes:

1. Exécutez une fenêtre `cmd.exe` en tant qu'administrateur
2. Exécutez `wsl -l` pour lister les distributions WSL installées
3. Exécutez la commande `wsl -d nom_distribution -u root` (remplacez `nom_distribution` par le nom de votre distribution). Si vous avez installé `Ubuntu-24.04`, ce sera `wsl -d Ubuntu-24.04 -u root`
4. Vous êtes maintenant dans le mode `root` et vous pouvez changer le mot de passe de n'importe quel utilisateur avec `passwd nom_utilisateur` (remplacez `nom_utilisateur` par le nom de l'utilisateur)
5. Si ne vous rappellez pas du nom de l'utilisateur, vous pouvez lister les utilisateurs avec `cat /etc/passwd | cut -d: -f1 | tail -n5`, votre utilisateur devrait être un des cinq derniers.

Une fois le mot de passe changé, vous pouvez vous reconnecter avec votre utilisateur.

### En root par défaut ?

Si, lorsque vous lancer WSL, vous êtes en mode `root`, c'est que vous avez échoué à créer un utilisateur lors de l'installation de WSL, probablement en annulant la saisie du mot de passe.

Pour résoudre ce problème :

1. Exécutez Ubuntu (vous serez en mode super-utilisateur)
2. Créez un utilisateur avec `adduser nom_utilisateur` (remplacez `nom_utilisateur` par le nom de l'utilisateur), choisissez un nom d'utilisateur simple, en minusucule, sans espace ni caractères spéciaux
3. Suivez les instructions pour définir un mot de passe
4. Ajoutez l'utilisateur au groupe `sudo` avec `usermod -aG sudo nom_utilisateur`
5. Pour configurer cet utilisateur comme utilisateur par défaut, exécutez `ubuntu config --default-user nom_utilisateur` (remplacez `nom_utilisateur` par le nom de l'utilisateur)

### J'ai des fichiers Zone.Identifier ?

Si vous avez des fichiers avec l'extension `:Zone.Identifier`, c'est que vous avez téléchargé des fichiers depuis Internet, et Windows a ajouté cette extension pour des raisons de sécurité. Ces fichiers sont utiles à Windows Defender (votre antivirus) pour savoir si le fichier est sûr ou non.

En effet, Windows ajoute cette extension pour indiquer que le fichier provient d'une source externe et peut potentiellement être dangereux.

Lorsque vous copiez des fichiers depuis Windows vers WSL, ces extensions sont également copiées. En pratique elle ne servent à rien d'utile et même elle encombrent et risquent de se retrouver sur Git.

La mauvaise nouvelle est qu'il n'y a pas d'option pour désactiver cette fonctionnalité de Windows juste pour WSL. Néanmoins vous pouvez vous protéger en :

1. Supprimant ces fichiers récursivement dans votre arborescence WSL avec la commande suivante (à exécuter dans WSL) :

   ```bash
   find /path/to/your/directory -name "*:Zone.Identifier" -exec rm {} \;
   ```

   Remplacez `/path/to/your/directory` par le chemin de votre répertoire.

2. En configurant Git pour ignorer ces fichiers en ajoutant la ligne suivante à votre fichier `.gitignore` :

   ```text
   *:Zone.Identifier
   ```

### Quand je lance WSL depuis l'explorateur je suis dans mon home ?

C'est le comportement par défaut de WSL. Lorsque vous lancez WSL depuis l'explorateur de fichiers, il vous place dans votre répertoire personnel (`/home/votre_utilisateur`), même si vous avez sélectionné l'option "Ouvrir dans Windows Terminal".

Par défaut WSL appelle Windows Terminal dans votre profile par défaut, et souvent Ubuntu est lancé avec `ubuntu2404.exe` et non `wsl.exe -d Ubuntu-24.04`.

Malheureusement `ubuntu2404.exe` n'accepte pas les options pour changer le répertoire de démarrage. En remplaceant `ubuntu2404.exe` par `wsl.exe -d Ubuntu-24.04` dans le profil Windows Terminal, vous résolvez le problème.
