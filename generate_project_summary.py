import os
from openai import OpenAI
import environ

# Initialize environment and OpenAI client
env = environ.Env()
env.read_env(".env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def list_markdown_files(directory):
    """List all markdown files in the directory."""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
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


def generate_summary_for_chunk(text, model="gpt-3.5-turbo", max_token_size=4096):
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


def create_project_summary(all_summary_files, p_openai_directory, p_summary_outputs_directory):
    """Create a project summary document."""
    print(":create_project_summary:")
    project_summary_content = "# Comprehensive Project Summary\n\n"

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
    markdown_files = sorted(list_markdown_files(full_summary_dir))
    # print("markdown_files:", markdown_files)

    # Organize files by directory structure
    organized_files = {}
    for file in markdown_files:
        directory = os.path.dirname(file)
        if directory not in organized_files:
            organized_files[directory] = []
        organized_files[directory].append(file)
    # print("organized_files:", organized_files)

    # Display files in hierarchical order
    for directory, files in organized_files.items():
        relative_dir = os.path.relpath(directory, p_summary_outputs_directory)
        project_summary_content += f"### {relative_dir}\n"
        for file in files:
            relative_path = os.path.relpath(file, p_summary_outputs_directory)
            file_name = os.path.basename(file)
            project_summary_content += f"- [{file_name}]({relative_path})\n"

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
create_project_summary(all_summary_file_list, openai_directory, summary_outputs_directory)
