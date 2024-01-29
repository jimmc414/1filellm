
# LLM Content Harvester: Command Line Data Aggregator for LLM Ingestion

**LLM Content Harvester** is a tool designed to simplify the aggregation and preprocessing of various data sources for ingestion into large language models (LLMs). Whether you're dealing with GitHub repositories, local directories, academic papers, or web pages, this utility processes the data into text for LLMs through an efficient command-line interface.

## Key Features:

### Data Aggregation
- **Sources**: Gather content from **GitHub** repositories, **local repo** directories, **web**-based documentation, and **arXiv papers**.
- **Integration**: Supports a range of formats, including text from PDFs and arXiv papers.

### Text Preprocessing
- **Cleaning and Preprocessing**: Implements techniques to optimize data for LLM processing. Outputs are available in both compressed and uncompressed formats.
- **Clipboard Integration**: For ease, uncompressed text is automatically copied to the clipboard, ready for pasting into an LLM.

### Enhanced User Experience
- **Token Count Metrics**: Get the token counts for both compressed and uncompressed outputs, aiding in effective LLM training.
- **Web Crawling**: Extract data from web sources by following links to a specified depth.


## System Requirements and Installation

### Prerequisites
Before using the LLM Content Harvester, ensure you have the following dependencies installed:
```bash
pip install requests nbformat nbconvert nltk PyPDF2 tiktoken pyperclip
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
- Webpage URL (e.g., `https://llm.datasette.io/en/stable/`)

### Output
The tool generates several output files:
- `uncompressed_output.txt`: Full text output, automatically copied to the clipboard.
- `compressed_output.txt`: Cleaned and compressed text (e.g., all lowercase, whitespace and stop words removed).
- `processed_urls.txt`: List of all processed URLs for web crawling.
- Token counts for both output files.

## Obtaining a GitHub Personal Access Token

A GitHub Personal Access Token (PAT) is required to authenticate with the GitHub API and access private repositories. Follow these steps to generate a token:

Log in to your GitHub account and navigate to the Settings page by clicking on your profile picture in the top-right corner and selecting Settings.

In the left sidebar, click on Developer settings.

Click on Personal access tokens in the left sidebar.

Click the Generate new token button.

Enter a descriptive name for the token in the Note field (e.g., "Repo-Prep").

Select the appropriate scopes for the token. For the 1filellm.py script, the minimum required scope is repo (which grants full control of private repositories). You may need to select additional scopes depending on your use case.

Click the Generate token button at the bottom of the page.

Your new personal access token will be displayed. Copy the token and save it somewhere secure, as you won't be able to see it again. If you lose the token, you'll need to generate a new one.

In the 1filellm.py script, replace the GITHUB_TOKEN placeholder with your actual token:

'''
TOKEN = "GITHUB_TOKEN"
'''


