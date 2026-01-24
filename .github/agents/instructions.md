# Repository Instructions for AI Assistants

## Purpose
This repository is a **template** for creating Model Context Protocol (MCP) servers in Python. It provides a complete, production-ready starting point with all essential components.

## When Working on This Repository

### Understand the Template Nature
- This is a template meant to be forked/cloned by users
- Keep examples simple and educational
- Maintain clear separation between template code and customization points
- Prioritize clarity over complexity

### Code Changes
- **Minimal Changes**: Only modify what's necessary
- **Test Coverage**: Always add/update tests for code changes
- **Type Safety**: Maintain full type hints
- **Documentation**: Update relevant docs with code changes

### Testing Requirements
- All new features must have unit tests
- Use hypothesis for property-based testing where appropriate
- Maintain >80% code coverage
- Test both success and error cases

### Code Quality Standards
- **Formatting**: Use black with 100 character line length
- **Linting**: Pass ruff checks
- **Type Checking**: Pass mypy without errors
- **Async/Await**: All MCP handlers must be async

### File Organization
```
src/mcp_server_template/
  __init__.py          # Package initialization
  server.py            # Main server with all components

tests/
  test_tools.py        # Tool tests
  test_prompts.py      # Prompt tests
  test_resources.py    # Resource tests

.github/
  workflows/
    ci.yml            # Continuous integration
    publish.yml       # Publishing to registries
  dependabot.yml      # Dependency updates
  agents/
    skills.md         # Development skills guide
    instructions.md   # This file
```

### Making Changes

#### Adding Features
1. Determine which component (tool/prompt/resource) to modify
2. Update the implementation in `server.py`
3. Add comprehensive tests
4. Run all quality checks (black, ruff, mypy, pytest)
5. Update documentation

#### Bug Fixes
1. Write a failing test that demonstrates the bug
2. Fix the bug with minimal changes
3. Verify the test passes
4. Check for similar issues elsewhere
5. Update relevant documentation

#### Documentation Updates
1. Keep README.md focused on user getting started
2. Keep skills.md focused on developer workflow
3. Include code examples where helpful
4. Update version-specific information when releasing

### CI/CD Workflows

#### CI Workflow
- Runs on: Push to main, Pull Requests
- Python versions: 3.10, 3.11, 3.12
- Checks: Linting, formatting, type checking, tests
- Coverage: Uploads to Codecov

#### Publish Workflow
- Runs on: Release published
- Actions: Build, publish to PyPI, create server.json
- Requirements: PYPI_TOKEN secret must be configured

### Dependency Management
- Dependabot runs weekly on Mondays
- Reviews required for major version updates
- Test thoroughly before merging dependency updates

### Security Considerations
- Never commit secrets or tokens
- Validate all external inputs
- Review dependencies for vulnerabilities
- Use type hints to prevent type errors
- Follow principle of least privilege

### Development Environment
- Use the devcontainer for consistent environment
- Or manually install with: `pip install -e '.[dev]'`
- VS Code extensions configured automatically

### Common Pitfalls to Avoid

1. **Breaking Template Structure**: Don't remove example components without replacement
2. **Incomplete Type Hints**: All functions must have full type annotations
3. **Missing Tests**: Every feature needs tests
4. **Undocumented Changes**: Update docs with code changes
5. **Hardcoded Values**: Use configuration for environment-specific values
6. **Blocking Code**: All MCP operations must be async

### Review Checklist

Before submitting changes:
- [ ] Tests pass: `pytest`
- [ ] Code formatted: `black src/ tests/`
- [ ] Linting passes: `ruff check src/ tests/`
- [ ] Type checking passes: `mypy src/`
- [ ] Documentation updated
- [ ] Example code still works
- [ ] No secrets committed
- [ ] Breaking changes documented

### Release Process

When creating a new release:
1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with changes
3. Create and push git tag (e.g., `v0.2.0`)
4. Create GitHub release
5. CI automatically publishes to PyPI
6. Verify package on PyPI
7. Test installation: `uvx mcp-server-template`

### Support for Users

When users report issues:
1. Ask for their environment (Python version, OS)
2. Request full error messages
3. Check if it's a template usage issue vs bug
4. Guide them to relevant documentation
5. Create issues for actual bugs

### Maintaining Example Quality

The examples in this template should:
- Demonstrate all MCP components (tools, prompts, resources)
- Show best practices
- Be simple enough to understand quickly
- Be complex enough to be useful
- Include error handling
- Have comprehensive tests

### Performance Considerations
- Keep operations fast and non-blocking
- Use async/await properly
- Don't perform expensive operations in list handlers
- Cache data when appropriate
- Log performance issues

### Compatibility
- Support Python 3.10+ (as specified in pyproject.toml)
- Use features available in all supported versions
- Test on all supported Python versions in CI
- Document breaking changes clearly

## Quick Reference Commands

```bash
# Setup
pip install -e '.[dev]'

# Run all checks
black src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest --cov

# Run server
python -m mcp_server_template.server

# Single test file
pytest tests/test_tools.py -v

# With coverage report
pytest --cov --cov-report=html
```

## Getting Help

- MCP Documentation: https://modelcontextprotocol.io/
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Example Servers: https://modelcontextprotocol.io/examples
- Registry: https://registry.modelcontextprotocol.io/

## Remember

This template exists to help developers quickly start building MCP servers. Every change should make that goal easier, clearer, or more robust.
