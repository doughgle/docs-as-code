# Contributing to MCP Server Template

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Code samples** if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

- Use a clear and descriptive title
- Provide detailed description of the enhancement
- Explain why this would be useful
- Include code examples if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests
5. Ensure all tests pass
6. Update documentation
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Process

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/mcp-server-template.git
cd mcp-server-template

# Install in development mode
pip install -e '.[dev]'

# Or use the devcontainer in VS Code
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_tools.py

# Run with verbose output
pytest -v
```

### Code Quality

Before submitting a PR, ensure:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run tests
pytest --cov
```

All checks must pass for PR to be merged.

### Code Style

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for public functions
- Keep line length to 100 characters
- Use async/await for all MCP handlers

### Testing Guidelines

- Write unit tests for all new features
- Use property-based testing for edge cases
- Aim for >80% code coverage
- Test both success and error cases
- Use descriptive test names

### Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples where helpful
- Keep documentation clear and concise

### Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Keep first line under 72 characters
- Add detailed description if needed

Examples:
```
Add support for custom resource handlers
Fix tool argument validation
Update documentation for new prompt types
```

## Project Structure

```
src/mcp_server_template/
  __init__.py          # Package initialization
  server.py            # Main server implementation

tests/
  test_tools.py        # Tool tests
  test_prompts.py      # Prompt tests
  test_resources.py    # Resource tests

.github/
  workflows/           # CI/CD workflows
  dependabot.yml       # Dependency updates
  agents/              # LLM instructions
```

## Release Process

Maintainers handle releases:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag
4. Push tag to trigger release workflow
5. GitHub Actions publishes to PyPI

## Questions?

Feel free to open an issue for questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
