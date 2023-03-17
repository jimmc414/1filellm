
# Repo-Prep for LLM Ingestion

This is a collection of scripts used to download and prepare a GitHub repository or a local folder of code files for ingestion by a language model. The code files are concatenated into a single file, cleaned to remove stopwords and extra whitespaces, and transformed to lowercase to minimize token usage. Additionally, URLs from the text are extracted and saved separately.

## Features

- Supports downloading and processing of GitHub repositories or local folders
- Supports various file types, including Jupyter notebooks
- Cleans and preprocesses the text for better language model ingestion
- Extracts and saves all URLs from the text separately

## Scripts

### 1. onefilerepo.py

This script takes a GitHub repository URL or a local folder path as input and processes the files by concatenating them into a single output file. It supports various file types, including Jupyter notebooks.

Usage:
`python onefilerepo.py`

### 2. clean.py

This script takes an input file, preprocesses the text by removing stopwords, extra whitespaces, and carriage returns, and converts the text to lowercase to minimize token usage.

Usage:
`python clean.py`

### 3. urlextractor.py

This script takes an input file and extracts all URLs from the text, saving them into a separate output file.

Usage:
`python urlextractor.py`

## Getting Started

1. Clone or download the repository.
2. Install the required libraries:

You can install all required libraries in a single line using the following command:

`pip install requests nbformat nbconvert nltk`

Simply run this command in your terminal or command prompt to install the necessary libraries for the scripts.


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

In the onefilerepo.py script, replace the GITHUB_PERSONAL_TOKEN placeholder with your actual token:

TOKEN = "GITHUB_PERSONAL_TOKEN"
