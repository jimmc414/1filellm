
# Repo-Prep for LLM Ingestion (Updated with Web Crawling and Enhanced Processing)
(Arxiv papers and web crawling now included as input)

This enhanced version of the Repo-Prep scripts now includes additional functionalities to download, prepare, and preprocess content from GitHub repositories, local folders of code files, papers from arXiv.org, and web pages for ingestion by a language model. The tool now supports web crawling, processes Jupyter notebooks directly, extracts text from PDFs, and performs advanced text preprocessing. It concatenates code files into a single file, cleans to remove stopwords and extra whitespaces, and transforms to lowercase to minimize token usage. URLs from the text are extracted and saved separately. All scripts are integrated into `1filellm.py`.

## New Features

- **Web Crawling**: Ability to crawl web pages and extract text, following links to a specified depth.
- **Direct Jupyter Notebook Processing**: Support for processing Jupyter Notebook files directly without conversion.
- **Enhanced PDF Processing**: Improved handling of PDF files, including direct download from arXiv URLs.
- **Advanced Text Preprocessing**: More sophisticated text cleaning and preprocessing for efficiency.
- **Token Count Calculation**: Provides a token count for both compressed and uncompressed output text.
- **Automatic Clipboard Copying**: The uncompressed text is now automatically copied to the clipboard for easy use.

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

**Input**: GitHub repo URL, arXiv abstract URL, local folder path, or a specific webpage URL.  
**Output**: "uncompressed_output.txt" (full text output), "compressed_output.txt" (cleaned and compressed text), "processed_urls.txt" (list of all processed URLs for web crawling), and token counts for both output files.

### Additional Scripts

The functionalities of `clean.py` and `urlextractor.py` are now integrated into `1filellm.py`.

## Getting Started

Follow the existing setup instructions. Replace references to `onefilerepo.py` with `1filellm.py` and ensure all additional dependencies are installed.

## Obtaining a GitHub Personal Access Token

(No changes in this section.)
