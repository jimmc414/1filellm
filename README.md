
# Repo-Prep for LLM Ingestion (Enhanced with Web Crawling)
(Arxiv papers and web crawling capabilities added)

## Overview
This utility, `Repo-Prep`, is specifically designed to streamline the process of preparing various types of content for ingestion into large language models (LLMs). It efficiently consolidates content from GitHub repositories, local code repositories, academic papers (specifically from arXiv.org), and web pages into a single text file. This process facilitates easy and efficient ingestion of diverse data sources into LLMs for training or analysis purposes.

## Key Functionalities
- **Content Aggregation**: Seamlessly combines content from multiple sources into a single, unified text file.
- **Web Crawling**: Adds the capability to crawl web pages and aggregate their content, enhancing the diversity of the input data.
- **Direct Jupyter Notebook Processing**: Processes Jupyter Notebook files (.ipynb) directly, extracting their code and markdown content.
- **PDF Text Extraction**: Efficiently extracts text from PDF documents, including direct downloads from arXiv.
- **Advanced Text Preprocessing**: Cleans the aggregated text by removing stopwords, extra whitespaces, and transforming text to lowercase to minimize token usage.
- **URL Extraction**: Extracts and separately saves URLs found in the text, allowing for additional context or reference material.

The integration of all these features into the `1filellm.py` script makes Repo-Prep a versatile and powerful tool for preparing data for LLM ingestion. Whether it's for training, fine-tuning, or any other application, Repo-Prep simplifies the data preparation step, allowing you to focus on the more critical aspects of working with LLMs.

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
