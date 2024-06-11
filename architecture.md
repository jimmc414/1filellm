## Architecture Diagram


```plaintext
                                                   +---------------------------------+
                                                   |         External Services       |
                                                   |-------------------------------- |
                                                   | +-------------+  +------------+ |
                                                   | | GitHub API  |  | YouTube API| |
                                                   | +-------------+  +------------+ |
                                                   | | Sci-Hub     |  | ArXiv      | |
                                                   | +-------------+  +------------+ |
                                                   +---------------------------------+
                                                                ^
                                                                |
 +-------------------------------------------+                  |
 |                User                       |                  |
 |-------------------------------------------|                  |
 | - Provides input path or URL              |                  |
 | - Receives output and token count         |                  |
 +---------------------+---------------------+                  |
                       |                                        |
                       v                                        |
 +---------------------+---------------------+                  |
 |          Command Line Tool                |                  |
 |-------------------------------------------|                  |
 | - Handles user input                      |                  |
 | - Detects source type                     |                  |
 | - Calls appropriate processing modules    |                  |
 | - Preprocesses text                       |                  |
 | - Generates output files                  |                  |
 | - Copies text to clipboard                |                  |
 | - Reports token count                     |                  |
 +---------------------+---------------------+                  |
                       |                                        |
                       v                                        |
 +---------------------+---------------------+                  |
 |           Source Type Detection           |                  |
 |-------------------------------------------|                  |
 | - Determines type of source (GitHub, local|                  |
 |   YouTube, ArXiv, Sci-Hub, Webpage)       |                  |
 +---------------------+---------------------+                  |
                       |                                        |
                       v                                        |
 +-------------------------------------------+------------------+---------------------+
 |               Processing Modules          |                  |                     |
 |-------------------------------------------|                  |                     |
 | +-------------------+   +----------------+|                  |                     |
 | | GitHub Repo Proc  |   | Local Dir Proc ||                  |                     |
 | +-------------------+   +----------------+|                  |                     |
 | | - Requests.get()  |   | - Os.walk()    ||                  |                     |
 | | - Download_file() |   | - Safe_file_   ||                  |                     |
 | | - Process_ipynb() |   |   read()       ||                  |                     |
 | +-------------------+   +----------------+|                  |                     |
 |                                        ^                     |                     |
 | +-------------------+   +----------------+|                  |                     |
 | | YouTube Transcript |   | ArXiv PDF Proc||                  |                     |
 | +-------------------+   +----------------+|                  |                     |
 | | - YouTubeTranscript|   | - Requests.get||                  |                     |
 | |   Api.get()        |   | - PdfReader() ||                  |                     |
 | | - Formatter.format |   +----------------+|                 |                     |
 | +-------------------+                      |                 |                     |
 |                                        ^                     |                     |
 | +-------------------+   +----------------+|                  |                     |
 | | Sci-Hub Paper Proc |   | Webpage Crawling||                |                     |
 | +-------------------+   +----------------+|                  |                     |
 | | - Requests.post() |   | - Requests.get()||                 |                     |
 | | - BeautifulSoup() |   | - BeautifulSoup||                  |                     |
 | | - Wget.download() |   | - Urljoin()     ||                 |                     |
 | +-------------------+   +----------------+|                  |                     |
 +-------------------------------------------+                  |                     |
                       |                                        |                     |
                       v                                        |                     |
 +-------------------------------------------+                  |                     |
 |              Text Preprocessing           |                  |                     |
 |-------------------------------------------|                  |                     |
 | - Stopword removal                        |                  |                     |
 | - Lowercase conversion                    |                  |                     |
 | - Re.sub()                                |                  |                     |
 | - Nltk.stop_words                         |                  |                     |
 +-------------------------------------------+                  |                     |
                       |                                        |                     |
                       v                                        |                     |
 +-------------------------------------------+                  |                     |
 |              Output Generation            |                  |                     |
 |-------------------------------------------|                  |                     |
 | - Generates compressed text file          |                  |                     |
 | - Generates uncompressed text file        |                  |                     |
 +-------------------------------------------+                  |                     |
                       |                                        |                     |
                       v                                        |                     |
 +-------------------------------------------+                  |                     |
 |              Clipboard Interaction        |                  |                     |
 |-------------------------------------------|                  |                     |
 | - Copies uncompressed text to clipboard   |                  |                     |
 | - Pyperclip.copy()                        |                  |                     |
 +-------------------------------------------+                  |                     |
                       |                                        |                     |
                       v                                        |                     |
 +-------------------------------------------+                  |                     |
 |             Token Count Reporting         |                  |                     |
 |-------------------------------------------|                  |                     |
 | - Reports token count for both outputs    |                  |                     |
 | - Tiktoken.get_encoding()                 |                  |                     |
 | - Enc.encode()                            |                  |                     |
 +-------------------------------------------+                  |                     |
                                                                v
                                          +---------------------------------+
                                          |      External Libraries/Tools   |
                                          |---------------------------------|
                                          | - Requests                      |
                                          | - BeautifulSoup                 |
                                          | - PyPDF2                        |
                                          | - Tiktoken                      |
                                          | - Nltk                          |
                                          | - Nbformat                      |
                                          | - Nbconvert                     |
                                          | - YouTube Transcript API        |
                                          | - Pyperclip                     |
                                          | - Wget                          |
                                          | - Tqdm                          |
                                          | - Rich                          |
                                          +---------------------------------+
```

