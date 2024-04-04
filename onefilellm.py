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

def safe_file_read(filepath, fallback_encoding='latin1'):
    try:
        with open(filepath, "r", encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filepath, "r", encoding=fallback_encoding) as file:
            return file.read()

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

TOKEN = os.getenv('GITHUB_TOKEN', 'default_token_here')
if TOKEN == 'default_token_here':
    raise EnvironmentError("GITHUB_TOKEN environment variable not set.")

headers = {"Authorization": f"token {TOKEN}"}

def download_file(url, target_path):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(response.content)

def is_allowed_filetype(filename):
    allowed_extensions = ['.py', '.txt', '.js', '.rst', '.sh', '.md', '.pyx', '.html', '.yaml', '.json', '.jsonl', '.ipynb', '.h', '.c', '.sql', '.csv']
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

def process_github_repo(repo_url):
    api_base_url = "https://api.github.com/repos/"
    repo_url_parts = repo_url.split("https://github.com/")[-1].split("/")
    repo_name = "/".join(repo_url_parts[:2])

    subdirectory = ""
    if len(repo_url_parts) > 4 and repo_url_parts[2] == "tree":
        subdirectory = "/".join(repo_url_parts[4:])

    contents_url = f"{api_base_url}{repo_name}/contents"
    if subdirectory:
        contents_url = f"{contents_url}/{subdirectory}"

    repo_content = []

    def process_directory(url, repo_content):
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        files = response.json()

        for file in files:
            if file["type"] == "file" and is_allowed_filetype(file["name"]):
                print(f"Processing {file['path']}...")

                temp_file = f"temp_{file['name']}"
                download_file(file["download_url"], temp_file)

                repo_content.append(f"# {'-' * 3}\n")
                repo_content.append(f"# Filename: {file['path']}\n")
                repo_content.append(f"# {'-' * 3}\n\n")

                if file["name"].endswith(".ipynb"):
                    repo_content.append(process_ipynb_file(temp_file))
                else:
                    with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
                        repo_content.append(f.read())

                repo_content.append("\n\n")
                os.remove(temp_file)
            elif file["type"] == "dir":
                process_directory(file["url"], repo_content)

    process_directory(contents_url, repo_content)
    print("All files processed.")

    return "\n".join(repo_content)

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
        pdf_element = soup.find(id='pdf')

        if pdf_element is None:
            raise ValueError(f"No PDF found for identifier {identifier}. Sci-hub might be inaccessible or the document is not available.")

        content = pdf_element.get('src').replace('#navpanes=0&view=FitH', '').replace('//', '/')

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
    except (requests.RequestException, ValueError) as e:
        print(f"Error processing identifier {identifier}: {str(e)}")
        print("Sci-hub appears to be inaccessible or the document was not found. Please try again later.")

def process_github_pull_request(pull_request_url, output_file):
    # Extract repository owner, repository name, and pull request number from the URL
    url_parts = pull_request_url.split("/")
    repo_owner = url_parts[3]
    repo_name = url_parts[4]
    pull_request_number = url_parts[-1]

    # Make API requests to retrieve pull request information
    api_base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_request_number}"
    headers = {"Authorization": f"token {TOKEN}"}

    # Retrieve pull request details
    response = requests.get(api_base_url, headers=headers)
    pull_request_data = response.json()

    # Retrieve pull request diff
    diff_url = pull_request_data["diff_url"]
    diff_response = requests.get(diff_url, headers=headers)
    pull_request_diff = diff_response.text

    # Retrieve pull request comments and review comments
    comments_url = pull_request_data["comments_url"]
    review_comments_url = pull_request_data["review_comments_url"]
    comments_response = requests.get(comments_url, headers=headers)
    review_comments_response = requests.get(review_comments_url, headers=headers)
    comments_data = comments_response.json()
    review_comments_data = review_comments_response.json()

    # Combine comments and review comments into a single list
    all_comments = comments_data + review_comments_data

    # Sort comments based on their position in the diff
    all_comments.sort(key=lambda comment: comment.get("position") or float("inf"))

    # Format the retrieved pull request information
    formatted_text = f"# Pull Request Information\n\n"
    formatted_text += f"## Title: {pull_request_data['title']}\n\n"
    formatted_text += f"## Description:\n{pull_request_data['body']}\n\n"
    formatted_text += f"## Merge Details:\n"
    formatted_text += f"{pull_request_data['user']['login']} wants to merge {pull_request_data['commits']} commit into {repo_owner}:{pull_request_data['base']['ref']} from {pull_request_data['head']['label']}\n\n"
    formatted_text += f"## Diff and Comments:\n"

    # Iterate through the diff and interleave comments
    diff_lines = pull_request_diff.split("\n")
    comment_index = 0
    for line in diff_lines:
        formatted_text += f"{line}\n"
        while comment_index < len(all_comments) and all_comments[comment_index].get("position") == diff_lines.index(line):
            comment = all_comments[comment_index]
            formatted_text += f"\n### Review Comment by {comment['user']['login']}:\n"
            formatted_text += f"{comment['body']}\n\n"
            formatted_text += f"Path: {comment['path']}\n"
            formatted_text += f"Line: {comment['original_line']}\n\n"
            comment_index += 1

    # Process the entire repository
    repo_url = f"https://github.com/{repo_owner}/{repo_name}"
    repo_content = process_github_repo(repo_url)

    # Concatenate the pull request information and repository content
    final_output = f"{formatted_text}\n\n# Repository Content\n\n{repo_content}"

    # Write the final output to the file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(final_output)

    print(f"Pull request {pull_request_number} and repository content processed successfully.")

    return final_output

