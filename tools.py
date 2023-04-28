import sys
import modules

repositories = modules.load_repositories()

def print_help():
    print("usage : tools.py [repository_name] [projets/commits/diff/branches] [branch_name] [arg1] [arg2] ")
    print("Utilisation : python3 tools.py <command> [arguments]")
    print("\nListe des commandes disponibles :")
    print("\nprojets")
    print("  Affiche la liste des projets disponibles.")
    print("\ncommits <repository_name> <branch_name>")
    print("  Affiche la liste des commits du dépôt spécifié et de la branche spécifiée.")
    print("\ndiff <repository_name> <branch_name> <commit1> <commit2>")
    print("  Affiche le diff entre les deux commits spécifiés pour le dépôt et la branche spécifiés.")
    print("\nbranches <repository_name>")
    print("  Affiche la liste des branches du dépôt spécifié.")
    print("\nExemple :")
    print("  python3 tools.py cleanweb2 diff origin/release-175.5.1 3059 3061")

def call_module(argument: str, repository_name: str, branch_name: str):
    repo = modules.get_repository(repository_name)

    if argument == "commits":
        return modules.get_commits(repo, branch_name)
    elif argument == "diff":
        return modules.get_diff(repo, branch_name) 
    elif argument == "branches":
        return modules.get_branches(repo)
    else:
        print_help()   

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'projets':
            modules.get_projects()
        elif sys.argv[1] == 'help':
            print_help()
        elif len(sys.argv) > 2:
            argument = sys.argv[2]
            repository_name = sys.argv[1]
            branch_name = sys.argv[3] if len(sys.argv) > 3 else None
            call_module(argument, repository_name, branch_name)
    else:
        print_help()

if __name__ == '__main__':
    main()