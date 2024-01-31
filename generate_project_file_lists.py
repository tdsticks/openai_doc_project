import os
import fnmatch
from pprint import pprint

file_write_mode = 0o755

openai_directory = os.getcwd()
print("openai_directory:", openai_directory)

# Change the current working directory to root
os.chdir("../")

root_directory = os.getcwd()
print("root_directory:", root_directory)

# Add you project folder
project_directory = root_directory + "my_test_project"
# print("project_directory:", project_directory)

project_file_lists = openai_directory + "/project_file_lists/"
# print("project_file_lists:", project_file_lists)

# Create the directory if it does not exist
if not os.path.exists(project_file_lists):
    os.makedirs(project_file_lists, file_write_mode)
    print(f"    Directory created: {project_file_lists}")

# Patterns to exclude (can be modified as needed)
exclude_patterns = [
    "LICENSE", "*.rst", "*.ipynb",
    "requirements.txt",
    "*.pyc", "__pycache__", ".DS_Store",
    "*.env", "*.sql", "env/", "venv/",
    "*.github*",
    ".git",  # Exclude everything inside .git directory
    "*.gitkeep", "*.gitattributes",
    "node_modules/", "*.sqlite3",
    ".pylintrc", ".pre-commit-config.yaml",
    ".editorconfig", "*locale*", "*.idea",
    "*test*", "*docs*", "*.workspace"
]

# Paths to exclude
root_exclude_paths = [
    # project_directory,
    openai_directory,
]


def is_excluded(path, exclude_patterns, exclude_paths=None):
    """ Check if the given path matches any of the exclusion patterns. """
    if exclude_paths is None:
        exclude_paths = []
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True

        # Check if any part of the path matches the pattern (useful for directories)
        if any(fnmatch.fnmatch(part, pattern) for part in path.split(os.sep)):
            return True

    if exclude_paths is not None:
        for exclude_path in exclude_paths:
            if path.startswith(exclude_path):
                return True

    return False


def count_words_in_file(file_path):
    """ Count the number of words in a file. """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            words = contents.split()
            return len(words)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0


def traverse_directory(directory, exclude_patterns, exclude_paths=None):
    # print("directory:", directory)
    # print("exclude_patterns:", exclude_patterns)
    # print("exclude_paths:", exclude_paths)

    dir_files = {}
    total_word_count = 0

    """ Traverse the directory, skipping excluded files and directories. """
    for root, dirs, files in os.walk(directory):
        # print("root:", root)

        # Skip excluded paths
        if is_excluded(root, exclude_patterns, exclude_paths):
            dirs[:] = []  # Skip subdirectories
            continue

        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclude_patterns)]

        for file in files:
            if not is_excluded(file, exclude_patterns, exclude_paths):
                file_path = os.path.join(root, file)
                word_count = count_words_in_file(file_path)
                total_word_count += word_count
                dir_files[file_path] = word_count

    return dir_files, total_word_count


def write_results_to_csv(file_data, output_file):
    # print("output_file:", output_file)
    # print("file_data:", file_data)

    """ Write the file data to a CSV file. """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("File Path, Word Count\n")  # CSV Header
        for file_path, word_count in file_data.items():
            if word_count > 0:
                f.write(f"{file_path},{word_count}\n")


# Get the Django files
get_root_files, total_root_word_count = traverse_directory(root_directory, exclude_patterns, root_exclude_paths)
# pprint(get_root_files)
print("len:", len(get_root_files), "word count:", total_root_word_count)

# Get the Django files
get_project_files, total_django_word_count = traverse_directory(project_directory, exclude_patterns)
# pprint(get_project_files)
print("len:", len(get_project_files), "word count:", total_django_word_count)

# Output to CSV
# root_output_file_name = project_file_lists + "root_directory_files.csv"
# write_results_to_csv(get_root_files, root_output_file_name)

# Output to CSV
# project_output_file_name = project_file_lists + "project_directory_files.csv"
# write_results_to_csv(get_project_files, project_output_file_name)
