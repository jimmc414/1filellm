# onefilellm: Command Line Data Aggregation Tool for LLM Ingestion

onefilellm is a command-line tool that aggregates and preprocesses data from various sources for ingestion into large language models (LLMs).

## Features

- Automatic source type detection based on provided path, URL, or identifier
- Support for local files and/or directories, GitHub repositories, academic papers from ArXiv, BiorXiv, and MedXiv, YouTube transcripts, web page documentation, Sci-Hub hosted papers via DOI or PMID
- Handling of multiple file formats, including Jupyter Notebooks (.ipynb), PDFs, .Xlsx and Compiled HTML Help (.chm) files
- Web crawling functionality to extract content from linked pages up to a specified depth
- Integration with Sci-Hub for automatic downloading of research papers using DOIs and PMIDs
- Text preprocessing, including compressed and uncompressed outputs, stopword removal, and lowercase conversion
- Automatic copying of uncompressed text to the clipboard for easy pasting into LLMs
- Token count reporting for both compressed and uncompressed outputs

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

At the prompt, enter the file or folder path, Documenation, Paper or Repo URL, or for Sci-Hub papers, the DOI or PMID of the data source you want to process:

```plaintext
Enter the local or remote path, URL, DOI, or PMID for ingestion:
```

The tool supports the following input options:

- Local file path (e.g., `C:\documents\report.pdf`)
- Local directory path (e.g., `C:\projects\research`) -> (files of selected filetypes segmented into one flat text file) 
- GitHub repository URL  (e.g., `https://github.com/username/repo`) -> (Repo files of selected filetypes segmented into one flat text file)
- ArXiv/BiorXiv/MedXiv paper URL (e.g., `https://arxiv.org/abs/2401.14295`) -> (Full paper PDF to text file)
- YouTube video URL (e.g., `https://www.youtube.com/watch?v=video_id`) -> (Video transcript to text file)
- Webpage URL  (e.g., `https://example.com/page` | `https://example.com/page/page.pdf`) -> (To scrape pages to x depth or remote file in segmented text file)
- Sci-Hub Paper DOI (Digital Object Identifier of Sci-Hub hosted paper) (e.g., `10.1234/example.doi` | `10.1234/example.doi`) -> (Full paper PDF to text file)
- Sci-Hub Paper PMID (PubMed Identifier of Sci-Hub hosted paper) (e.g., `12345678`) -> (Full paper PDF to text file)

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

- Token counts are displayed in the console for both output files.

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.
