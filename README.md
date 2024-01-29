# LLM Content Harvester: Your Comprehensive Data Aggregator

**LLM Content Harvester** is a sophisticated tool designed for efficient aggregation and processing of diverse content sources, tailored for ingestion into large language models (LLMs). Whether it's GitHub repositories, local directories, academic papers, or web pages, this utility simplifies and streamlines data preparation for LLMs.

## Key Features:
- **Unified Data Aggregation**: Gathers and integrates content from various sources into a single text file.
- **Smart Web Crawling**: Enhances data diversity by crawling and extracting content from web pages.
- **Seamless Jupyter Notebook Integration**: Directly processes Jupyter Notebook files, extracting code and markdown.
- **Robust PDF and ArXiv Integration**: Facilitates extraction of text from PDFs and arXiv papers.
- **Sophisticated Text Cleaning**: Implements advanced preprocessing techniques for optimal LLM data processing.
- **Efficient URL Management**: Organizes URLs for additional context or reference.

## New and Enhanced Features:
- **Deeper Web Crawling**: Expands web content extraction by following links to a specified depth.
- **Improved PDF and arXiv Processing**: Better extraction accuracy for PDFs and arXiv documents.
- **Advanced Text Processing**: Refined cleaning and preprocessing for optimized LLM readiness.
- **Token Count Metrics**: Displays token counts for both compressed and uncompressed outputs.
- **Clipboard Convenience**: Uncompressed text is automatically copied to the clipboard.

  
**Input**: GitHub repo URL (eg https://github.com/jimmc414/onefilellm), arXiv abstract URL (eg https://arxiv.org/abs/2401.14295), local folder path (eg C:\python\PipMyRide), or a specific webpage URL (eg https://llm.datasette.io/en/stable/).  
**Output**: "uncompressed_output.txt" (full text output; automatically copied into the clipboard), "compressed_output.txt" (cleaned and compressed text), "processed_urls.txt" (list of all processed URLs for web crawling), and token counts for both output files.


## Prerequisites

In addition to previous requirements, ensure `PyPDF2`, `tiktoken`, and `pyperclip` are installed:

```bash
pip install requests nbformat nbconvert nltk PyPDF2 tiktoken pyperclip
```

To access private repositories on GitHub, generate a GitHub personal token as described in the existing README.

## Script Update: `1filellm.py`

Replaces `onefilerepo.py`, now handling web crawling, direct Jupyter Notebook processing, and improved PDF handling. Also includes a function for automatic clipboard copying.

Usage:
```bash
python 1filellm.py
```

![image](https://github.com/jimmc414/onefilellm/assets/6346529/aac59566-9b31-48b6-aa7b-5f6fd7427f2c)


## Getting Started

Follow the existing setup instructions. Replace references to `onefilerepo.py` with `1filellm.py` and ensure all additional dependencies are installed.

## Obtaining a GitHub Personal Access Token

Obtaining a GitHub Personal Access Token
A GitHub Personal Access Token (PAT) is required to authenticate with the GitHub API and access private repositories. Follow these steps to generate a token:

Log in to your GitHub account and navigate to the Settings page by clicking on your profile picture in the top-right corner and selecting Settings.

In the left sidebar, click on Developer settings.

Click on Personal access tokens in the left sidebar.

Click the Generate new token button.

Enter a descriptive name for the token in the Note field (e.g., "Repo-Prep").

Select the appropriate scopes for the token. For the onefilerepo.py script, the minimum required scope is repo (which grants full control of private repositories). You may need to select additional scopes depending on your use case.

Click the Generate token button at the bottom of the page.

Your new personal access token will be displayed. Copy the token and save it somewhere secure, as you won't be able to see it again. If you lose the token, you'll need to generate a new one.

In the onefilerepo.py script, replace the GITHUB_TOKEN placeholder with your actual token:

'''
TOKEN = "GITHUB_TOKEN"
'''