### External Libraries/Tools

The tool relies on several external libraries and tools to perform its functions efficiently. Here is a brief overview of each:

- **Requests**: Used for making HTTP requests to fetch data from web APIs and other online resources.
- **BeautifulSoup4**: A library for parsing HTML and XML documents. It is used for web scraping tasks.
- **PyPDF2**: A library for reading and manipulating PDF files.
- **Tiktoken**: Utilized for encoding text into tokens, essential for LLM input preparation.
- **NLTK**: The Natural Language Toolkit, used for various NLP tasks such as stopword removal.
- **Nbformat**: For reading and writing Jupyter Notebook files.
- **Nbconvert**: Converts Jupyter Notebooks to Python scripts and other formats.
- **YouTube Transcript API**: Fetches transcripts from YouTube videos.
- **Pyperclip**: A cross-platform clipboard module for Python.
- **Wget**: A utility for downloading files from the web.
- **Tqdm**: Provides progress bars for loops.
- **Rich**: Used for rich text and beautiful formatting in the terminal.

---


## Dependency Graph

```
graph LR
    subgraph onefilellm.py
        main[main()] --> process_github_repo
        main[main()] --> process_github_pull_request
        main[main()] --> process_github_issue
        main[main()] --> process_arxiv_pdf
        main[main()] --> process_local_folder
        main[main()] --> fetch_youtube_transcript
        main[main()] --> crawl_and_extract_text
        main[main()] --> process_doi_or_pmid
        main[main()] --> preprocess_text
        main[main()] --> get_token_count
        process_github_repo --> download_file
        process_github_pull_request --> download_file
        process_github_issue --> download_file
        process_arxiv_pdf --> PdfReader
        crawl_and_extract_text --> BeautifulSoup
        crawl_and_extract_text --> urlparse
        crawl_and_extract_text --> urljoin
        crawl_and_extract_text --> is_same_domain
        crawl_and_extract_text --> is_within_depth
        crawl_and_extract_text --> process_pdf
        process_doi_or_pmid --> wget
        process_doi_or_pmid --> PdfReader
        preprocess_text --> re
        preprocess_text --> stop_words
        get_token_count --> tiktoken
    end
    subgraph External Libraries
        requests[requests]
        BeautifulSoup[BeautifulSoup4]
        PyPDF2[PyPDF2]
        tiktoken[tiktoken]
        nltk[nltk]
        nbformat[nbformat]
        nbconvert[nbconvert]
        youtube_transcript_api[youtube-transcript-api]
        pyperclip[pyperclip]
        wget[wget]
        tqdm[tqdm]
        rich[rich]
    end
    subgraph External Resources
        GitHub_API[GitHub API]
        ArXiv[ArXiv]
        YouTube[YouTube]
        SciHub[Sci-Hub]
        Webpage[Webpage]
        Filesystem[Filesystem]
    end
    onefilellm.py --> requests
    onefilellm.py --> BeautifulSoup
    onefilellm.py --> PyPDF2
    onefilellm.py --> tiktoken
    onefilellm.py --> nltk
    onefilellm.py --> nbformat
    onefilellm.py --> nbconvert
    onefilellm.py --> youtube_transcript_api
    onefilellm.py --> pyperclip
    onefilellm.py --> wget
    onefilellm.py --> tqdm
    onefilellm.py --> rich
    onefilellm.py --> GitHub_API
    onefilellm.py --> ArXiv
    onefilellm.py --> YouTube
    onefilellm.py --> SciHub
    onefilellm.py --> Webpage
    onefilellm.py --> Filesystem
```


## Sequence Diagram

