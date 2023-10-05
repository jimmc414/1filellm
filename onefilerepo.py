import os
import re
import requests
import nltk
import tiktoken
from pathlib import Path
import nbformat
from nbconvert import PythonExporter
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from urllib.parse import urlparse

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

TOKEN = "GITHUB_PERSONAL_ACCESS_TOKEN"
headers = {"Authorization": f"token {TOKEN}"}

def download_file(url, target_path):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(response.content)

def is_allowed_filetype(filename):
#    allowed_extensions = ['.py', '.js', '.rst', '.sh', '.md', '.pyx', '.html', '.yaml', 'ipynb']
#    allowed_extensions = ['.py', '.txt', '.js', '.rst', '.sh', '.md', '.pyx', '.html', '.yaml','.json', '.jsonl', 'ipynb']
    allowed_extensions = ['.py', '.js', '.rst', '.sh', '.md', '.ini', '.html', '.yaml','.json', '.jsonl', 'ipynb']
#    allowed_extensions = ['.ipynb']
#    allowed_extensions = ['.yaml']
#    allowed_extensions = ['.md']
#    allowed_extensions = ['.py']
#    allowed_extensions = ['.rst']
#    allowed_extensions = ['.ts', '.md', '.js', '.rst', '.tsx', '.pxd', '.css', '.html', '.yaml','.json', '.jsonl', 'ipynb']
#    allowed_extensions = ['.ts', '.md', '.js', '.rst', '.tsx', '.pxd', '.jsonl', 'ipynb']
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

            output.write(f"# {'-' * 3}\n")
            output.write(f"# Filename: {file['path']}\n")
            output.write(f"# {'-' * 3}\n\n")

            if file["name"].endswith(".ipynb"):
                output.write(process_ipynb_file(temp_file))
            elif file["name"].endswith(".pdf"):
                # Check if the url domain is 'https://arxiv.org/'
                parsed_uri = urlparse(file["download_url"])
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                if domain == 'https://arxiv.org/':
                    # Modify the url to point to the pdf version
                    pdf_url = file["download_url"].replace("/abs/", "/pdf/") + ".pdf"
                    response = requests.get(pdf_url)
                    pdf_content = response.content

                    # Save the pdf file
                    with open('temp.pdf', 'wb') as pdf_file:
                        pdf_file.write(pdf_content)

                    # Open the pdf file and extract its text
                    with open('temp.pdf', 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                        for page in range(pdf_reader.getNumPages()):
                            output.write(pdf_reader.getPage(page).extractText())
            else:
                with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
                    output.write(f.read())

            output.write("\n\n")
            os.remove(temp_file)
        elif file["type"] == "dir":
            process_directory(file["url"], output)

def process_local_directory(local_path, output):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if is_allowed_filetype(file):
                print(f"Processing {os.path.join(root, file)}...")

                output.write(f"# {'-' * 3}\n")
                output.write(f"# Filename: {os.path.join(root, file)}\n")
                output.write(f"# {'-' * 3}\n\n")

                file_path = os.path.join(root, file)

                if file.endswith(".ipynb"):
                    output.write(process_ipynb_file(file_path))
                else:
                    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                        output.write(f.read())

                output.write("\n\n")

def process_github_repo(repo_url, output_file):
    # Check if the URL is a GitHub repo URL
    parsed_uri = urlparse(repo_url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if domain != 'https://github.com/':
        print("Invalid GitHub repo URL.")
        return

    api_base_url =     "https://api.github.com/repos/"
    repo_url_parts = repo_url.split("https://github.com/")[-1].split("/")
    repo_name = "/".join(repo_url_parts[:2])

    # Check if a subdirectory is provided
    subdirectory = ""
    if len(repo_url_parts) > 4 and repo_url_parts[2] == "tree":
        subdirectory = "/".join(repo_url_parts[4:])

    contents_url = f"{api_base_url}{repo_name}/contents"
    if subdirectory:
        contents_url = f"{contents_url}/{subdirectory}"

    with open(output_file, "w", encoding='utf-8') as output:
        process_directory(contents_url, output)
    print("All files processed.")

def process_local_folder(local_path, output_file):
    with open(output_file, "w", encoding='utf-8') as output:
        process_local_directory(local_path, output)

    print("All files processed.")

def process_arxiv_pdf(arxiv_abs_url, output_file):
    # Modify the url to point to the pdf version
    pdf_url = arxiv_abs_url.replace("/abs/", "/pdf/") + ".pdf"
    response = requests.get(pdf_url)
    pdf_content = response.content

    # Save the pdf file
    with open('temp.pdf', 'wb') as pdf_file:
        pdf_file.write(pdf_content)

    # Open the pdf file and extract its text
    with open('temp.pdf', 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = []
        for page in range(len(pdf_reader.pages)):
            text.append(pdf_reader.pages[page].extract_text())
        
    # Write the extracted text to the given output file
    with open(output_file, "w", encoding='utf-8') as output:
        output.write(' '.join(text))

    print("All files processed.")

def process_input(input_path, output_file):
    parsed_uri = urlparse(input_path)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    if domain == 'https://arxiv.org/':
        process_arxiv_pdf(input_path, output_file)
    elif domain == 'https://github.com/':
        process_github_repo(input_path, output_file)
    elif os.path.isdir(input_path):
        process_local_folder(input_path, output_file)
    else:
        print("Invalid input. Please provide a GitHub repo URL or a local folder path.")

def extract_links(input_file, output_file):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        urls = re.findall(url_pattern, content)
    
    with open(output_file, 'w', encoding='utf-8') as output:
        for url in urls:
            output.write(url + '\n')

def main():
    input_path = input("Enter GitHub repo URL or local folder path: ")
    output_filename = "concatenated_files.txt"
    process_input(input_path, output_filename)

    input_file_path = output_filename
    output_file_path = "output.txt"
    process_input_file(input_file_path, output_file_path)

    with open(output_file_path, "r") as f:
        text = f.read()

    token_count = get_token_count(text)
    print(f"The input text file has {token_count} tokens.")

    # Call extract_links only if the file exists
    if os.path.isfile(input_file_path):
        input_file = '.\concatenated_files.txt'
        output_file = 'links.txt'
        extract_links(input_file, output_file)
    else:
        print("The input file does not exist.")

def preprocess_text(text):
    text = re.sub(r"[\n\r]+", "\n", text)  # Remove duplicate line breaks
    text = re.sub(r"[^a-zA-Z0-9\s_.,!?:;@#$%^&*()+\-=[\]{}|\\<>`~'\"/]+", "", text)  # Remove unwanted characters
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = text.lower()  # Convert text to lowercase

    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = " ".join(words)

    return text.strip()

def process_input_file(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        input_text = input_file.read()

    cleaned_text = preprocess_text(input_text)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(cleaned_text)

def get_token_count(text):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    return len(tokens)

if __name__ == "__main__":
    input_path = input("Enter GitHub repo URL or local folder path: ")
    output_filename = "concatenated_files.txt"
    process_input(input_path, output_filename)

    input_file_path = output_filename
    output_file_path = "output.txt"
    process_input_file(input_file_path, output_file_path)

    with open(output_file_path, "r") as f:
        text = f.read()

    token_count = get_token_count(text)
    print(f"The input text file has {token_count} tokens.")
