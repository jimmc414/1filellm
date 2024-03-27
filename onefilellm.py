import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin, urlparse
from PyPDF2 import PdfReader
import os
import tiktoken
import nltk
from nltk.corpus import stopwords
import re
from pathlib import Path
import nbformat
from nbconvert import PythonExporter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import pyperclip
import wget
from tqdm import tqdm
from time import sleep
from dotenv import load_dotenv
load_dotenv()

def safe_file_read(filepath, fallback_encoding='latin1'):
    try:
        with open(filepath, "r", encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding=fallback_encoding) as file:
            return file.read()

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))


def download_file(url, target_path, headers):
    response = requests.get(url, headers)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(response.content)

def is_allowed_filetype(filename):
    allowed_extensions = ['.tsx', '.ts', '.py', '.txt', '.js', '.rst', '.sh', '.md', '.pyx', '.html', '.yaml', '.json', '.jsonl', '.ipynb', '.h', '.c', '.sql', '.csv']
    return any(filename.endswith(ext) for ext in allowed_extensions)

def process_ipynb_file(temp_file):
    with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
        notebook_content = f.read()

    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(nbformat.reads(notebook_content, as_version=4))
    return python_code

def process_directory(url, output, headers):
    response = requests.get(url, headers)
    response.raise_for_status()
    files = response.json()

    for file in files:
        if file["type"] == "file" and is_allowed_filetype(file["name"]):
            print(f"Processing {file['path']}...")

            temp_file = f"temp_{file['name']}"
            download_file(file["download_url"], temp_file, headers)

            output.write(f"# {'-' * 3}\n")
            output.write(f"# Filename: {file['path']}\n")
            output.write(f"# {'-' * 3}\n\n")

            if file["name"].endswith(".ipynb"):
                output.write(process_ipynb_file(temp_file))
            else:
                with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
                    output.write(f.read())

            output.write("\n\n")
            os.remove(temp_file)
        elif file["type"] == "dir":
            process_directory(file["url"], output, headers)

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
    TOKEN = os.getenv('GITHUB_TOKEN', 'default_token_here')
    if TOKEN == 'default_token_here':
        raise EnvironmentError("GITHUB_TOKEN environment variable not set.")
    headers = {"Authorization": f"token {TOKEN}"}
    api_base_url = "https://api.github.com/repos/"
    repo_url_parts = repo_url.split("https://github.com/")[-1].split("/")
    repo_name = "/".join(repo_url_parts[:2])

    subdirectory = ""
    if len(repo_url_parts) > 4 and repo_url_parts[2] == "tree":
        subdirectory = "/".join(repo_url_parts[4:])

    contents_url = f"{api_base_url}{repo_name}/contents"
    if subdirectory:
        contents_url = f"{contents_url}/{subdirectory}"

    with open(output_file, "w", encoding='utf-8') as output:
        process_directory(contents_url, output, headers)
    print("All files processed.")

def process_local_folder(local_path, output_file):
    with open(output_file, "w", encoding='utf-8') as output:
        process_local_directory(local_path, output)

    print("All files processed.")

