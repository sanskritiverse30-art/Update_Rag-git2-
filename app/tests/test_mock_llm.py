from app.llm_service import MockLLMService


def test_mock_llm_returns_string():
    llm = MockLLMService()

    answer = llm.generate("What is AI?")

    assert isinstance(answer, str)
    assert answer == "Mock answer generated for testing."