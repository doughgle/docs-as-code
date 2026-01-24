# MCP Server Template 🚀

A production-ready template repository for creating [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers in Python. Get started building your own MCP server in minutes with comprehensive examples, testing, and CI/CD built-in.

[![CI](https://github.com/doughgle/docs-as-code/actions/workflows/ci.yml/badge.svg)](https://github.com/doughgle/docs-as-code/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features ✨

- 🎯 **Complete MCP Components**: Examples of tools, prompts, resources, and instructions
- 🧪 **Comprehensive Testing**: Unit tests with pytest and property-based testing with hypothesis
- 🔄 **Automated Dependency Updates**: Dependabot configured for Python and GitHub Actions
- 🏗️ **CI/CD Pipeline**: GitHub Actions for testing and publishing to PyPI and MCP registry
- 🐳 **Development Container**: VSCode devcontainer with all extensions pre-configured
- 🤖 **LLM-Friendly**: Repository-level skills and instructions for AI assistants
- 📦 **Easy Publishing**: One-click release to public MCP server registry for VSCode discoverability

## Quick Start 🏃

### Use This Template

1. Click "Use this template" button on GitHub
2. Clone your new repository
3. Customize for your use case

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/your-mcp-server.git
cd your-mcp-server

# Install in development mode
pip install -e '.[dev]'

# Run tests
pytest

# Run the server
python -m mcp_server_template.server
```

### Using the Devcontainer

1. Open in VS Code
2. Click "Reopen in Container" when prompted
3. Everything is automatically set up!

## What's Included 📦

### MCP Server Components

The template demonstrates all key MCP server components:

#### 🛠️ **Tools**
Functions that the LLM can call to perform actions:
- `hello`: Returns a friendly greeting
- `add`: Adds two numbers together

#### 💬 **Prompts**
Pre-defined templates for common interactions:
- `greeting`: Customizable greeting (formal/casual)
- `code_review`: Code review prompt template

#### 📚 **Resources**
Data sources accessible by the LLM:
- `template://info`: Information about the template
- `template://examples`: Example code snippets

#### 📋 **Instructions**
Server-level guidance for LLM behavior (configurable)

### Testing Infrastructure

- **pytest**: Fast, feature-rich testing framework
- **hypothesis**: Property-based testing for edge cases
- **pytest-cov**: Code coverage reporting
- **pytest-asyncio**: Async test support

Example test structure:
```python
@pytest.mark.asyncio
async def test_hello_tool():
    result = await call_tool("hello", {"name": "Alice"})
    assert "Alice" in result[0].text

@given(st.integers(), st.integers())
@pytest.mark.asyncio
async def test_add_with_any_integers(a: int, b: int):
    result = await call_tool("add", {"a": a, "b": b})
    assert str(a + b) in result[0].text
```

### CI/CD Workflows

#### Continuous Integration (`.github/workflows/ci.yml`)
- Runs on every push and pull request
- Tests on Python 3.10, 3.11, and 3.12
- Checks: linting (ruff), formatting (black), type checking (mypy), tests (pytest)
- Uploads coverage to Codecov

#### Publishing (`.github/workflows/publish.yml`)
- Triggers on GitHub releases
- Builds and publishes to PyPI
- Generates `server.json` for MCP registry
- Attaches metadata to release

### Dependency Management

Dependabot automatically opens PRs for:
- Python package updates (weekly)
- GitHub Actions updates (weekly)

Configuration in `.github/dependabot.yml`

## Usage Examples 💡

### Adding the Server to Claude Desktop

Add to your Claude configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcp-server-template": {
      "command": "uvx",
      "args": ["mcp-server-template"]
    }
  }
}
```

### Adding to VSCode

1. Open VSCode settings
2. Enable MCP gallery: `chat.mcp.gallery.enabled`
3. Open Extensions view
4. Search for `@mcp mcp-server-template`
5. Click install

Or add directly to VSCode MCP config.

## Customization Guide 🔧

### 1. Update Project Metadata

Edit `pyproject.toml`:
```toml
[project]
name = "your-mcp-server"
version = "0.1.0"
description = "Your server description"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
```

### 2. Rename the Server

In `src/mcp_server_template/server.py`:
```python
server = Server("your-server-name")
```

### 3. Add Your Tools

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="your_tool",
            description="What your tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "Parameter description"}
                },
                "required": ["param"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "your_tool":
        # Your implementation
        return [TextContent(type="text", text="Result")]
```

### 4. Add Tests

Create tests in `tests/test_tools.py`:
```python
@pytest.mark.asyncio
async def test_your_tool():
    result = await call_tool("your_tool", {"param": "value"})
    assert result[0].text == "Expected output"
```

### 5. Run Quality Checks

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run tests
pytest --cov
```

## Publishing Your Server 🚀

### To PyPI (for `uvx` installation)

1. Set up PyPI token in GitHub secrets as `PYPI_TOKEN`
2. Update version in `pyproject.toml`
3. Create a git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. Create a GitHub release
6. CI automatically publishes to PyPI

Users can then install with:
```bash
uvx your-mcp-server
```

### To MCP Registry (for VSCode discoverability)

The publish workflow automatically generates and attaches `server.json` to your GitHub release, which can be submitted to the MCP registry following their submission process.

## Development Tips 💡

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov --cov-report=html

# Specific test file
pytest tests/test_tools.py

# Watch mode (requires pytest-watch)
ptw
```

### Code Quality
```bash
# Run all checks
black src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest

# Auto-fix linting issues
ruff check --fix src/ tests/
```

### Debugging
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python -m mcp_server_template.server

# Use pytest debugging
pytest --pdb  # Drop into debugger on failure
```

## Project Structure 📁

```
.
├── src/
│   └── mcp_server_template/
│       ├── __init__.py           # Package initialization
│       └── server.py              # MCP server implementation
├── tests/
│   ├── __init__.py
│   ├── test_tools.py              # Tool tests
│   ├── test_prompts.py            # Prompt tests
│   └── test_resources.py          # Resource tests
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # Continuous integration
│   │   └── publish.yml            # Publishing workflow
│   ├── dependabot.yml             # Dependency updates
│   └── agents/
│       ├── skills.md              # Development skills for LLMs
│       └── instructions.md         # Instructions for LLMs
├── .devcontainer/
│   └── devcontainer.json          # VS Code devcontainer config
├── pyproject.toml                 # Project configuration
└── README.md                      # This file
```

## Requirements 📋

- Python 3.10 or higher
- pip (for installing dependencies)

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Resources 📚

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Example MCP Servers](https://modelcontextprotocol.io/examples)
- [MCP Registry](https://registry.modelcontextprotocol.io/)

## License 📄

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

This template is inspired by:
- [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- [aj-geddes/python-mcp-server-template](https://github.com/aj-geddes/python-mcp-server-template)
- MCP community examples and best practices

---

**Ready to build your MCP server?** Click "Use this template" to get started! 🎉
