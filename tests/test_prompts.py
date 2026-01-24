"""Unit tests for MCP server prompts."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mcp_server_template.server import get_prompt, list_prompts


class TestPrompts:
    """Test suite for MCP prompts."""

    @pytest.mark.asyncio
    async def test_list_prompts(self):
        """Test that list_prompts returns expected prompts."""
        prompts = await list_prompts()
        assert len(prompts) == 2
        prompt_names = [prompt.name for prompt in prompts]
        assert "greeting" in prompt_names
        assert "code_review" in prompt_names

    @pytest.mark.asyncio
    async def test_greeting_prompt_casual(self):
        """Test greeting prompt with casual style."""
        result = await get_prompt("greeting", {"style": "casual"})
        assert result.description == "A casual greeting"
        assert len(result.messages) == 1
        assert "Hey there" in result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_greeting_prompt_formal(self):
        """Test greeting prompt with formal style."""
        result = await get_prompt("greeting", {"style": "formal"})
        assert result.description == "A formal greeting"
        assert len(result.messages) == 1
        assert "Good day" in result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_greeting_prompt_default(self):
        """Test greeting prompt with default style."""
        result = await get_prompt("greeting", None)
        assert "casual" in result.description
        assert len(result.messages) == 1

    @pytest.mark.asyncio
    async def test_code_review_prompt(self):
        """Test code review prompt with Python."""
        result = await get_prompt("code_review", {"language": "Python"})
        assert "Python" in result.description
        assert len(result.messages) == 1
        assert "Python" in result.messages[0].content.text
        assert "best practices" in result.messages[0].content.text.lower()

    @pytest.mark.asyncio
    async def test_code_review_prompt_javascript(self):
        """Test code review prompt with JavaScript."""
        result = await get_prompt("code_review", {"language": "JavaScript"})
        assert "JavaScript" in result.description
        assert "JavaScript" in result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_unknown_prompt(self):
        """Test that unknown prompts raise an error."""
        with pytest.raises(ValueError, match="Unknown prompt"):
            await get_prompt("unknown", None)

    # Property-based tests
    @given(st.text(min_size=1, max_size=50))
    @pytest.mark.asyncio
    async def test_code_review_with_any_language(self, language: str):
        """Test code review prompt with any language name."""
        result = await get_prompt("code_review", {"language": language})
        assert language in result.description
        assert language in result.messages[0].content.text
