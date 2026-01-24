"""Unit tests for MCP server resources."""

import pytest

from mcp_server_template.server import list_resources, read_resource


class TestResources:
    """Test suite for MCP resources."""

    @pytest.mark.asyncio
    async def test_list_resources(self):
        """Test that list_resources returns expected resources."""
        resources = await list_resources()
        assert len(resources) == 2
        resource_uris = [r["uri"] for r in resources]
        assert "template://info" in resource_uris
        assert "template://examples" in resource_uris

    @pytest.mark.asyncio
    async def test_resource_structure(self):
        """Test that resources have required fields."""
        resources = await list_resources()
        for resource in resources:
            assert "uri" in resource
            assert "name" in resource
            assert "description" in resource
            assert "mimeType" in resource

    @pytest.mark.asyncio
    async def test_read_info_resource(self):
        """Test reading the info resource."""
        content = await read_resource("template://info")
        assert "MCP Server Template" in content
        assert "Tools" in content
        assert "Prompts" in content
        assert "Resources" in content

    @pytest.mark.asyncio
    async def test_read_examples_resource(self):
        """Test reading the examples resource."""
        content = await read_resource("template://examples")
        assert "hello" in content
        assert "add" in content
        assert "call_tool" in content

    @pytest.mark.asyncio
    async def test_read_unknown_resource(self):
        """Test that unknown resources raise an error."""
        with pytest.raises(ValueError, match="Unknown resource"):
            await read_resource("template://unknown")

    @pytest.mark.asyncio
    async def test_read_invalid_uri(self):
        """Test that invalid URIs raise an error."""
        with pytest.raises(ValueError):
            await read_resource("invalid://uri")
