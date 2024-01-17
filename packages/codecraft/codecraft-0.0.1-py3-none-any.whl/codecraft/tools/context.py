import os.path
import subprocess
from typing import Optional

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..context import context


def get_coverage_info(path: str):
    command = ["coverage", "annotate", path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode == 0:
        with open(f"{path},cover") as fp:
            legend = """\n> executed
! missing (not executed)
- excluded"""
            return legend + "\n\n" + fp.read()
    else:
        return result.stderr


def add_file_to_context(filename: str, with_coverage: bool = False):
    if not os.path.exists(filename):
        return f"Error: file {filename} does not exist"

    if with_coverage:
        return get_coverage_info(filename)
    else:
        context.added_files.append(filename)
        with open(filename) as fp:
            source_code = fp.read()
        return f"Added {filename} to the context.\nSource code of file {filename}:\n```{source_code}```"


class AddFileToContextInput(BaseModel):
    filename: str = Field(description="Name of the file to get content")
    with_coverage: Optional[bool] = Field(description="Show coverage information for the file", default=False)


add_file_to_context_tool = StructuredTool.from_function(
    func=add_file_to_context,
    name="add_file_to_context",
    args_schema=AddFileToContextInput,
    description="Tool is useful to add file to context to see its source code.",
)