```
sequenceDiagram
    participant User
    participant onefilellm.py
    participant GitHub API
    participant ArXiv
    participant YouTube
    participant Sci-Hub
    participant Webpage
    participant Filesystem
    participant Clipboard

    User->>onefilellm.py: Start script (python onefilellm.py <input>)
    onefilellm.py->>User: Prompt for input if not provided (path/URL/DOI/PMID)
    User->>onefilellm.py: Provide input

    onefilellm.py->>onefilellm.py: Determine input type
    alt GitHub repository
        onefilellm.py->>GitHub API: Request repository content
        GitHub API->>onefilellm.py: Return file/directory list
        onefilellm.py->>GitHub API: Download files recursively
        onefilellm.py->>Filesystem: Save downloaded files
        onefilellm.py->>onefilellm.py: Process files (text extraction, preprocessing)
    else GitHub pull request
        onefilellm.py->>GitHub API: Request pull request data
        GitHub API->>onefilellm.py: Return PR details, diff, comments
        onefilellm.py->>onefilellm.py: Process and format PR data
        onefilellm.py->>GitHub API: Request repository content (for full repo)
        GitHub API->>onefilellm.py: Return file/directory list
        onefilellm.py->>GitHub API: Download files recursively
        onefilellm.py->>Filesystem: Save downloaded files
        onefilellm.py->>onefilellm.py: Process files (text extraction, preprocessing)
    else GitHub issue
        onefilellm.py->>GitHub API: Request issue data
        GitHub API->>onefilellm.py: Return issue details, comments
        onefilellm.py->>onefilellm.py: Process and format issue data
        onefilellm.py->>GitHub API: Request repository content (for full repo)
        GitHub API->>onefilellm.py: Return file/directory list
        onefilellm.py->>GitHub API: Download files recursively
        onefilellm.py->>Filesystem: Save downloaded files
        onefilellm.py->>onefilellm.py: Process files (text extraction, preprocessing)
    else ArXiv Paper
        onefilellm.py->>ArXiv: Download PDF
        ArXiv->>onefilellm.py: Return PDF content
        onefilellm.py->>onefilellm.py: Extract text from PDF
    else Local Folder
        onefilellm.py->>Filesystem: Read files recursively
        onefilellm.py->>onefilellm.py: Process files (text extraction, preprocessing)
    else YouTube Transcript
        onefilellm.py->>YouTube: Request transcript
        YouTube->>onefilellm.py: Return transcript
    else Web Page
        onefilellm.py->>Webpage: Crawl pages (recursive)
        Webpage->>onefilellm.py: Return HTML content
        onefilellm.py->>onefilellm.py: Extract text from HTML
    else Sci-Hub Paper (DOI/PMID)
        onefilellm.py->>Sci-Hub: Request paper
        Sci-Hub->>onefilellm.py: Return PDF content
        onefilellm.py->>onefilellm.py: Extract text from PDF
    end

    onefilellm.py->>onefilellm.py: Preprocess text (cleaning, compression)
    onefilellm.py->>Filesystem: Write outputs (uncompressed, compressed, URLs)
    onefilellm.py->>Clipboard: Copy uncompressed text to clipboard
    onefilellm.py->>User: Display token counts and file information
```

## Data Flow Diagram

```
graph LR

subgraph External Entities
    UserInput[User Input]
    GitHubAPI[GitHub API]
    Arxiv[ArXiv]
    YouTubeAPI[YouTube API]
    SciHub[Sci-Hub]
    WebPage[Web Pages]
    LocalFiles[Local Files]
    Clipboard[Clipboard]
end

subgraph Processes
    InputProcessing[Input Processing]
    GithubProcessing[GitHub Processing]
    ArxivProcessing[ArXiv Processing]
    YouTubeProcessing[YouTube Processing]
    WebCrawling[Web Crawling]
    SciHubProcessing[Sci-Hub Processing]
    LocalFileProcessing[Local File Processing]
    TextProcessing[Text Processing]
    OutputHandling[Output Handling]
end

subgraph Data Stores
    UncompressedOutput[uncompressed_output.txt]
    CompressedOutput[compressed_output.txt]
    ProcessedURLs[processed_urls.txt]
end

UserInput --> InputProcessing
InputProcessing --> |GitHub URL| GithubProcessing
InputProcessing --> |ArXiv URL| ArxivProcessing
InputProcessing --> |YouTube URL| YouTubeProcessing
InputProcessing --> |Web Page URL| WebCrawling
InputProcessing --> |DOI or PMID| SciHubProcessing
InputProcessing --> |Local File/Folder Path| LocalFileProcessing

GitHubAPI --> GithubProcessing: Repository/PR/Issue Data
Arxiv --> ArxivProcessing: PDF Content
YouTubeAPI --> YouTubeProcessing: Transcript
WebPage --> WebCrawling: HTML Content
SciHub --> SciHubProcessing: PDF Content
LocalFiles --> LocalFileProcessing: File Content

GithubProcessing --> |Extracted Text| TextProcessing
ArxivProcessing --> |Extracted Text| TextProcessing
YouTubeProcessing --> |Transcript| TextProcessing
WebCrawling --> |Extracted Text| TextProcessing
SciHubProcessing --> |Extracted Text| TextProcessing
LocalFileProcessing --> |Extracted Text| TextProcessing

TextProcessing --> |Processed Text| OutputHandling

OutputHandling --> |Uncompressed Text| UncompressedOutput
OutputHandling --> |Compressed Text| CompressedOutput
OutputHandling --> |Processed URLs| ProcessedURLs
OutputHandling --> |Uncompressed Text| Clipboard

subgraph Detailed Processes
    GithubProcessing --> |Repo URL| process_directory[Process Directory]
    process_directory --> |Files| ExtractText[Extract Text]
    ExtractText --> TextProcessing
    ArxivProcessing --> |PDF| ExtractPDFText[Extract PDF Text]
    ExtractPDFText --> TextProcessing
    YouTubeProcessing --> |Video ID| FetchTranscript[Fetch Transcript]
    FetchTranscript --> TextProcessing
    WebCrawling --> |HTML| ExtractWebText[Extract Web Text]
    ExtractWebText --> TextProcessing
    SciHubProcessing --> |DOI/PMID| FetchSciHubPaper[Fetch Sci-Hub Paper]
    FetchSciHubPaper --> ExtractPDFText
    LocalFileProcessing --> |Local Path| process_local_directory[Process Local Directory]
    process_local_directory --> ExtractText
end

```



