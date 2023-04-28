# Présentation du projet

Ce projet est une suite d'outils Python permettant de gérer et d'interagir avec des dépôts Git. Il vous permet d'afficher des informations telles que la liste des projets, des commits, des différences entre les commits et des branches.

## Installation

Pour utiliser ce projet, vous devez avoir Python 3 installé sur votre machine. Clonez simplement ce dépôt et vous êtes prêt à commencer.

## Configuration

Créez un fichier **'repositories.json'** à la racine du projet avec la structure suivante :

```
[
  {"name": "projet", "url": "git@github.com:amines17/git-tools.git"}
]
```
Remplacez les valeurs **'name'** et **'url'** par les informations correspondantes à vos propres projets.

Créez également un fichier **'.ignore'** à la racine du projet et ajoutez-y les extensions de fichiers que vous ne souhaitez pas traiter lors des comparaisons de différences (diff). Par exemple :

```
.xml
.css
.html
```
Cette configuration exclura les fichiers XML, CSS et HTML des résultats de la commande diff.

## Utilisation

Exécutez la commande suivante pour afficher l'aide du programme :

```bash
python3 tools.py
```

Voici les commandes disponibles :

## projets

Affiche la liste des projets disponibles.

```bash
python3 tools.py projets
```

## commits

Affiche la liste des commits du dépôt spécifié et de la branche spécifiée.

```bash
python3 tools.py commits <repository_name> <branch_name>
```

## diff

Affiche le diff entre les deux commits spécifiés pour le dépôt et la branche spécifiés.

```bash
python3 tools.py diff <repository_name> <branch_name> <commit1> <commit2>
```

## branches

Affiche la liste des branches du dépôt spécifié.

```bash
python3 tools.py branches <repository_name>
```

## Exemple d'utilisation

Pour afficher la différence entre les commits 3059 et 3061 de la branche origin/release-175.5.1 du dépôt projet, utilisez la commande suivante :

```bash
python3 tools.py projet diff origin/release-175.5.1 3059 3061
```

## Contribution

Si vous souhaitez contribuer à ce projet, n'hésitez pas à soumettre des issues ou des pull requests sur le dépôt Github.
