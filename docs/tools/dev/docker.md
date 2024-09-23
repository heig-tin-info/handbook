# Docker

## Introduction

![Docker](/assets/images/docker.png)

Docker est une plateforme logicielle qui permet de créer, de tester et de déployer des applications dans des **conteneurs logiciels**. Un conteneur est une unité logicielle qui contient une application et toutes ses dépendances. Les conteneurs sont légers, portables et auto-suffisants. Ils sont exécutés dans un environnement isolé de l'hôte.

C'est une alternative à la virtualisation (comme VirtualBox ou VMware) vue comme beaucoup plus légère et plus rapide. Docker est devenu un outil incontournable pour les développeurs et les administrateurs système.

Sous Windows, Docker dépend de la technologie Hyper-V qui permet de créer des machines virtuelles. Sous Linux, Docker utilise les fonctionnalités de virtualisation du noyau Linux. Dans les versions récentes, Docker est basé sur WSL 2 (Windows Subsystem for Linux 2) qui permet d'exécuter un noyau Linux complet dans Windows.

Pour utiliser docker il y a deux notions à comprendre :

- **Images** : une image est un modèle de conteneur. C'est un fichier binaire qui contient toutes les dépendances nécessaires pour exécuter une application. Les images sont stockées dans un registre (comme Docker Hub) et peuvent être partagées.
- **Conteneurs** : un conteneur est une instance d'une image. C'est une application en cours d'exécution avec son propre environnement isolé. Les conteneurs peuvent être créés, démarrés, arrêtés, déplacés et supprimés.

Imaginons que nous souhaitions exécuter une application Python qui utilise numpy sur une machine qui n'a pas Python d'installé. Nous pourrions créer une image Docker qui contient Python et numpy, puis exécuter un conteneur basé sur cette image. L'application fonctionnera sans problème, même si Python n'est pas installé sur la machine hôte.

```bash
docker run python:3.8-slim python -c "import numpy; print(numpy.__version__)"
```