def process_github_issue(issue_url, output_file):
    # Extract repository owner, repository name, and issue number from the URL
    url_parts = issue_url.split("/")
    repo_owner = url_parts[3]
    repo_name = url_parts[4]
    issue_number = url_parts[-1]

    # Make API requests to retrieve issue information
    api_base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"
    headers = {"Authorization": f"token {TOKEN}"}

    # Retrieve issue details
    response = requests.get(api_base_url, headers=headers)
    issue_data = response.json()

    # Retrieve issue comments
    comments_url = issue_data["comments_url"]
    comments_response = requests.get(comments_url, headers=headers)
    comments_data = comments_response.json()

    # Format the retrieved issue information
    formatted_text = f"# Issue Information\n\n"
    formatted_text += f"## Title: {issue_data['title']}\n\n"
    formatted_text += f"## Description:\n{issue_data['body']}\n\n"
    formatted_text += f"## Comments:\n"

    for comment in comments_data:
        formatted_text += f"\n### Comment by {comment['user']['login']}:\n"
        formatted_text += f"{comment['body']}\n"

        # Extract code snippets from comment
        code_snippets = re.findall(r'https://github.com/.*#L\d+-L\d+', comment['body'])
        for snippet_url in code_snippets:
            # Extract file path, start line, and end line from the snippet URL
            url_parts = snippet_url.split("#")
            file_url = url_parts[0].replace("/blob/", "/raw/")
            line_range = url_parts[1]
            start_line, end_line = map(int, line_range.split("-")[0][1:]), map(int, line_range.split("-")[1][1:])

            # Make API request to retrieve the file content
            file_response = requests.get(file_url, headers=headers)
            file_content = file_response.text

            # Extract the code snippet based on the line range
            code_lines = file_content.split("\n")[start_line-1:end_line]
            code_snippet = "\n".join(code_lines)

            # Add the code snippet to the formatted text
            formatted_text += f"\n#### Code Snippet:\n```\n{code_snippet}\n```\n"

    # Process the entire repository
    repo_url = f"https://github.com/{repo_owner}/{repo_name}"
    repo_content = process_github_repo(repo_url)

    # Concatenate the issue information and repository content
    final_output = f"{formatted_text}\n\n# Repository Content\n\n{repo_content}"

    # Write the final output to the file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(final_output)

    print(f"Issue {issue_number} and repository content processed successfully.")

    return final_output

def main():
    input_path = input("Enter the local or Github repo path, GitHub pull request or Github issue URL, Documentation URL, DOI, or PMID for ingestion: ")
    output_file = "uncompressed_output.txt"
    urls_list_file = "processed_urls.txt"
    max_depth = 2
    include_pdfs = True
    ignore_epubs = True

    if "github.com" in input_path:
        if "/pull/" in input_path:
            final_output = process_github_pull_request(input_path, output_file)
        elif "/issues/" in input_path:
            final_output = process_github_issue(input_path, output_file)
        else:
            repo_content = process_github_repo(input_path)
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(repo_content)
            final_output = repo_content
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
            final_output = crawl_and_extract_text(input_path, output_file, urls_list_file, max_depth, include_pdfs, ignore_epubs)
    elif input_path.startswith("10.") and "/" in input_path or input_path.isdigit():
        process_doi_or_pmid(input_path, output_file)
    else:
        process_local_folder(input_path, output_file)

    processed_file = "compressed_output.txt"
    preprocess_text(output_file, processed_file)

    compressed_text = safe_file_read(processed_file)
    compressed_token_count = get_token_count(compressed_text)
    print("Compressed Token Count:", compressed_token_count)

    uncompressed_text = safe_file_read(output_file)
    uncompressed_token_count = get_token_count(uncompressed_text)
    print("Uncompressed Token Count:", uncompressed_token_count)

    pyperclip.copy(uncompressed_text)
    print(f"compressed_output.txt and uncompressed_output.txt have been created in the working directory. Contents of {output_file} have been copied to the clipboard.")

if __name__ == "__main__":
    main()
