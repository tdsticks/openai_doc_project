# Open AI Doc Project

## Overview

The Open AI Doc Project is a tool designed to automate the documentation of software projects. Utilizing the Open AI API, this project simplifies the process of creating comprehensive Markdown documents for your entire project, along with generating an overall final summary file of the entire director structure linking to each markdown file.

## Key Features

- **Automated Documentation:** Automatically generates Markdown documents for individual files and components within your project.
- **Project Summary:** Formulates a concise and comprehensive summary of the entire project, offering a high-level overview.
- **Cost-Efficient:** Designed to minimize API usage to keep costs low, while providing the option to adjust settings for more detailed documentation.

## Future Enhancements

- Consolidate code into one file (classes and methods)
- **Comprehensive Project Overview:** We plan to integrate a feature that compiles all individual summaries into a larger, overarching project summary. This will provide an even more detailed understanding of the project as a whole.
- **Platform Compatibility:** While currently optimized for MacOS, efforts are underway to ensure compatibility and efficiency across other operating systems like Windows and Linux.

## Disclaimer

- Please note that the Open AI Doc Project is provided "as is" without any warranties or guarantees. Users are responsible for their own actions and decisions while using this software. The creators and contributors of the Open AI Doc Project are not liable for any misuse, errors, or financial charges that may arise from the use of this project.

## Usage Instructions

- Setup a virtual environment (I prefer pyenv) using Python 3.10.0
- Place this project in your existing project directory to analyze root and other specified project folders.
- Install the `requirements.txt` file: `pip install -r requirements.txt`
- Copy the `.env.example` file to `.env` and add your Open AI API key.
- Run `generate_project_file_lists.py` from the `openai_doc_project` folder to create file paths and word counts for processing.
- Update the `generate_openai_summary.py` prefix variable with your project file set to process. 
    This script is designed to process one project file set at a time.
- Run `generate_project_summary.py` from the `openai_doc_project` folder to create a project summary from your project summaries.

By using this project, you acknowledge and agree to these terms.
