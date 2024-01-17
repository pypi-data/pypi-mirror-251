import multiprocessing
import os.path
import subprocess

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


def run_test(path: str) -> str:
    command = [
        "pytest",
        f"-n {multiprocessing.cpu_count()}",
        "-W ignore",
        "--cov-config=.coveragerc",
        "--cov-report=xml",
        f"--cov={os.getenv('CODECRAFT_COV_FOLDER', '.')}",
        "--tb=short",
        "-x",
        path,
    ]
    output = ""
    if os.path.isfile(path):
        command = [
            "pytest",
            "-W ignore",
            "--tb=short",
            "-x",
            path,
        ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode == 0:
        output += result.stdout.strip()
        if not os.path.isfile(path):
            command = ["coverage", "report", "--sort=-cover"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output += "\n"
            output += result.stdout.strip()
    else:
        return f"{result.stdout}\n\n{result.stderr or ''}"
    return output


class RunTestInput(BaseModel):
    path: str = Field()


run_test_tool = StructuredTool.from_function(
    func=run_test,
    name="run_test",
    args_schema=RunTestInput,
    description="Tool is useful to run tests for the code.",
)
