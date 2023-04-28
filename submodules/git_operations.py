from datetime import datetime
import git
import modules

repositories = modules.load_repositories()

def get_repository(repository_name: str):
    for repo in repositories:
        if repo['name'] == repository_name:
            try:
                return git.Repo(f"./projets/{repository_name}")
            except git.exc.NoSuchPathError:
                if repo['url'] is not None:
                    print(f"Le répertoire '{repository_name}' n'existe pas sur votre machine, il va être cloné")
                    return git.Repo.clone_from(repo['url'], f"./projets/{repository_name}")
                else:
                    print(f"Le répertoire {repository_name} n'a pas été trouvé et l'URL du dépôt est manquante.")
                    return None
    print(f"Repository {repository_name} non trouvé.")

def git_fetch(repository):
    if repository is not None:
        try:
            repository.remote().fetch()
        except git.exc.GitCommandError as e:
            print(f"Erreur lors de la récupération des dernières modifications: {e}")
            return None
    else:
        print("Erreur: L'objet repo est nul.")


def get_commits(repository, branch_name, verbose=True):
    git_fetch(repository)  
    if repository is not None:
        commits = list(repository.iter_commits(branch_name, reverse=True))
        if verbose:
            i = 0
            for commit in commits:
                committed_date = datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{i}]  Commit: {commit.hexsha} - Author: {commit.author} - Date: {committed_date} - Message: {commit.summary}")
                i+=1
        return commits
    else:
        print("Erreur: L'objet repo est nul.")


def get_branches(repository):
    if repository is not None:
        branches = [ref.name for ref in repository.remote().refs]
        i = 0
        for branch in branches:
            print(f"[{i}] Branch: {branch}")
            i += 1
    else:
        print("Erreur: L'objet repo est nul.")