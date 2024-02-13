
# LLM Content Collector: Command Line Data Aggregator for LLM Ingestion

**LLM Content Collector** is a tool designed to simplify the aggregation and preprocessing of various data sources for ingestion into large language models (LLMs). GitHub repositories, local directories, academic papers, and web pages are processed into text for LLMs through an efficient command-line interface.

## Key Features:

### Data Aggregation
- **Sources**: Extract text from **GitHub** repositories, **local repo** directories, **webpages**, **Youtube transcripts**, and **arXiv papers**.
- **Integration**: Supports Jupiter Notebook .ipynb and pdf formats.
- **Web Crawling**: Extract data from web sources by following links to a specified depth.

### Text Preprocessing
- **Cleaning and Preprocessing**: Outputs are generated in both compressed and uncompressed formats.  Compressed output removes stopwords and whitespace and converts to lowercase to minimize token usage.
- **Clipboard Integration**: Uncompressed text is automatically copied to the clipboard, ready for pasting into an LLM.
- **Token Count Metrics**: Token counts provided for compressed and uncompressed outputs.

## System Requirements and Installation

### Prerequisites
Before using the LLM Content Collector, ensure you have the following dependencies installed:
```bash
pip install requests nbformat nbconvert nltk PyPDF2 tiktoken pyperclip bs4 youtube_transcript_api 
```

### GitHub Personal Token
For accessing private repositories on GitHub, generate a GitHub personal token as outlined in the 'Obtaining a GitHub Personal Access Token' section.

### Installation
Clone the repository or download the source code. No additional installation is required.

## Usage Instructions

### Basic Command
```bash
python 1filellm.py
```
```
Enter the path or URL for ingestion:
```
  
### Input Options
The tool supports various input options, including:
- GitHub repository URL (e.g., `https://github.com/jimmc414/onefilellm`)
- arXiv abstract URL (e.g., `https://arxiv.org/abs/2401.14295`)
- Local folder path (e.g., `C:\python\PipMyRide`)
- Youtube video URL (e.g., `https://www.youtube.com/watch?v=KZ_NlnmPQYk`)
- Webpage URL (e.g., `https://llm.datasette.io/en/stable/`)

### Output
- `uncompressed_output.txt`: Full text output, automatically copied to the clipboard.
- `compressed_output.txt`: Cleaned and compressed text (e.g., all lowercase, whitespace and stop words removed).
- `processed_urls.txt`: List of all processed URLs for web crawling.
- To console: Token counts for both output files.

## Obtaining a GitHub Personal Access Token

A GitHub Personal Access Token (PAT) is required to authenticate with the GitHub API and access private repositories. Follow these steps to generate a token:

Log in to your GitHub account and navigate to the Settings page by clicking on your profile picture in the top-right corner and selecting Settings.

In the left sidebar, click on Developer settings.

Click on Personal access tokens in the left sidebar.

Click the Generate new token button.

Enter a name for the token in the Note field (e.g., "Repo-Prep").

Select the appropriate scopes for the token. For the 1filellm.py script, the minimum required scope is repo (which grants full control of private repositories). You may need to select additional scopes depending on your use case.

Click the Generate token button at the bottom of the page.

In the 1filellm.py script, replace the GITHUB_TOKEN placeholder with your actual token or add to the %GITHUB_TOKEN% env variable as detailed to automatically pull it from your environment.

  - Add Github Personal Access Token to environment variable GITHUB_TOKEN
    - Windows:
      ```
      setx GITHUB_TOKEN "YourGitHubToken"
      ```
    - Linux:
      ```
      echo 'export GITHUB_TOKEN="YourGitHubToken"' >> ~/.bashrc
      source ~/.bashrc
      ```

## Notes ##
- For Repos, Modify this line of code to add or remove filetypes processed: ``` allowed_extensions = ['.py', '.txt', '.js', '.rst', '.sh', '.md', '.pyx', '.html', '.yaml','.json', '.jsonl', '.ipynb', '.h', '.c', '.sql', '.csv'] ```
- For Web scraping, Modify this line of code to change how many links deep from the starting URL to include ``` max_depth = 2 ```

![image](https://github.com/jimmc414/1filellm/assets/6346529/5ef47d3f-e154-439e-a828-5b40a123a19c)
