from src.llm.filler import _clean_llm_output


class TestCleanLLMOutput:
    def test_removes_markdown_fences(self):
        original = '"""Docstring."""\n\n# LLM_FILL: test\n\ndef foo():\n    pass\n'
        output = '```python\n"""Docstring."""\n# Fixed\ndef foo():\n    return 1\n```'
        cleaned = _clean_llm_output(output, original)
        assert not cleaned.startswith("```")

    def test_preserves_python_content(self):
        original = '"""Docstring."""\ndef foo():\n    pass\n'
        output = '"""Docstring."""\ndef foo():\n    return 42\n'
        cleaned = _clean_llm_output(output, original)
        assert "return 42" in cleaned
        assert "```" not in cleaned

    def test_handles_plain_output(self):
        original = '"""Header"""\ndef foo():\n    pass\n'
        output = 'def foo():\n    return 42\n'
        cleaned = _clean_llm_output(output, original)
        assert "return 42" in cleaned
