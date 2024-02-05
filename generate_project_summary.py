import os
from openai import OpenAI
import environ
import itertools
from pprint import pprint


# Initialize environment and OpenAI client
env = environ.Env()
env.read_env(".env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def list_markdown_files(directory):
    """List all markdown files in the directory."""
    # markdown_files = []
    markdown_files = {}
    for root, dirs, files in os.walk(directory):
        md_files = []
        for file in files:
            if file.endswith(".md"):
                # markdown_files.append(os.path.join(root, file))
                md_files.append(file)
        if len(md_files) > 0:
            rel_path = "/" + root.replace(directory, "")
            # print(rel_path, md_files)
            markdown_files[rel_path] = md_files
    return markdown_files
    
            
def read_file(file_path):
    """Read file content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content


def chunk_text(text, chunk_size):
    """
    Yield successive chunk_size chunks from text.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): Size of each chunk in characters.

    Yields:
        str: A chunk of the text.
    """
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


# def generate_summary_for_chunk(text, model="gpt-3.5-turbo", max_token_size=4096):
    """
    Get a high-level summary of the text using OpenAI.

    Args:
        text (str): The text to summarize.
        p_file_path (str): Path to the file being summarized.
        model (str): The OpenAI model to use.
        max_token_size (int): The maximum token size for the model.

    Returns:
        str: A summary of the text.
    """
    print(":generate_summary_for_chunk:")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Estimate whether chunking is needed based on word count
    estimated_tokens = len(text) / 4  # Rough estimation of tokens
    print("\nestimated_tokens:", estimated_tokens)

    if estimated_tokens <= max_token_size:
        chunks = [text]
    else:
        # If chunking needed, divide text into chunks
        chunk_size = max_token_size * 4  # Estimate characters per chunk
        print(" chunk_size:", chunk_size)
        
        chunks = list(chunk_text(text, chunk_size))
    # print(chunks)
    
    summaries = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            prompt = (
                "I am the lead software developer on my project. I need to write a technical summary documentation for my project. "
                "The files I'm providing are already in Markdown and summaries from entire folder structures with possibly many files from my project. "
                "The files themselves could be quite large so I'm chunking them up due to OpenAI's token limitations. "
                "Please remember the context of each chunked message to get the full story of the project. "
                f"I'm providing an enumeration from the for loop to help you know what chunk we're on using this value: {i} "
                "Here is the first chunk from all of the summary files put together.\n\n"
                "---\n"  # Separator for clarity
                f"{chunk}\n"
                "---\n"  # Separator for clarity
                "Please provide a summary if all of the Markdown documentation together in one Markdown document with a title "
                "and whatever context from the markdown documents."
            )
        else:
             prompt = (
                f"Next enumeration value: {i}\n"
                "Here is the continued context chunk:\n\n"
                "---\n"  # Separator for clarity
                f"{chunk}\n"
                "---\n"  # Separator for clarity
                "Please continue formulating the end result Markdown summary document."
            )
        # print("\n\n >>> Prompt:", prompt)

        print("\nSending API call to Open AI. estimated_tokens:", estimated_tokens)
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=model,
            )
            summaries.append(response.choices[0].message.content)
        except Exception as e:
            print(f"    An error occurred while processing chunk: {e}")
            continue
        
    print("End with processing API call to Open AI.")

    # Combine summaries for all chunks
    combined_summary = '\n\n'.join(summaries)
    return combined_summary


def generate_tree(directory, files_dict, prefix=''):
    print(":generate_tree:")
    
    tree_lines = []
    
    # Sort directories and files to ensure consistent order
    items = files_dict[directory].items()
    
    # Loop through all the files and paths
    for p, (path, files) in enumerate(items):
        print(p, path, files)
        
        indent = ''  # Indentation based on directory depth
        indent = path.count(os.sep) * '│   '  # Indentation based on directory depth
        
        # Special handling for root ('/') to avoid extra indentation
        if path != '/':
            tree_lines.append(f"{prefix}{indent}├── {os.path.basename(path)}/")
            if p >= len(items)-1:
                indent += '└    '
            else:
                indent += '│    '
        
        # Loop through all the files underneath the paths
        for f, file in enumerate(sorted(files)):
        # for f, file in enumerate(files):
            # print(file)
            # If its the last item, end the hierarchy
            if f >= len(files)-1:
                tree_lines.append(f"{prefix}{indent}└── {file}")
            # Otherwise, keep the hierarching going
            else:
                tree_lines.append(f"{prefix}{indent}├── {file}")
            
    # pprint(tree_lines)
    return tree_lines


def create_project_summary(p_openai_directory, p_summary_outputs_directory, all_summary_files=None):
    """Create a project summary document."""
    print(":create_project_summary:")
    project_summary_content = "# Project Summary\n\n"

    # Add a project summary if you wish
    # project_summary_content += "This prject is about..."

    # TODO: Pausing this feature for now. Need to rethink the approach into using Open AI for
    #  building a summary of the entire project from the summary files.

    # cumulation_file_content = ""
    #
    # # Process each summary file
    # for summary_file in all_summary_files:
    #     print("\nsummary_file:", summary_file)
    #     file_content = read_file(summary_file)
    #     # print("\n   >>> file_content:", file_content)
    #     if file_content:
    #         cumulation_file_content += file_content
        
    # Process the file content into chunks as we call to Open AI getting a response back
    # project_summary_content += generate_summary_for_chunk(cumulation_file_content) + "\n\n"

    # Append index of all markdown files
    project_summary_content += "## Index of Project Markdown Files\n\n"
    full_summary_dir = os.path.join(p_openai_directory, p_summary_outputs_directory)
    # print("full_summary_dir:", full_summary_dir)

    # Get list of markdown files and sort them
    # markdown_files = sorted(list_markdown_files(full_summary_dir))
    markdown_files = list_markdown_files(full_summary_dir)
    # pprint(markdown_files)
    
    # Organize files by directory structure
    organized_files = {}
    organized_files[full_summary_dir] = markdown_files
    # pprint(organized_files)
    
    # Generate directory tree for each top-level directory
    # for directory in sorted(organized_files.keys()):
    #     relative_dir = os.path.relpath(directory, p_summary_outputs_directory)
    #     project_summary_content += f"\n<pre>\n{relative_dir}\n"
    #     # TODO: This is where we loop through data and generate the Markdown data structure
    #     tree_lines = ""
    #     project_summary_content += "\n".join(tree_lines) + "\n</pre>\n"
    
     # Assuming organized_files is structured as shown in your data
    for directory, files in organized_files.items():
        relative_dir = os.path.relpath(directory, p_openai_directory)  # Adjust based on actual usage
        if relative_dir == '.':
            relative_dir = '/'  # Adjusting root representation
        
        project_summary_content += f"'''\n{directory}\n"
        
        # Initialize an empty dictionary to hold filtered paths and files
        filtered_files_dict = {}

        # Iterate over each item in the organized_files dictionary
        for sub_path, files in organized_files.items():
            # Check if the current sub_path starts with the directory we're generating the tree for
            if sub_path.startswith(directory):
                # If it does, add it to the filtered dictionary
                filtered_files_dict[sub_path] = files

        # Now, pass the filtered dictionary to the generate_tree function
        tree_lines = generate_tree(directory, filtered_files_dict, prefix='')
        project_summary_content += "\n".join(tree_lines) + "\n'''\n"

    # Write the final project summary to a file
    full_final_project_summary = os.path.join(full_summary_dir, "FINAL_PROJECT_SUMMARY.md")
    with open(full_final_project_summary, 'w', encoding='utf-8') as summary_file:
        summary_file.write(project_summary_content)
    print("All done, file written:", full_final_project_summary)


all_summary_file_list = [
    "root_all_summaries.md",
    # Add other summary files here
]

# Example usage
openai_directory = os.getcwd() + "/"
# print("openai_directory:", openai_directory)

summary_outputs_directory = "summary_outputs/"  # Set your project directory path
# create_project_summary(openai_directory, summary_outputs_directory, all_summary_file_list)
create_project_summary(openai_directory, summary_outputs_directory, None)
