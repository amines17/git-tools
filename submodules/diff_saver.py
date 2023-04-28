import modules
import re
import sys
import os
import json

def get_diff(repository, branch_name):
    if len(sys.argv) > 5:
        try:
            commit1_index = int(sys.argv[4])
            commit2_index = int(sys.argv[5])
        except ValueError:
            print("Les index des commits doivent être des entiers.")
            return

        ignore_extensions = modules.load_ignore_extensions()
        commits = modules.get_commits(repository, branch_name, verbose=False)

        if commit1_index >= len(commits) or commit2_index >= len(commits):
            print("L'un des index des commits est en dehors de la plage valide.")
            return

        commit1 = commits[commit1_index].hexsha
        commit2 = commits[commit2_index].hexsha

        diff = repository.git.diff(f'{commit1}..{commit2}', '--patch', branch_name)

        if ignore_extensions:
            diff_lines = diff.splitlines()
            filtered_diff_lines = []
            ignoring_file_diff = False
            for line in diff_lines:
                if line.startswith("diff"):
                    ignoring_file_diff = False
                if line.startswith("+++") or line.startswith("---"):
                    filename = line[4:]
                    if any(filename.endswith(ext) for ext in ignore_extensions):
                        ignoring_file_diff = True
                        continue
                if not ignoring_file_diff:
                    filtered_diff_lines.append(line)
                if line.startswith("diff"):
                    ignoring_file_diff = False
            diff = "\n".join(filtered_diff_lines)

        return save_diff(diff, repository, commit1_index, commit2_index)
    else:
        print("Aucun argument en paramètre fourni.")

def should_ignore_diff_line(line, ignored_extensions):
    for ext in ignored_extensions:
        if line.endswith(ext[1:]):  # Remove the '*' in the extension
            return True
    return False

def save_diff(diff, repository, commit1_index, commit2_index, ignore_file: str = ".ignore"):
    repository_name = os.path.basename(repository.working_tree_dir)
    ignored_extensions = modules.load_ignore_extensions(ignore_file)

    output_directory = f"diff/{repository_name}/{commit1_index}_{commit2_index}"

    os.makedirs(output_directory, exist_ok=True)
    lines = diff.splitlines()
    formatted_lines = []
    line_counter = 1
    modified_files = []

    class_pattern = re.compile(r'@@.*@@\s*(.*)(?=\s*{)')

    current_file = None
    for line in lines:
        if line.startswith('diff'):
            if should_ignore_diff_line(line, ignored_extensions):
                continue

            formatted_lines.append('\n' + '='*80 + '\n')
            formatted_lines.append(line + '\n')
            line_counter = 1
        elif line.startswith('index'):
            pass
        elif line.startswith('---'):
            formatted_lines.append(line + '\n')
        elif line.startswith('+++'):
            formatted_lines.append(line + '\n')
            filename = line[6:]
            current_file = {'file': filename, 'classes': set()}
            modified_files.append(current_file)
        elif line.startswith('-'):
            formatted_lines.append(f"\033[91m- [{line_counter}] {line[1:]}\033[0m\n")  # Red color for removed lines
            line_counter += 1
        elif line.startswith('+'):
            formatted_lines.append(f"\033[92m+ [{line_counter}] {line[1:]}\033[0m\n")  # Green color for added lines
            line_counter += 1
        else:
            if line.startswith('@@'):
                match = class_pattern.match(line)
                if match:
                    current_file['classes'].add(match.group(1))

            formatted_lines.append(line + '\n')
            line_counter += 1

    with open(f"{output_directory}/{commit1_index}_{commit2_index}.txt", 'w') as f:
        f.writelines(formatted_lines)

    # Convert the sets of classes to lists for JSON serialization
    for modified_file in modified_files:
        modified_file['classes'] = list(modified_file['classes'])

    with open(f"{output_directory}/{commit1_index}_{commit2_index}_modified_files.json", 'w') as json_file:
        json.dump(modified_files, json_file)

    print('Un fichier a été généré !')
    print(f"{output_directory}/{commit1_index}_{commit2_index}.txt")
    print(f"{output_directory}/{commit1_index}_{commit2_index}_modified_files.json")