## Call Graph


```
main
|
+--- safe_file_read(filepath, fallback_encoding='latin1')
|
+--- process_local_folder(local_path, output_file)
|    |
|    +--- process_local_directory(local_path, output)
|         |
|         +--- os.walk(local_path)
|         +--- is_allowed_filetype(file)
|         +--- process_ipynb_file(temp_file)
|         |    |
|         |    +--- nbformat.reads(notebook_content, as_version=4)
|         |    +--- PythonExporter().from_notebook_node()
|         |
|         +--- safe_file_read(file_path)
|
+--- process_github_repo(repo_url)
|    |
|    +--- process_directory(url, repo_content)
|         |
|         +--- requests.get(url, headers=headers)
|         +--- is_allowed_filetype(file["name"])
|         +--- download_file(file["download_url"], temp_file)
|         |    |
|         |    +--- requests.get(url, headers=headers)
|         |
|         +--- process_ipynb_file(temp_file)
|         +--- os.remove(temp_file)
|
+--- process_github_pull_request(pull_request_url, output_file)
|    |
|    +--- requests.get(api_base_url, headers=headers)
|    +--- requests.get(diff_url, headers=headers)
|    +--- requests.get(comments_url, headers=headers)
|    +--- requests.get(review_comments_url, headers=headers)
|    +--- process_github_repo(repo_url)
|
+--- process_github_issue(issue_url, output_file)
|    |
|    +--- requests.get(api_base_url, headers=headers)
|    +--- requests.get(comments_url, headers=headers)
|    +--- process_github_repo(repo_url)
|
+--- process_arxiv_pdf(arxiv_abs_url, output_file)
|    |
|    +--- requests.get(pdf_url)
|    +--- PdfReader(pdf_file).pages
|
+--- fetch_youtube_transcript(url)
|    |
|    +--- YouTubeTranscriptApi.get_transcript(video_id)
|    +--- TextFormatter().format_transcript(transcript_list)
|
+--- crawl_and_extract_text(base_url, output_file, urls_list_file, max_depth, include_pdfs, ignore_epubs)
|    |
|    +--- requests.get(current_url)
|    +--- BeautifulSoup(response.content, 'html.parser')
|    +--- process_pdf(url)
|    |    |
|    |    +--- requests.get(url)
|    |    +--- PdfReader(pdf_file).pages
|    |
|    +--- is_same_domain(base_url, new_url)
|    +--- is_within_depth(base_url, current_url, max_depth)
|
+--- process_doi_or_pmid(identifier, output_file)
|    |
|    +--- requests.post(base_url, headers=headers, data=payload)
|    +--- BeautifulSoup(response.content, 'html.parser')
|    +--- wget.download(pdf_url, pdf_filename)
|    +--- PdfReader(pdf_file).pages
|
+--- preprocess_text(input_file, output_file)
|    |
|    +--- safe_file_read(input_file)
|    +--- re.sub(pattern, replacement, text)
|    +--- stop_words.words("english")
|    +--- open(output_file, "w", encoding="utf-8").write(text.strip())
|
+--- get_token_count(text, disallowed_special=[], chunk_size=1000)
|    |
|    +--- tiktoken.get_encoding("cl100k_base")
|    +--- enc.encode(chunk, disallowed_special=disallowed_special)
|
+--- pyperclip.copy(uncompressed_text)
```
