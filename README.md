
# LLM Content Harvester: Command Line Data Aggregator for LLM Ingestion

**LLM Content Harvester** is a powerful and versatile tool designed to simplify the aggregation and preprocessing of various data sources for ingestion into large language models (LLMs). Whether you're dealing with GitHub repositories, local directories, academic papers, or web pages, this utility streamlines the data preparation process for LLMs through an efficient command-line interface.

## Key Features:

### Comprehensive Data Aggregation
- **Sources**: Seamlessly gather content from GitHub repositories, local directories, web-based documentation, and arXiv papers.
- **Integration**: Supports a wide range of formats, including text from PDFs and arXiv papers, ensuring flexibility in data sourcing.

### Advanced Text Processing
- **Cleaning and Preprocessing**: Implements sophisticated techniques to optimize data for LLM processing. Outputs are available in both compressed and uncompressed formats.
- **Clipboard Integration**: For ease of use, uncompressed text is automatically copied to the clipboard, ready for pasting into an LLM.

### Enhanced User Experience
- **Token Count Metrics**: Get immediate feedback on the token counts for both compressed and uncompressed outputs, aiding in effective LLM training.
- **Deeper Web Crawling**: Extract more comprehensive data from web sources by following links to a specified depth.
- **Improved PDF and arXiv Handling**: Enjoy better accuracy and quality in text extraction from PDFs and arXiv documents.

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

[Instructions for obtaining a GitHub Personal Access Token]

## Advanced Features and Customization

### Customization Options
- [Details on how users can customize the tool, such as setting different levels for web crawling depth, choosing specific file types, etc.]

### Troubleshooting and FAQs
- [Common issues users might face and their solutions, along with frequently asked questions.]

## Contributing to LLM Content Harvester

We welcome contributions to improve and expand the capabilities of LLM Content Harvester. Please refer to our contribution guidelines for more details.

## License

[Details about the license under which the LLM Content Harvester is released, e.g., MIT, GPL, etc.]
