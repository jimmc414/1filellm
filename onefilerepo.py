import os
import requests
from pathlib import Path
import nbformat
from nbconvert import PythonExporter

TOKEN = "GITHUB_PERSONAL_ACCESS_TOKEN"
headers = {"Authorization": f"token {TOKEN}"}

def download_file(url, target_path):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(response.content)

def is_allowed_filetype(filename):
    allowed_extensions = ['.py', '.md', '.js', '.rst', '.ts', '.html', '.json', '.jsonl', 'ipynb']
#    allowed_extensions = ['.st','py']
    return any(filename.endswith(ext) for ext in allowed_extensions)

def process_ipynb_file(temp_file):
    with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
        notebook_content = f.read()

    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(nbformat.reads(notebook_content, as_version=4))
    return python_code

def process_directory(url, output):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()

    for file in files:
        if file["type"] == "file" and is_allowed_filetype(file["name"]):
            print(f"Processing {file['path']}...")

            temp_file = f"temp_{file['name']}"
            download_file(file["download_url"], temp_file)

            output.write(f"# {'-' * 30}\n")
            output.write(f"# Filename: {file['path']}\n")
            output.write(f"# {'-' * 30}\n\n")

            if file["name"].endswith(".ipynb"):
                output.write(process_ipynb_file(temp_file))
            else:
                with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
                    output.write(f.read())

            output.write("\n\n")
            os.remove(temp_file)
        elif file["type"] == "dir":
            process_directory(file["_links"]["self"], output)

def process_local_directory(local_path, output):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if is_allowed_filetype(file):
                print(f"Processing {os.path.join(root, file)}...")

                output.write(f"# {'-' * 30}\n")
                output.write(f"# Filename: {os.path.join(root, file)}\n")
                output.write(f"# {'-' * 30}\n\n")

                file_path = os.path.join(root, file)

                if file.endswith(".ipynb"):
                    output.write(process_ipynb_file(file_path))
                else:
                    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                        output.write(f.read())

                output.write("\n\n")

def process_github_repo(repo_url, output_file):
    api_base_url = "https://api.github.com/repos/"
    repo_name = repo_url.split("https://github.com/")[-1]
    contents_url = f"{api_base_url}{repo_name}/contents"

    with open(output_file, "w", encoding='utf-8') as output:
        process_directory(contents_url, output)

    print("All files processed.")

def process_local_folder(local_path, output_file):
    with open(output_file, "w", encoding='utf-8') as output:
        process_local_directory(local_path, output)

    print("All files processed.")

def process_input(input_path, output_file):
    if input_path.startswith("http"):
        process_github_repo(input_path, output_file)
    elif os.path.isdir(input_path):
        process_local_folder(input_path, output_file)
    else:
        print("Invalid input. Please provide a GitHub repo URL or a local folder path.")

if __name__ == "__main__":
    input_path = input("Enter GitHub repo URL or local folder path: ")
    output_filename = "concatenated_files.txt"
    process_input(input_path, output_filename)
