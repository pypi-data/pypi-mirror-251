import os
from unittest import mock


def test_together_llm():
    os.environ["TOGETHER_API_KEY"] = "4e4c665d0f329d0d2e567a9b184215a6b8b51f46cb774c46a8408d4faa32e674"
    from codecraft.models import TogetherLLM

    llm = TogetherLLM()
    assert llm.model == "togethercomputer/llama-2-70b-chat"
    assert llm.together_api_key == "4e4c665d0f329d0d2e567a9b184215a6b8b51f46cb774c46a8408d4faa32e674"
    assert llm.temperature == 0.1
    assert llm.max_tokens == 1024
    assert llm.prompt_format_string == "{prompt}"
    assert llm.type == "lang"
    assert llm._llm_type == "together"
    assert llm.validate_environment(
        {"together_api_key": "4e4c665d0f329d0d2e567a9b184215a6b8b51f46cb774c46a8408d4faa32e674"}
    ) == {"together_api_key": "4e4c665d0f329d0d2e567a9b184215a6b8b51f46cb774c46a8408d4faa32e674"}


def test_wizard_coder_llm():
    os.environ["TOGETHER_API_KEY"] = "test"
    from codecraft.models import WizardCoderLLM

    llm = WizardCoderLLM()
    assert llm.model == "WizardLM/WizardCoder-Python-34B-V1.0"
    assert llm.type == "code"
    assert (
        llm.prompt_format_string
        == "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{prompt}\n\n### Response:"
    )


def test_together_llm_call():
    """Test the _call method of the TogetherLLM class."""
    with mock.patch("requests.post") as mock_post:
        # Setup the mock to return a successful response with expected data
        mock_response = mock.Mock()
        mock_response.json.return_value = {"output": {"choices": [{"text": "test response"}]}}
        mock_post.return_value = mock_response

        # Instantiate the TogetherLLM with a mock API key
        os.environ["TOGETHER_API_KEY"] = "test_api_key"
        from codecraft.models import TogetherLLM

        llm = TogetherLLM()

        # Call the _call method
        response = llm._call(prompt="test prompt")

        # Assertions to check if the response is as expected
        mock_post.assert_called_once_with(
            llm.endpoint,
            json={
                "model": llm.model,
                "max_tokens": llm.max_tokens,
                "prompt": "test prompt",
                "request_type": "language-model-inference",
                "temperature": llm.temperature,
                "stop": ["</s>", "###"],
                "type": llm.type,
                "prompt_format_string": llm.prompt_format_string,
            },
            headers={"Authorization": f"Bearer {llm.together_api_key}"},
        )
        assert response == "test response"


def test_llama2_chat_llm():
    os.environ["TOGETHER_API_KEY"] = "test"
    from codecraft.models import Llama2ChatLLM

    llm = Llama2ChatLLM()
    assert llm.model == "togethercomputer/llama-2-70b-chat"
    assert llm.type == "chat"
    assert llm.prompt_format_string == "[INST]  {prompt}\n [/INST]"