def process_arxiv_pdf(arxiv_abs_url, output_file):
    pdf_url = arxiv_abs_url.replace("/abs/", "/pdf/") + ".pdf"
    response = requests.get(pdf_url)
    pdf_content = response.content

    with open('temp.pdf','wb') as pdf_file:
        pdf_file.write(pdf_content)

    text = []
    with open('temp.pdf', 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page in range(len(pdf_reader.pages)):
            text.append(pdf_reader.pages[page].extract_text())

    with open(output_file, "w", encoding='utf-8') as output:
        output.write(' '.join(text))

    print("All files processed.")

def extract_links(input_file, output_file):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        urls = re.findall(url_pattern, content)
    
    with open(output_file, 'w', encoding='utf-8') as output:
        for url in urls:
            output.write(url + '\n')

def fetch_youtube_transcript(url):
    def extract_video_id(url):
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return None

    video_id = extract_video_id(url)
    if not video_id:
        return "Error: Could not extract video ID from URL."

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript = formatter.format_transcript(transcript_list)
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"

def preprocess_text(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as input_file:
        input_text = input_file.read()

    text = re.sub(r"[\n\r]+", "\n", input_text)
    text = re.sub(r"[^a-zA-Z0-9\s_.,!?:;@#$%^&*()+\-=[\]{}|\\<>`~'\"/]+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()

    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = " ".join(words)

    with open(output_file, "w", encoding="utf-8") as output_file:
        output_file.write(text.strip())

def get_token_count(text):
    enc = tiktoken.get_encoding("cl100k_base")
    disallowed_special = enc.special_tokens_set - {''}
    tokens = enc.encode(text, disallowed_special=disallowed_special)
    return len(tokens)

def is_same_domain(base_url, new_url):
    return urlparse(base_url).netloc == urlparse(new_url).netloc

def is_within_depth(base_url, current_url, max_depth):
    base_parts = urlparse(base_url).path.rstrip('/').split('/')
    current_parts = urlparse(current_url).path.rstrip('/').split('/')

    if current_parts[:len(base_parts)] != base_parts:
        return False

    return len(current_parts) - len(base_parts) <= max_depth

def process_pdf(url):
    response = requests.get(url)
    response.raise_for_status()

    with open('temp.pdf', 'wb') as pdf_file:
        pdf_file.write(response.content)

    text = []
    with open('temp.pdf', 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page in range(len(pdf_reader.pages)):
            text.append(pdf_reader.pages[page].extract_text())

    os.remove('temp.pdf')
    return ' '.join(text)

def crawl_and_extract_text(base_url, output_file, urls_list_file, max_depth, include_pdfs, ignore_epubs):
    visited_urls = set()
    urls_to_visit = [(base_url, 0)]
    processed_urls = []
    all_text = ""

    while urls_to_visit:
        current_url, current_depth = urls_to_visit.pop(0)
        clean_url = current_url.split('#')[0]

        if clean_url not in visited_urls and is_same_domain(base_url, clean_url) and is_within_depth(base_url, clean_url, max_depth):
            if ignore_epubs and clean_url.endswith('.epub'):
                continue

            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                visited_urls.add(clean_url)

                if clean_url.endswith('.pdf') and include_pdfs:
                    text = process_pdf(clean_url)
                else:
                    for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
                        element.decompose()
                    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                    for comment in comments:
                        comment.extract()
                    text = soup.get_text(separator='\n', strip=True)

                all_text += f"\n\n# URL: {clean_url}\n{text}"
                processed_urls.append(clean_url)
                print(f"Processed: {clean_url}")

                if current_depth < max_depth:
                    for link in soup.find_all('a', href=True):
                        new_url = urljoin(current_url, link['href']).split('#')[0]
                        if new_url not in visited_urls and is_within_depth(base_url, new_url, max_depth) and (include_pdfs or not new_url.endswith('.pdf')) and not (ignore_epubs and new_url.endswith('.epub')):
                            urls_to_visit.append((new_url, current_depth + 1))

            except requests.RequestException as e:
                print(f"Failed to retrieve {clean_url}: {e}")

    processed_urls_string = '\n'.join(processed_urls)
    header = f"Generated text from the website: {base_url}. This includes content from the base page and all linked pages up to {max_depth} levels deep.\nProcessed URLs:\n{processed_urls_string}\n\n"
    
    all_text = header + all_text

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(all_text)

    with open(urls_list_file, 'w', encoding='utf-8') as urls_file:
        for url in processed_urls:
            urls_file.write(url + '\n')

    return all_text

def process_doi_or_pmid(identifier, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Connection': 'keep-alive'
    }

    try:
        payload = {
            'sci-hub-plugin-check': '',
            'request': identifier
        }

        base_url = 'https://sci-hub.se/'
        response = requests.post(base_url, headers=headers, data=payload, timeout=60)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find(id='pdf').get('src').replace('#navpanes=0&view=FitH', '').replace('//', '/')

        if content.startswith('/downloads'):
            pdf_url = 'https://sci-hub.se' + content
        elif content.startswith('/tree'):
            pdf_url = 'https://sci-hub.se' + content
        elif content.startswith('/uptodate'):
            pdf_url = 'https://sci-hub.se' + content
        else:
            pdf_url = 'https:/' + content

        pdf_filename = f"{identifier.replace('/', '-')}.pdf"
        wget.download(pdf_url, pdf_filename)

        with open(pdf_filename, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

        with open(output_file, "w", encoding='utf-8') as output:
            output.write(text)

        os.remove(pdf_filename)
        print(f"Identifier {identifier} processed successfully.")
    except Exception as e:
        print(f"Error processing identifier {identifier}: {str(e)}")
def get_base_name(input_path):
    """
    Extracts a base name from the input path.
    For a local directory, it uses the folder name.
    For a GitHub URL, it uses 'gh-repo' where 'repo' is the repo name.
    For any other URL, it uses 'hostname-subpath'.
    """
    if "github.com" in input_path:
        # For GitHub repositories, extract the repo name
        repo_name = input_path.split("/")[-1]
        base_name = f"gh-{repo_name}"
    elif urlparse(input_path).scheme in ["http", "https"]:
        # For URLs, use hostname and subpath
        url_parts = urlparse(input_path)
        subpath = url_parts.path.replace('/', '-').strip("-")
        domain = url_parts.netloc
        site = ((url_parts.hostname).split(".")[0])
        base_name = f"{site}-{subpath}"
    else:
        # For local directories, use the folder name
        base_name = os.path.basename(os.path.normpath(input_path))
    
    # Ensure base_name does not contain illegal characters for filenames
    base_name = re.sub(r'[^a-zA-Z0-9\-_]', '_', base_name)
    return base_name

def main():
    input_path = input("Enter the path, URL, DOI, or PMID for ingestion: ")
    base_name = get_base_name(input_path)
    subdirectory = f"./output/{base_name}"
    os.makedirs(subdirectory, exist_ok=True)
    output_file = os.path.join(subdirectory, f"{base_name}_full_output.txt")
    urls_list_file = os.path.join(subdirectory, f"{base_name}_processed_urls.txt")
    processed_file = os.path.join(subdirectory, f"{base_name}_min_output.txt")

    max_depth = 2
    include_pdfs = True
    ignore_epubs = True

    if "github.com" in input_path:
        process_github_repo(input_path, output_file)
    elif "arxiv.org" in input_path:
        process_arxiv_pdf(input_path, output_file)
    elif urlparse(input_path).scheme in ["http", "https"]:
        if "youtube.com" in input_path or "youtu.be" in input_path:
            transcript = fetch_youtube_transcript(input_path)
            with open(output_file, "w", encoding='utf-8') as output:
                output.write(f"# YouTube Video Transcript\n")
                output.write(f"# URL: {input_path}\n\n")
                output.write(transcript)
            print("YouTube video transcript processed.")
        else:
            crawl_and_extract_text(input_path, output_file, urls_list_file, max_depth, include_pdfs, ignore_epubs)
    elif input_path.startswith("10.") and "/" in input_path or input_path.isdigit():
        process_doi_or_pmid(input_path, output_file)
    else:
        process_local_folder(input_path, output_file)

    preprocess_text(output_file, processed_file)

    min_text = safe_file_read(processed_file)
    min_token_count = get_token_count(min_text)
    print("min Token Count:", min_token_count)

    full_text = safe_file_read(output_file)
    full_token_count = get_token_count(full_text)
    print("full Token Count:", full_token_count)
    # rename output to tokenCount_output
    os.rename(output_file, f"{subdirectory}/{base_name}_{full_token_count}_full.txt")
    os.rename(processed_file, f"{subdirectory}/{base_name}_{min_token_count}_min.txt")
    # pyperclip.copy(full_text)
    print(f"Minified and full text saved to ./output/. Contents of {output_file} have been copied to the clipboard.")

if __name__ == "__main__":
    main()
