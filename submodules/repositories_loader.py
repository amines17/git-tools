import sys
import json

def load_repositories():
    try:
        with open('repositories.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Erreur: Le fichier 'repositories.json' est introuvable.")
        sys.exit(1)

repositories = load_repositories()

def load_ignore_extensions(ignore_file: str = ".ignore") -> list:
    extensions = []
    try:
        with open(ignore_file, "r") as f:
            extensions = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Le fichier {ignore_file} est introuvable.")
    return extensions

def get_projects():
    i = 0
    for repo in repositories:
        i+=1
        print(f"[{i}] ** {repo['name']}")