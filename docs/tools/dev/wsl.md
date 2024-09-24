# Windows Subsystem for Linux

Windows Subsystem for Linux est un outil qui permet d'exécuter des applications Linux sur Windows. Il est disponible sur Windows 10 et Windows Server 2019.

Face à l'augmentation de la popularité de Linux, Microsoft a décidé de créer un outil permettant d'exécuter des applications Linux sur Windows. Cela permet aux développeurs de travailler sur des projets Linux sans avoir à quitter Windows.

Cela tombe bien, la plupart des outils de développement sont disponibles sur Linux. Par exemple, vous pouvez utiliser des outils comme Git, Node.js, Python, Ruby, etc.

## Résolution des problèmes

### J'ai oublié mon mot de passe

Si vous êtes sur un vrai linux et que vous avez oublié votre mot de passe utilisateur, vous pouvez utiliser le compte `root`, et si vous avez oublié le mot de passe de `root` vous êtes dans la mouise.

Sur Windows, il n'y a pas de mot de passe `root`, et pour entrer dans ce mode voici les étapes: 

1. Exécutez une fenêtre `cmd.exe` en tant qu'administrateur
2. Exécutez `wsl -l` pour lister les distributions WSL installées
3. Exécutez la commande `wsl -d nom_distribution -u root` (remplacez `nom_distribution` par le nom de votre distribution). Si vous avez installé `Ubuntu-24.04`, ce sera `wsl -d Ubuntu-24.04 -u root`
4. Vous êtes maintenant dans le mode `root` et vous pouvez changer le mot de passe de n'importe quel utilisateur avec `passwd nom_utilisateur` (remplacez `nom_utilisateur` par le nom de l'utilisateur)
5. Si ne vous rappellez pas du nom de l'utilisateur, vous pouvez lister les utilisateurs avec `cat /etc/passwd | cut -d: -f1 | tail -n5`, votre utilisateur devrait être un des cinq derniers.

Une fois le mot de passe changé, vous pouvez vous reconnecter avec votre utilisateur.

### En root par défaut

Si, lorsque vous lancer WSL, vous êtes en mode `root`, c'est que vous avez échoué à créer un utilisateur lors de l'installation de WSL, probablement en annulant la saisie du mot de passe.

Pour résoudre ce problème : 

1. Exécutez Ubuntu (vous serez en mode super-utilisateur)
2. Créez un utilisateur avec `adduser nom_utilisateur` (remplacez `nom_utilisateur` par le nom de l'utilisateur), choisissez un nom d'utilisateur simple, en minusucule, sans espace ni caractères spéciaux
3. Suivez les instructions pour définir un mot de passe
4. Ajoutez l'utilisateur au groupe `sudo` avec `usermod -aG sudo nom_utilisateur`
5. Pour configurer cet utilisateur comme utilisateur par défaut, exécutez `ubuntu config --default-user nom_utilisateur` (remplacez `nom_utilisateur` par le nom de l'utilisateur)
