import re
import os

def read_txt_files(path):
    """
    Reads multiple text files from the specified path and joins their content into a single string.
    
    :param path: Directory path where the text files are located.
    :return: Joined content of the text files as a single string.
    """
    file_names = ['tale1.txt', 'folk_tale.txt', 'Brothers.txt', 'Aesop.txt']
    lines = []
    
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        try:
            # Handle different encodings
            encoding = 'utf-8' if file_name in ['tale1.txt', 'folk_tale.txt'] else 'cp949'
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                content = " ".join(content.split())  # Clean up extra spaces
                lines.append(content)
        except FileNotFoundError:
            print(f"File {file_name} not found in {path}. Skipping.")
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
    
    # Join all file contents with a space separator
    joined_lines = " ".join(lines)
    return joined_lines


def clean_text(lines):
    """
    Cleans the given text using regular expressions to remove unwanted characters, symbols, and patterns.
    
    :param lines: The input string to be cleaned.
    :return: Cleaned string.
    """
    lines = re.sub(r'\(계속\).*?[●○]', '', lines)   # Remove certain text patterns
    lines = re.sub(r'[●○]', '', lines)              # Remove unwanted characters
    lines = re.sub(r"\s+", " ", lines).strip()      # Replace multiple spaces with a single space
    lines = re.sub(r"[~♥]", "", lines)              # Remove specific characters like ~ and ♥
    lines = re.sub(r"[ㅋㅎㅠㅜ]", "", lines)         # Remove common Korean emoticon characters
    lines = re.sub(r'\n', '', lines).strip()        # Remove newlines
    lines = re.sub(r"\(.*\)|\s-\s.*", "", lines)    # Remove text in parentheses or in the form of " - text"
    lines = re.sub(r"(http|https)?:\/\/\S+\b|www\.(\w+\.)+\S*", "", lines).strip()  # Remove URLs

    return lines
