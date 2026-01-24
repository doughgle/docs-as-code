"""Unit tests for MCP server tools."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mcp_server_template.server import call_tool, list_tools


class TestTools:
    """Test suite for MCP tools."""

    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test that list_tools returns expected tools."""
        tools = await list_tools()
        assert len(tools) == 2
        tool_names = [tool.name for tool in tools]
        assert "hello" in tool_names
        assert "add" in tool_names

    @pytest.mark.asyncio
    async def test_hello_tool(self):
        """Test the hello tool with a specific name."""
        result = await call_tool("hello", {"name": "Alice"})
        assert len(result) == 1
        assert "Alice" in result[0].text
        assert "👋" in result[0].text

    @pytest.mark.asyncio
    async def test_hello_tool_default(self):
        """Test the hello tool with no name provided."""
        result = await call_tool("hello", {})
        assert len(result) == 1
        assert "World" in result[0].text

    @pytest.mark.asyncio
    async def test_add_tool(self):
        """Test the add tool with positive numbers."""
        result = await call_tool("add", {"a": 5, "b": 3})
        assert len(result) == 1
        assert "8" in result[0].text

    @pytest.mark.asyncio
    async def test_add_tool_negative(self):
        """Test the add tool with negative numbers."""
        result = await call_tool("add", {"a": -5, "b": 3})
        assert len(result) == 1
        assert "-2" in result[0].text

    @pytest.mark.asyncio
    async def test_add_tool_zero(self):
        """Test the add tool with zero."""
        result = await call_tool("add", {"a": 0, "b": 0})
        assert len(result) == 1
        assert "0" in result[0].text

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        """Test that unknown tools raise an error."""
        with pytest.raises(ValueError, match="Unknown tool"):
            await call_tool("unknown", {})

    # Property-based tests using hypothesis
    @given(st.text(min_size=1, max_size=100))
    @pytest.mark.asyncio
    async def test_hello_with_any_name(self, name: str):
        """Test hello tool with any valid string name."""
        result = await call_tool("hello", {"name": name})
        assert len(result) == 1
        assert name in result[0].text

    @given(st.integers(), st.integers())
    @pytest.mark.asyncio
    async def test_add_with_any_integers(self, a: int, b: int):
        """Test add tool with any integers."""
        result = await call_tool("add", {"a": a, "b": b})
        assert len(result) == 1
        expected_sum = a + b
        assert str(expected_sum) in result[0].text

    @given(st.floats(allow_nan=False, allow_infinity=False))
    @pytest.mark.asyncio
    async def test_add_with_floats(self, a: float):
        """Test add tool with float numbers."""
        b = 1.5
        result = await call_tool("add", {"a": a, "b": b})
        assert len(result) == 1
        # Result should contain some numeric representation
        assert result[0].text is not None
