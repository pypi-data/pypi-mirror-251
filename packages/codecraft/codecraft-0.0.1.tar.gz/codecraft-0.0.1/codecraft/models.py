import os
from typing import Any, Dict

import requests
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
from pydantic import Extra, root_validator
from termcolor.termcolor import cprint


class TogetherLLM(LLM):
    """Together large language models."""

    endpoint: str = "https://api.together.xyz/inference"

    model: str = "togethercomputer/llama-2-70b-chat"
    """model endpoint to use"""

    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    """Together API key"""

    temperature: float = 0.1
    """What sampling temperature to use."""

    max_tokens: int = 1024
    """The maximum number of tokens to generate in the completion."""

    prompt_format_string = """{prompt}"""

    type: str = "lang"

    class Config:
        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(values, "together_api_key", "TOGETHER_API_KEY")
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Call to Together endpoint."""

        res = requests.post(
            self.endpoint,
            json={
                "model": self.model,
                "max_tokens": self.max_tokens,
                "prompt": prompt,
                "request_type": "language-model-inference",
                "temperature": self.temperature,
                # "top_p": 0.7,
                # "top_k": 50,
                # "repetition_penalty": 1,
                "stop": ["</s>", "###"],
                "type": self.type,
                "prompt_format_string": self.prompt_format_string,
            },
            headers={
                "Authorization": f"Bearer {self.together_api_key}",
            },
        )
        cprint(res.text, "yellow")
        text = res.json()["output"]["choices"][0]["text"]
        return text


class WizardCoderLLM(TogetherLLM):
    model = "WizardLM/WizardCoder-Python-34B-V1.0"
    type = "code"
    prompt_format_string = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{prompt}

### Response:"""


class Llama2ChatLLM(TogetherLLM):
    model = "togethercomputer/llama-2-70b-chat"
    type = "chat"
    prompt_format_string = """[INST]  {prompt}\n [/INST]"""
    stop = ["</s>", "[INST]"]


class CodeLlamaInstruct(TogetherLLM):
    model = "togethercomputer/CodeLlama-34b-Instruct"
    type = "chat"
    stop = ["</s>", "[INST]"]
