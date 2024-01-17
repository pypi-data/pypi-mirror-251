import fnmatch
import json
import os
import subprocess
from collections import defaultdict

import os

from tree_sitter_languages import get_language, get_parser

language = get_language('python')
parser = get_parser('python')

query_scm = """
(class_definition
  name: (identifier) @name.definition.class) @definition.class

(function_definition
  name: (identifier) @name.definition.function) @definition.function

(call
  function: [
      (identifier) @name.reference.call
      (attribute
        attribute: (identifier) @name.reference.call)
  ]) @reference.call
"""


def parse_code(code):
    elements = {
        'class': {},
        'function': []
    }

    if not code:
        return elements

    tree = parser.parse(bytes(code, "utf-8"))

    # Run the tags queries
    query = language.query(query_scm)
    captures = query.captures(tree.root_node)

    for node, tag in captures:
        if tag == 'name.definition.class':
            class_name = node.text.decode('utf8')
            elements['class'][class_name] = []
        elif tag == 'name.definition.function':

            function_name = node.text.decode('utf8')
            parameters = node.parent.child_by_field_name('parameters').text.decode('utf8').replace('\n', ' ')
            func_sig = f'{function_name}{parameters}'

            parent = node.parent
            while parent is not None:
                if parent.type == 'class_definition':
                    class_name = parent.child_by_field_name('name').text.decode('utf8')
                    elements['class'][class_name].append(func_sig)
                    break
                parent = parent.parent
            else:
                elements['function'].append(func_sig)

    return elements


def parse_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return parse_code(code)


def render_repo_map(repo_map, files_and_names=False):
    rendered_text = ""
    files = []
    names = []
    for file_path, elements in repo_map.items():
        rendered_text += file_path + ":\n"
        files.append(file_path)
        for class_name, methods in elements['class'].items():
            rendered_text += f"   class {class_name}\n"
            names.append(class_name)
            for method in methods:
                rendered_text += f"         def {method}\n"
                names.append(method)
        for function in elements['function']:
            rendered_text += f"   def {function}\n"
            names.append(function)
    if files_and_names:
        return files, names
    return rendered_text


def get_python_files_in_directory(
        directory=".",
        ignore_folders=["venv", ".venv", "build", "node_modules", "dev_gpt.egg-info", "migrations"],
):
    """
    Get list of python files in a directory and subdirectories

    :param directory:
    :param ignore_folders:
    :return:
    """
    python_files_content = []

    for _root, dirs, files in os.walk(directory):
        # Remove ignored folders from dirs in-place to prevent os.walk from traversing them
        dirs[:] = [d for d in dirs if d not in ignore_folders]

        for filename in fnmatch.filter(files, "*.py"):
            filepath = os.path.join(_root, filename)
            if filepath.startswith("./"):
                filepath = filepath[2:]
            python_files_content.append(filepath)

    return python_files_content


def create_repo_map():
    repo_map = {}
    for file_path in get_python_files_in_directory():
        repo_map[file_path] = parse_file(file_path)
    return repo_map


def get_repomap(files_and_names=False):
    return render_repo_map(create_repo_map(), files_and_names)


if __name__ == "__main__":  # pragma: no cover
    print(get_repomap())
