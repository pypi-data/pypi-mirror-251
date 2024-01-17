import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def read_default_prompt(prompt_file_name: str) -> str:
    with open(BASE_DIR / prompt_file_name) as fp:
        return fp.read()


def read_prompt(prompt_file_name: str) -> str:
    with open(prompt_file_name) as fp:
        return fp.read()


PROMPTS_DIR = ".codecraft/prompts"

SYSTEM_PROMPT_FILENAME = f"{PROMPTS_DIR}/SYSTEM_PROMPT.txt"
COVERAGE_INSTRUCTION_FILENAME = f"{PROMPTS_DIR}/COVERAGE_INSTRUCTION.txt"


def create_nested_folders_if_not_exist(path):
    """
    Creates nested folders as specified in the path if they do not already exist.

    :param path: A string representing the path where the folders should be created.
    """
    # Using os.makedirs with the 'exist_ok' flag to handle existing directories
    os.makedirs(path, exist_ok=True)


def add_line_to_gitignore(file_path, line_to_add):  # pragma: no cover
    """
    Checks if a specific line is present in the .gitignore file.
    If not, it adds the line to the file.

    :param file_path: Path to the .gitignore file.
    :param line_to_add: Line to check and potentially add to the file.
    :return: Message indicating whether the line was added or already existed.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        line_exists = line_to_add in (line.strip() for line in lines)
    except FileNotFoundError:
        # If the file doesn't exist, create it and add the line
        with open(file_path, "w") as file:
            file.write(line_to_add + "\n")
        return "File not found. Created .gitignore and added the line."

    if not line_exists:
        with open(file_path, "a") as file:
            # Ensure there's a newline before adding
            if lines and not lines[-1].endswith("\n"):
                file.write("\n")
            file.write(line_to_add + "\n")
        return "Line added to .gitignore."
    else:
        return "Line already exists in .gitignore."


def check_if_prompts_are_exists():
    create_nested_folders_if_not_exist(PROMPTS_DIR)
    if not os.path.exists(SYSTEM_PROMPT_FILENAME):
        with open(SYSTEM_PROMPT_FILENAME, "w") as f:
            f.write(read_default_prompt("SYSTEM_PROMPT.txt"))

    if not os.path.exists(COVERAGE_INSTRUCTION_FILENAME):
        with open(COVERAGE_INSTRUCTION_FILENAME, "w") as f:
            f.write(read_default_prompt("COVERAGE_INSTRUCTION.txt"))

    add_line_to_gitignore(".gitignore", ".codecraft")


check_if_prompts_are_exists()

SYSTEM_PROMPT = read_prompt(SYSTEM_PROMPT_FILENAME)
COVERAGE_INSTRUCTION = read_prompt(COVERAGE_INSTRUCTION_FILENAME)

DEV_INSTRUCTIONS = read_default_prompt("DEV_INSTRUCTIONS.txt")

OUTPUT_INSTRUCTIONS = read_default_prompt("OUTPUT_INSTRUCTIONS.txt")
