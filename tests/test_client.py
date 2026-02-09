import pytest
from src.client import ConcentrateClient, APIRequestError
from src.config import settings


def test_client_initialization():
    client = ConcentrateClient(api_key="test-key")
    assert client.api_key == "test-key"
    assert "Bearer test-key" in client.headers["Authorization"]


def test_client_missing_api_key():
    with pytest.raises(ValueError):
        ConcentrateClient(api_key="")


def test_prompt_library():
    from src.prompts import PromptLibrary

    simple_prompts = PromptLibrary.get_simple_qa_prompts()
    assert len(simple_prompts) > 0
    assert "content" in simple_prompts[0]
    assert "name" in simple_prompts[0]

    reasoning_prompts = PromptLibrary.get_reasoning_prompts()
    assert len(reasoning_prompts) > 0

    all_prompts = PromptLibrary.get_all_prompts()
    assert len(all_prompts) > len(simple_prompts)
