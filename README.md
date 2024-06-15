# Command Line Data Aggregation Tool for LLM Ingestion

This is a command-line tool that aggregates and preprocesses data from various sources into a single text file and copies it to the clipboard. 

This enables the quick creation of information-dense prompts for large language models (LLMs) by combining content from repositories, research papers, websites, and other sources. 

For more detailed program documentation see [architecture.md](https://github.com/jimmc414/1filellm/blob/main/architecture.md)

## Features

- Automatic source type detection based on provided path, URL, or identifier
- Support for local files and/or directories, GitHub repositories, GitHub pull requests, GitHub issues, academic papers from ArXiv, YouTube transcripts, web page documentation, Sci-Hub hosted papers via DOI or PMID
- Handling of multiple file formats, including Jupyter Notebooks (.ipynb), and PDFs
- Web crawling functionality to extract content from linked pages up to a specified depth
- Integration with Sci-Hub for automatic downloading of research papers using DOIs or PMIDs
- Text preprocessing, including compressed and uncompressed outputs, stopword removal, and lowercase conversion
- Automatic copying of uncompressed text to the clipboard for easy pasting into LLMs
- Token count reporting for both compressed and uncompressed outputs

## Data Flow Diagram

```
                                 +--------------------------------+
                                 |      External Services         |
                                 |--------------------------------|
                                 |  GitHub API  | YouTube API     |
                                 |  Sci-Hub     | ArXiv           |
                                 +--------------------------------+
                                           |
                                           |
                                           v
 +----------------------+          +---------------------+         +----------------------+
 |                      |          |                     |         |                      |
 |        User          |          |  Command Line Tool  |         |  External Libraries  |
 |----------------------|          |---------------------|         |----------------------|
 | - Provides input URL |--------->| - Handles user input|         | - Requests           |
 |                      |          | - Detects source    |<--------| - BeautifulSoup      |
 | - Receives text      |          |   type              |         | - PyPDF2             |
 |   in clipboard       |<---------| - Calls appropriate |         | - Tiktoken           |
 |                      |          |   processing modules|         | - NLTK               |
 +----------------------+          | - Preprocesses text |         | - Nbformat           |
                                   | - Generates output  |         | - Nbconvert          |
                                   |   files             |         | - YouTube Transcript |
                                   | - Copies text to    |         |   API                |
                                   |   clipboard         |         | - Pyperclip          |
                                   | - Reports token     |         | - Wget               |
                                   |   count             |         | - Tqdm               |
                                   +---------------------+         | - Rich               |
                                           |                       +----------------------+
                                           |
                                           v
                                    +---------------------+
                                    | Source Type         |
                                    | Detection           |
                                    |---------------------|
                                    | - Determines type   |
                                    |   of source         |
                                    +---------------------+
                                           |
                                           v
                                    +---------------------+
                                    | Processing Modules  |
                                    |---------------------|
                                    | - GitHub Repo Proc  |
                                    | - Local Dir Proc    |
                                    | - YouTube Transcript|
                                    |   Proc              |
                                    | - ArXiv PDF Proc    |
                                    | - Sci-Hub Paper Proc|
                                    | - Webpage Crawling  |
                                    |   Proc              |
                                    +---------------------+
                                           |
                                           v
                                    +---------------------+
                                    | Text Preprocessing  |
                                    |---------------------|
                                    | - Stopword removal  |
                                    | - Lowercase         |
                                    |   conversion        |
                                    | - Text cleaning     |
                                    +---------------------+
                                           |
                                           v
                                    +---------------------+
                                    | Output Generation   |
                                    |---------------------|
                                    | - Compressed text   |
                                    |   file output       |
                                    | - Uncompressed text |
                                    |   file output       |
                                    +---------------------+
                                           |
                                           v
                                    +---------------------+
                                    | Token Count         |
                                    | Reporting           |
                                    |---------------------|
                                    | - Report token count|
                                    |                     |
                                    | - Copies text to    |
                                    |   clipboard         |
                                    +---------------------+
```

## Recent Changes

- **2024-05-17:** Added ability to pass path or URL as command line argument.
- **2024-05-16:** Updated text colors.
- **2024-05-11:** 
  - Updated requirements.txt.
  - Added Rich library to `onefilellm.py`.
- **2024-04-04:**
  - Added GitHub PR and issue tests.
  - Added GitHub PR and issues.
  - Added tests for GitHub PRs and issues.
  - Added ability to concatenate specific GitHub issue and repo when GitHub issue URL is passed.
  - Updated tests to include pull request changes.
  - Added ability to concatenate pull request and repo when GitHub pull request URL is passed.
- **2024-04-03:**
  - Included the ability to pull a complete GitHub pull request given the GitHub pull request URL.
  - Updated `onefilellm.py` to return an error when Sci-hub is inaccessible or no document is found.
- **2024-03-19:**
  - Updated for Sci-Hub integration.
  - Added Sci-Hub DOI and PMIDs to test battery.
  - Added tests for Sci-Hub downloads via DOI and PMID.
- **2024-03-18:**
  - Updated for Sci-Hub, medrxiv, biorxiv & xlsx integration.
  - Added libraries.
  - Added Sci-Hub integration via paper's DOI or PMID.
- **2024-03-06:**
  - Created automated testing README.
  - Added automated self-testing module.
  - Renamed `onefilellm.py` for automated testing (no number as module's first character).
- **2024-02-13:** Added ability to ingest YouTube transcripts from URL.

## Installation

### Prerequisites

Install the required dependencies:

```bash
pip install -U -r requirements.txt
```

Optionally, create a virtual environment for isolation:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
```

### GitHub Personal Access Token

To access private GitHub repositories, generate a personal access token as described in the 'Obtaining a GitHub Personal Access Token' section.

### Setup

Clone the repository or download the source code.

## Usage

Run the script using the following command:

```bash
python onefilellm.py
```

![image](https://github.com/jimmc414/1filellm/assets/6346529/b4e281eb-8a41-4612-9d73-b2c115691013)


Or pass the URL or path in at the command line for the same behavior with less human interaction:

```bash
python onefilellm.py https://github.com/jimmc414/1filellm
```

The tool supports the following input options:

- Local file path (e.g., C:\documents\report.pdf)
- Local directory path (e.g., C:\projects\research) -> (files of selected filetypes segmented into one flat text file)
- GitHub repository URL (e.g., https://github.com/jimmc414/onefilellm) -> (Repo files of selected filetypes segmented into one flat text file)
- GitHub pull request URL (e.g., https://github.com/dear-github/dear-github/pull/102) -> (Pull request diff detail and comments and entire repository content concatenated into one flat text file)
- GitHub issue URL (e.g., https://github.com/isaacs/github/issues/1191) -> (Issue details, comments, and entire repository content concatenated into one flat text file)
- ArXiv paper URL (e.g., https://arxiv.org/abs/2401.14295) -> (Full paper PDF to text file)
- YouTube video URL (e.g., https://www.youtube.com/watch?v=KZ_NlnmPQYk) -> (Video transcript to text file)
- Webpage URL (e.g., https://llm.datasette.io/en/stable/) -> (To scrape pages to x depth in segmented text file)
- Sci-Hub Paper DOI (Digital Object Identifier of Sci-Hub hosted paper) (e.g., 10.1053/j.ajkd.2017.08.002) -> (Full Sci-Hub paper PDF to text file)
- Sci-Hub Paper PMID (PubMed Identifier of Sci-Hub hosted paper) (e.g., 29203127) -> (Full Sci-Hub paper PDF to text file)

The script generates the following output files:

- `uncompressed_output.txt`: The full text output, automatically copied to the clipboard.
- `compressed_output.txt`: Cleaned and compressed text.
- `processed_urls.txt`: A list of all processed URLs during web crawling.

## Configuration

- To modify the allowed file types for repository processing, update the `allowed_extensions` list in the code.
- To change the depth of web crawling, adjust the `max_depth` variable in the code.

## Obtaining a GitHub Personal Access Token

To access private GitHub repositories, you need a personal access token. Follow these steps:

1. Log in to your GitHub account and go to Settings.
2. Navigate to Developer settings > Personal access tokens.
3. Click on "Generate new token" and provide a name.
4. Select the necessary scopes (at least `repo` for private repositories).
5. Click "Generate token" and copy the token value.

In the `onefilellm.py` script, replace `GITHUB_TOKEN` with your actual token or set it as an environment variable:

- For Windows:
  ```shell
  setx GITHUB_TOKEN "YourGitHubToken"
  ```

- For Linux:
  ```shell
  echo 'export GITHUB_TOKEN="YourGitHubToken"' >> ~/.bashrc
  source ~/.bashrc
  ```

## Notes
- For Repos, Modify this line of code to add or remove filetypes processed: ``` allowed_extensions = ['.py', '.txt', '.js', '.rst', '.sh', '.md', '.pyx', '.html', '.yaml','.json', '.jsonl', '.ipynb', '.h', '.c', '.sql', '.csv'] ```
- For Web scraping, Modify this line of code to change how many links deep from the starting URL to include ``` max_depth = 2 ```
- Token counts are displayed in the console for both output files.

![image](https://github.com/jimmc414/1filellm/assets/6346529/5ef47d3f-e154-439e-a828-5b40a123a19c)
