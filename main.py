import subprocess
import pandas as pd
import os
from datetime import datetime

def run_git_log_command(repo_path, author, since_date, diff_filter, repo_name):
    print(f"Obtendo logs do repositório '{repo_name}'...")
    command = (
        f"cd {repo_path} && "
        f"git log --name-only --diff-filter={diff_filter} --since={since_date} "
        f"--all --pretty=format:\"'%ad','%s#%H'\" --date=format:'%Y-%m-%d%H:%M:%S' --author={author}"
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Logs do repositório '{repo_name}' obtidos com sucesso.")
    return result.stdout

def parse_git_log(git_log_output, repo_name):
    print(f"Analisando logs do repositório '{repo_name}'...")
    lines = git_log_output.split('\n')
    data = []
    current_commit = None

    for line in lines:
        if line.startswith("'"):
            date, message = line.strip().split("','")
            date = date.strip("'")
            message, commit_hash = message.rsplit('#', 1)
            commit_hash = commit_hash[:10]
            date_obj = datetime.strptime(date, '%Y-%m-%d%H:%M:%S')
            date_year_month_day = date_obj.strftime('%Y-%m-%d')
            current_commit = {'date': date_year_month_day, 'message': message, 'commit_hash': commit_hash, 'files': []}
        elif line.strip() and current_commit:
            file_path = line.strip()
            formatted_entry = f"{repo_name}/{file_path}#{current_commit['commit_hash']}".rstrip("'")
            extension = os.path.splitext(file_path)[1].lower() if file_path else None
            date_obj = datetime.strptime(current_commit['date'], '%Y-%m-%d')
            date_year_month_day = date_obj.strftime('%Y-%m-%d')
            data.append({'date': date_year_month_day, 'repository': repo_name, 'path': formatted_entry, 'extension': extension})

    print(f"Logs do repositório '{repo_name}' analisados com sucesso.")
    return data

def save_to_excel(data, output_excel_file, sheet_name):
    df = pd.DataFrame(data)
    print(f"Salvando dados no arquivo '{output_excel_file}'...")
    if os.path.exists(output_excel_file):
        with pd.ExcelWriter(output_excel_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(output_excel_file, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Dados salvos no arquivo '{output_excel_file}'.")

def read_repo_list_from_file(file_path):
    repo_list = []
    with open(file_path, 'r') as file:
        for line in file:
            repo_info = line.strip().split(',')
            if len(repo_info) == 2:
                repo_list.append({'name': repo_info[0], 'path': repo_info[1]})
            else:
                print(f"Ignorando linha inválida: {line}")
    return repo_list

def process_repositories(repo_list, author, since_date):
    all_modifications_data = []
    all_additions_data = []
    
    ignored_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.json', '.ttf','.tff', '.woff', '.woff2', '.eot', '.svg', '.ico', '.mp4', '.mp3', '.wav', '.avi', '.mov', '.webm', '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.exe', '.dll', '.so', '.a', '.lib', '.obj', '.o', '.pyc', '.class', '.jar', '.war', '.ear', '.tar.gz', '.tar.bz2', '.tar.xz', '.tar.zst', '.tar.lz', '.tar.lzma', '.tar.sz', '.tar.lzo', '.tar.lz4', '.tar.zstd', '.txt']
    
    for repo in repo_list:
        repo_path = repo['path']
        repo_name = repo['name']
        
        modifications_output = run_git_log_command(repo_path, author, since_date, 'M', repo_name)
        additions_output = run_git_log_command(repo_path, author, since_date, 'A', repo_name)
        
        modifications_data = parse_git_log(modifications_output, repo_name)
        additions_data = parse_git_log(additions_output, repo_name)

        modifications_data = [entry for entry in modifications_data if entry['extension'] not in ignored_extensions]
        additions_data = [entry for entry in additions_data if entry['extension'] not in ignored_extensions]

        all_modifications_data.extend(modifications_data)
        all_additions_data.extend(additions_data)

    output_excel_file = 'all_repositories_commits.xlsx'
    save_to_excel(all_modifications_data, output_excel_file, 'Modifications')
    save_to_excel(all_additions_data, output_excel_file, 'Additions')

print("Iniciando o processamento dos repositórios...")
repo_list_file = 'repositories.txt'
with open('entry.txt', 'r') as entry_file:
    entry_data = entry_file.readlines()

for line in entry_data:
    if line.startswith('author='):
        author = line.strip().split('=')[1]
    elif line.startswith('since_date='):
        since_date = line.strip().split('=')[1]

repo_list = read_repo_list_from_file(repo_list_file)

process_repositories(repo_list, author, since_date)
print("Processamento concluído.")
