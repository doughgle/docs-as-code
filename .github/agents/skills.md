# MCP Server Template - Development Skills

This document provides guidance for AI assistants working with this MCP server template.

## Repository Overview

This is a template repository for creating Model Context Protocol (MCP) servers in Python. It demonstrates best practices and includes all essential components.

## Key Components

### 1. MCP Server Structure
- **Location**: `src/mcp_server_template/server.py`
- **Components**:
  - Tools: Functions the LLM can call
  - Prompts: Pre-defined prompt templates
  - Resources: Data sources accessible by the LLM
  - Instructions: Server-level behavior guidance

### 2. Testing
- **Framework**: pytest with hypothesis for property-based testing
- **Location**: `tests/`
- **Coverage**: Tools, prompts, and resources have comprehensive test coverage
- **Run tests**: `pytest` or `pytest --cov`

### 3. Code Quality
- **Formatter**: black (line length: 100)
- **Linter**: ruff
- **Type Checker**: mypy
- **Run checks**: 
  - `black src/ tests/`
  - `ruff check src/ tests/`
  - `mypy src/`

## Development Workflow

### Adding New Tools
1. Add tool definition to `list_tools()` in `server.py`
2. Add implementation to `call_tool()` in `server.py`
3. Create tests in `tests/test_tools.py`
4. Run tests and type checking

### Adding New Prompts
1. Add prompt definition to `list_prompts()` in `server.py`
2. Add implementation to `get_prompt()` in `server.py`
3. Create tests in `tests/test_prompts.py`
4. Run tests and validation

### Adding New Resources
1. Add resource definition to `list_resources()` in `server.py`
2. Add implementation to `read_resource()` in `server.py`
3. Create tests in `tests/test_resources.py`
4. Verify resource URIs follow convention

## CI/CD Pipeline

### Continuous Integration
- **Workflow**: `.github/workflows/ci.yml`
- **Triggers**: Push to main, pull requests
- **Checks**: Linting, formatting, type checking, tests
- **Python versions**: 3.10, 3.11, 3.12

### Publishing
- **Workflow**: `.github/workflows/publish.yml`
- **Trigger**: Release published
- **Actions**: 
  - Build Python package
  - Publish to PyPI (if PYPI_TOKEN secret is set)
  - Generate server.json for MCP registry
  - Attach server.json to release

## Dependency Management

### Dependabot
- **Config**: `.github/dependabot.yml`
- **Schedule**: Weekly on Mondays
- **Ecosystems**: pip, GitHub Actions
- **Auto-updates**: Dependencies and actions

## Development Environment

### Devcontainer
- **Config**: `.devcontainer/devcontainer.json`
- **Base**: Python 3.12 dev container
- **Extensions**: Python, Pylance, Black, Ruff, Mypy, Copilot, etc.
- **Setup**: Automatic installation of dev dependencies

## Best Practices

### Code Style
- Follow PEP 8 and type hints
- Use async/await for all MCP handlers
- Document all public functions
- Keep line length to 100 characters

### Testing
- Write unit tests for all new functionality
- Use property-based testing for edge cases
- Aim for high code coverage (>80%)
- Test error conditions

### Documentation
- Update README.md for user-facing changes
- Update docstrings for code changes
- Include examples in documentation
- Keep server.json metadata current

### Security
- Never hardcode secrets
- Validate all user inputs
- Use type hints to prevent type errors
- Review dependencies for vulnerabilities

## Common Tasks

### Running the Server Locally
```bash
# Install in development mode
pip install -e '.[dev]'

# Run the server
python -m mcp_server_template.server

# Or use the CLI command
mcp-server-template
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov

# Specific test file
pytest tests/test_tools.py

# Specific test
pytest tests/test_tools.py::TestTools::test_hello_tool
```

### Code Quality Checks
```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run all checks
black src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest
```

### Publishing a Release
1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a git tag: `git tag v0.1.0`
4. Push the tag: `git push origin v0.1.0`
5. Create a GitHub release from the tag
6. CI will automatically publish to PyPI and MCP registry

## Customization Guide

When using this template for a new MCP server:

1. **Update project metadata** in `pyproject.toml`:
   - name
   - description
   - authors
   - dependencies

2. **Update server name** in `server.py`:
   - Change `Server("mcp-server-template")` to your server name

3. **Replace example tools/prompts/resources** with your own

4. **Update tests** to match your implementation

5. **Update README.md** with your server's documentation

6. **Configure secrets**:
   - Add PYPI_TOKEN to GitHub secrets for PyPI publishing

7. **Customize workflows** as needed for your use case

## Troubleshooting

### Tests Failing
- Ensure all dependencies installed: `pip install -e '.[dev]'`
- Check Python version compatibility (3.10+)
- Review test output for specific failures

### Type Errors
- Run `mypy src/` to see detailed type errors
- Ensure all function signatures have type hints
- Check mcp package types are properly imported

### Server Not Starting
- Check logs for error messages
- Verify MCP package is installed
- Ensure async/await is used correctly

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [Example MCP Servers](https://modelcontextprotocol.io/examples)
