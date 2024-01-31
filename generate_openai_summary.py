from openai import OpenAI
import csv
import os
import environ

env = environ.Env()
env.read_env(".env")
OPENAI_API_KEY = env("OPENAI_API_KEY")

file_write_mode = 0o755

# Change the current working directory to root of your project
os.chdir("../")

root_directory = os.getcwd()
# print("root_directory:", root_directory)

os.chdir("./openai_doc_project")

openai_directory = os.getcwd()
# print("openai_directory:", openai_directory)

project_file_lists  = openai_directory + '/project_file_lists/'
summary_output_path = openai_directory + '/summary_outputs'
# print("project_file_lists:", project_file_lists)
# print("summary_output_path:", summary_output_path)

# Add any other prefix name to process the project file lists
prefix_name = "root"
# prefix_name = "my_test_project"

# Define the path for the single output file
all_summaries_file_path = os.path.join(openai_directory, prefix_name+'_all_summaries.md')
# print("All summaries will be stored in:", all_summaries_file_path)

# Path to your CSV file
csv_file_path = project_file_lists + prefix_name+'_directory_files.csv'
# print("csv_file_path:", csv_file_path)


def read_csv(file_path):
    """ Read file paths and word counts from a CSV file. """
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [(row[0], int(row[1])) for row in reader]


def read_file_content(file_path):
    """ Read the content of a file. """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def chunk_text(text, chunk_size):
    """Yield successive chunk_size chunks from text."""
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]


# Get a high-level summary of the text using OpenAI.
def get_summary_from_openai(text, p_file_path, model="gpt-3.5-turbo", max_token_size=4096):
    print(":get_summary_from_openai:")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Estimate whether chunking is needed based on word count
    estimated_tokens = len(text) / 4  # Rough estimation of tokens
    print(" estimated_tokens:", estimated_tokens)

    if estimated_tokens <= max_token_size:
        chunks = [text]
    else:
        # If chunking needed, divide text into chunks
        chunk_size = max_token_size * 4  # Estimate characters per chunk
        chunks = list(chunk_text(text, chunk_size))

    summaries = []
    for chunk in chunks:
        prompt = (
            "I am the lead software developer on my project. I need to write technical documentation for my team. "
            "Here is some code or configuration file:\n\n"
            "---\n"  # Separator for clarity
            f"{chunk}\n"
            "---\n"  # Separator for clarity
            "Provide a detailed summary of this code, explaining its functionality and purpose. "
            "The response should be concise written in markdown format with a title, "
            "summary and breakdown of the code or configuration."
        )

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
            # Optionally, handle specific API error related to token limit here
            print(f"    file_path: {p_file_path}")
            continue

    # Combine summaries for all chunks
    combined_summary = '\n\n'.join(summaries)
    return combined_summary


# Read the file paths and word counts
file_data = read_csv(csv_file_path)
# print("file_data:", file_data)

# Iterate through the file data and process each file
with open(all_summaries_file_path, 'w', encoding='utf-8') as all_summaries_file:
    for file_path, word_count in file_data:
        print("\n >>> Processing file: ", file_path, "word_count:", word_count)

        content = read_file_content(file_path)
        if content:
            original_file_name = file_path.split('/')[-1]
            file_name = original_file_name.split(".")[0]
            prefix_path = file_path.split(root_directory)[1].replace(original_file_name, "")
            new_summary_dir = summary_output_path + prefix_path

            # Create the directory if it does not exist
            if not os.path.exists(new_summary_dir):
                os.makedirs(new_summary_dir, file_write_mode)
                print(f"    Directory created: {new_summary_dir}")

            summary = get_summary_from_openai(content, file_path)
            summary_file_path = os.path.join(new_summary_dir, file_name + ".md")

            # Write the summary to its individual file
            if summary:
                with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                    summary_file.write(summary)
                print(f"    Summary written for {summary_file_path}")

                # Also write the summary to the single output file
                all_summaries_file.write(f"Summary for {file_path}:\n{summary}\n\n")
                print(f"    Summary added to {all_summaries_file_path}")
