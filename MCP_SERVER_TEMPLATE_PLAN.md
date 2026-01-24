# MCP Server Template Enhancement Plan

## Overview

This plan outlines the enhancements needed for the forked `python-mcp-starter` repository to create a production-ready MCP server template that meets all specified requirements.

**Base Repository**: https://github.com/ltwlf/python-mcp-starter  
**Target**: Enhanced template for fast feedback dev/test workflow with LLM-discoverable guardrails and public registry publishing

---

## Current State of python-mcp-starter

The python-mcp-starter already provides:
- ✅ MCP server skeleton using FastMCP and Python SDK
- ✅ Example tools and resources
- ✅ Docker and docker-compose setup
- ✅ VS Code debugging configuration (.vscode/)
- ✅ GitHub Actions workflows (.github/)
- ✅ Development container (.devcontainer/)
- ✅ Basic project structure with pyproject.toml
- ✅ Sample server package (hello_mcp_server/)
- ✅ Test infrastructure (tests/)

---

## Requirements Analysis

### Requirement 1: Template Git Repository ✅
**Status**: Already met by python-mcp-starter  
**Action**: Configure repository settings to enable "Use this template" on GitHub

### Requirement 2: Skeleton Code for Hello World MCP Server ✅
**Status**: Partially met - has hello_mcp_server example  
**Actions**:
- Review and enhance example to demonstrate ALL MCP components
- Ensure clear examples of:
  - Tools with various input schemas
  - Prompts with arguments
  - Resources with different URI schemes
  - Instructions for LLM behavior

### Requirement 2.1: Show Each Component of MCP Server 🔄
**Status**: Needs enhancement  
**Actions**:
1. Add comprehensive examples to hello_mcp_server/ showing:
   - **Tools**: Multiple examples with different parameter types
   - **Prompts**: Pre-defined prompt templates with arguments
   - **Resources**: Static and dynamic resources
   - **Instructions**: Server-level instructions for LLMs
   - **Sampling**: LLM text completion examples (if applicable)

2. Create separate module files:
   ```
   hello_mcp_server/
   ├── __init__.py
   ├── tools/
   │   ├── __init__.py
   │   ├── greeting.py      # Simple tool example
   │   └── calculator.py    # Tool with validation
   ├── prompts/
   │   ├── __init__.py
   │   └── templates.py     # Prompt templates
   ├── resources/
   │   ├── __init__.py
   │   └── data.py          # Resource examples
   └── server.py            # Main server setup
   ```

### Requirement 3: Example Unit Tests with pytest and hypothesis 🔄
**Status**: Basic tests exist, need enhancement  
**Actions**:
1. Expand test coverage to include:
   - Property-based tests using hypothesis
   - Tests for each tool, prompt, and resource
   - Edge case testing
   - Async operation testing

2. Update test files:
   ```
   tests/
   ├── __init__.py
   ├── test_tools.py           # Tool tests with hypothesis
   ├── test_prompts.py         # Prompt tests
   ├── test_resources.py       # Resource tests
   └── test_integration.py     # Integration tests
   ```

3. Add pytest configuration to pyproject.toml:
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   asyncio_mode = "auto"
   addopts = "-v --cov=hello_mcp_server --cov-report=term-missing --cov-report=html"
   ```

### Requirement 4: Automated Dependency Management 🔄
**Status**: Needs Dependabot configuration  
**Actions**:
1. Create `.github/dependabot.yml`:
   ```yaml
   version: 2
   updates:
     - package-ecosystem: "pip"
       directory: "/"
       schedule:
         interval: "weekly"
         day: "monday"
       open-pull-requests-limit: 10
       labels:
         - "dependencies"
         - "python"
     - package-ecosystem: "github-actions"
       directory: "/"
       schedule:
         interval: "weekly"
       open-pull-requests-limit: 5
       labels:
         - "dependencies"
         - "github-actions"
   ```

### Requirement 5: GitHub Workflows for Build ✅
**Status**: Already has workflows, may need enhancement  
**Actions**:
1. Review existing workflows in `.github/workflows/`
2. Ensure CI workflow includes:
   - Matrix testing across Python 3.10, 3.11, 3.12
   - Linting (ruff)
   - Formatting checks (black)
   - Type checking (mypy)
   - Test execution with coverage
   - Security scanning

3. Example CI workflow structure:
   ```yaml
   name: CI
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ["3.10", "3.11", "3.12"]
       steps:
         - uses: actions/checkout@v4
         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: ${{ matrix.python-version }}
         - name: Install dependencies
           run: |
             pip install -e ".[dev]"
         - name: Lint and format checks
           run: |
             ruff check .
             black --check .
         - name: Type checking
           run: mypy hello_mcp_server/
         - name: Run tests
           run: pytest --cov
   ```

### Requirement 6: Publish to Public MCP Registry ❌
**Status**: Not implemented  
**Actions**:
1. Create `.github/workflows/publish.yml` for release automation:
   ```yaml
   name: Publish to MCP Registry
   
   on:
     release:
       types: [published]
   
   jobs:
     publish:
       runs-on: ubuntu-latest
       permissions:
         contents: write
       steps:
         - uses: actions/checkout@v4
         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: "3.12"
         - name: Build package
           run: |
             pip install build
             python -m build
         - name: Generate server.json
           run: |
             cat > server.json << 'EOF'
             {
               "name": "your-mcp-server",
               "version": "${{ github.event.release.tag_name }}",
               "description": "Your MCP server description",
               "homepage": "${{ github.event.repository.html_url }}",
               "repository": {
                 "type": "git",
                 "url": "${{ github.event.repository.clone_url }}"
               },
               "runtime": {
                 "type": "python",
                 "command": "uvx",
                 "args": ["your-mcp-server"]
               },
               "capabilities": {
                 "tools": true,
                 "prompts": true,
                 "resources": true
               }
             }
             EOF
         - name: Publish to PyPI
           if: env.PYPI_TOKEN != ''
           env:
             TWINE_USERNAME: __token__
             TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
           run: |
             pip install twine
             twine upload dist/*
         - name: Upload server.json
           uses: actions/upload-release-asset@v1
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
           with:
             upload_url: ${{ github.event.release.upload_url }}
             asset_path: ./server.json
             asset_name: server.json
             asset_content_type: application/json
   ```

2. Update README with publishing instructions:
   - How to configure PyPI token
   - How to create releases
   - How to submit to MCP registry
   - VSCode installation instructions

### Requirement 7: Devcontainer with VSCode Extensions ✅
**Status**: Already has .devcontainer/, needs verification/enhancement  
**Actions**:
1. Review `.devcontainer/devcontainer.json`
2. Ensure it includes essential extensions:
   ```json
   {
     "name": "MCP Server Development",
     "image": "mcr.microsoft.com/devcontainers/python:3.12",
     "customizations": {
       "vscode": {
         "extensions": [
           "ms-python.python",
           "ms-python.vscode-pylance",
           "ms-python.black-formatter",
           "charliermarsh.ruff",
           "ms-python.mypy-type-checker",
           "GitHub.copilot",
           "GitHub.copilot-chat",
           "tamasfe.even-better-toml",
           "eamodio.gitlens"
         ],
         "settings": {
           "python.defaultInterpreterPath": "/usr/local/bin/python",
           "python.testing.pytestEnabled": true,
           "editor.formatOnSave": true,
           "[python]": {
             "editor.defaultFormatter": "ms-python.black-formatter"
           }
         }
       }
     },
     "postCreateCommand": "pip install -e '.[dev]'"
   }
   ```

### Requirement 8: Repo-level Skills and Instructions for LLMs ❌
**Status**: Not implemented  
**Actions**:
1. Create `.github/agents/` directory
2. Create `.github/agents/skills.md`:
   - Development workflow guide
   - Common tasks and commands
   - Project structure explanation
   - Testing procedures
   - Deployment process
   - Troubleshooting guide

3. Create `.github/agents/instructions.md`:
   - Code standards and best practices
   - Contribution guidelines
   - Security considerations
   - File organization rules
   - Testing requirements
   - Documentation expectations

---

## Implementation Checklist

### Phase 1: Repository Setup
- [ ] Fork https://github.com/ltwlf/python-mcp-starter
- [ ] Enable "Use this template" in repository settings
- [ ] Update repository description and topics

### Phase 2: Enhance MCP Server Examples
- [ ] Restructure hello_mcp_server/ with separate tool/prompt/resource modules
- [ ] Add comprehensive tool examples
- [ ] Add prompt template examples
- [ ] Add resource examples (static and dynamic)
- [ ] Add server-level instructions
- [ ] Update main.py with clear documentation

### Phase 3: Testing Infrastructure
- [ ] Add hypothesis to dev dependencies
- [ ] Create comprehensive test suite:
  - [ ] test_tools.py with property-based tests
  - [ ] test_prompts.py
  - [ ] test_resources.py
  - [ ] test_integration.py
- [ ] Configure pytest in pyproject.toml
- [ ] Add test coverage reporting
- [ ] Ensure all tests pass

### Phase 4: CI/CD and Automation
- [ ] Review and enhance existing CI workflows
- [ ] Add/verify matrix testing for Python 3.10, 3.11, 3.12
- [ ] Add linting, formatting, and type checking to CI
- [ ] Create publish workflow for releases
- [ ] Add Dependabot configuration
- [ ] Test workflows with a test release

### Phase 5: Development Environment
- [ ] Review and enhance .devcontainer configuration
- [ ] Verify all necessary VSCode extensions are included
- [ ] Test devcontainer setup
- [ ] Add development documentation

### Phase 6: LLM Documentation
- [ ] Create .github/agents/ directory
- [ ] Write comprehensive skills.md
- [ ] Write detailed instructions.md
- [ ] Include examples and best practices

### Phase 7: Documentation
- [ ] Update README.md with:
  - [ ] Quick start guide
  - [ ] Usage examples for all MCP components
  - [ ] Publishing instructions
  - [ ] VSCode integration guide
  - [ ] Customization guide
- [ ] Create CHANGELOG.md
- [ ] Create/update CONTRIBUTING.md
- [ ] Add inline code documentation

### Phase 8: Publishing Setup
- [ ] Configure pyproject.toml for PyPI publishing
- [ ] Create server.json template
- [ ] Document PyPI token setup
- [ ] Document MCP registry submission process
- [ ] Test release workflow

### Phase 9: Quality Assurance
- [ ] Run all tests and ensure they pass
- [ ] Run code quality checks (black, ruff, mypy)
- [ ] Security scan with CodeQL
- [ ] Dependency vulnerability check
- [ ] Documentation review
- [ ] Example code verification

### Phase 10: Final Touches
- [ ] Add badges to README (CI, coverage, license, etc.)
- [ ] Add LICENSE file (if not present)
- [ ] Create .gitignore for Python projects
- [ ] Add template repository settings JSON
- [ ] Final integration test

---

## Key Files to Create/Modify

### New Files to Create:
1. `.github/dependabot.yml` - Automated dependency updates
2. `.github/workflows/publish.yml` - Publishing automation
3. `.github/agents/skills.md` - Developer skills guide
4. `.github/agents/instructions.md` - LLM instructions
5. `CHANGELOG.md` - Version history
6. `CONTRIBUTING.md` - Contribution guidelines
7. `.github/template-repository-settings.json` - Template config
8. `server.json.template` - MCP registry metadata template
9. Enhanced test files with hypothesis

### Files to Modify:
1. `README.md` - Comprehensive documentation
2. `pyproject.toml` - Add dependencies, configure tools
3. `.devcontainer/devcontainer.json` - Verify/enhance extensions
4. `.github/workflows/*.yml` - Enhance CI workflows
5. `hello_mcp_server/` - Restructure and enhance examples
6. `tests/` - Expand test coverage
7. `.gitignore` - Ensure comprehensive coverage

---

## Technical Requirements

### Python Dependencies to Add:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "hypothesis>=6.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

### Code Quality Standards:
- **Formatting**: Black (line length: 100)
- **Linting**: Ruff with rules: E, F, I, N, W, UP
- **Type Checking**: MyPy with strict settings
- **Testing**: pytest with 80%+ coverage target
- **Python Version**: 3.10+ support

---

## MCP Component Examples to Include

### Tools Examples:
1. **Simple Tool**: Greeting function
2. **Data Processing**: Calculator or text transformer
3. **Async Tool**: API call or database query
4. **Complex Tool**: Multi-step operation with validation

### Prompts Examples:
1. **Simple Prompt**: Basic template
2. **Parametric Prompt**: With required/optional arguments
3. **Multi-message Prompt**: Complex conversation starter

### Resources Examples:
1. **Static Resource**: Info/help text
2. **Dynamic Resource**: Generated data
3. **External Resource**: File or API data

### Instructions Example:
- Server-level guidance on tool usage
- Context about server capabilities
- Usage recommendations

---

## Testing Strategy

### Unit Tests:
- Test each tool individually
- Test prompt generation
- Test resource access
- Mock external dependencies

### Property-Based Tests (Hypothesis):
- Generate random but valid inputs
- Test edge cases automatically
- Verify invariants hold

### Integration Tests:
- Test complete MCP server flow
- Test tool registration
- Test error handling

### Coverage Goals:
- Minimum 80% code coverage
- 100% coverage for critical paths
- All public APIs tested

---

## Publishing Guide

### PyPI Publishing:
1. Configure `PYPI_TOKEN` secret in GitHub
2. Update version in pyproject.toml
3. Create git tag (e.g., v0.1.0)
4. Create GitHub release
5. Workflow automatically publishes to PyPI

### MCP Registry Submission:
1. server.json is generated on release
2. Download from release assets
3. Submit to MCP registry following their process
4. Server becomes discoverable in VSCode

### VSCode Integration:
Users can install via:
```bash
uvx your-mcp-server
```

Or in Claude Desktop/VSCode config:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "uvx",
      "args": ["your-mcp-server"]
    }
  }
}
```

---

## Success Criteria

The enhanced template will be considered complete when:

1. ✅ All MCP components (tools, prompts, resources, instructions) have clear examples
2. ✅ Test suite has 80%+ coverage with pytest and hypothesis
3. ✅ Dependabot is configured and creating PRs
4. ✅ CI workflow passes on all Python versions (3.10, 3.11, 3.12)
5. ✅ Publishing workflow successfully creates releases
6. ✅ Devcontainer works with all configured extensions
7. ✅ LLM documentation (skills.md, instructions.md) is comprehensive
8. ✅ README includes complete quick start and usage guide
9. ✅ server.json is generated for MCP registry
10. ✅ All code quality checks pass (black, ruff, mypy)
11. ✅ Security scans show no vulnerabilities
12. ✅ Template repository feature is enabled

---

## Usage Instructions for New Users

Once completed, users should be able to:

1. Click "Use this template" on GitHub
2. Clone their new repository
3. Open in VSCode (devcontainer auto-configures)
4. Run `pytest` to verify setup
5. Customize server name and tools
6. Run tests to ensure changes work
7. Create a release to publish
8. See their server in VSCode MCP gallery

---

## Notes and Considerations

- **FastMCP**: python-mcp-starter uses FastMCP which may have different APIs than vanilla mcp SDK
- **Project Naming**: Guide users to rename `hello_mcp_server` to their project name
- **Docker**: The existing Docker setup should be maintained and documented
- **UV Package Manager**: python-mcp-starter uses `uv` - ensure compatibility
- **Debugging**: Existing VS Code debug config should be preserved
- **Examples**: Keep examples simple but comprehensive enough to teach

---

## Resources and References

- python-mcp-starter: https://github.com/ltwlf/python-mcp-starter
- MCP Documentation: https://modelcontextprotocol.io/
- FastMCP: Documentation for the framework used
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP Registry: https://registry.modelcontextprotocol.io/
- Example Servers: https://modelcontextprotocol.io/examples

---

## Estimated Effort

- **Phase 1-2**: 2-3 hours (Setup and examples)
- **Phase 3**: 2-3 hours (Testing)
- **Phase 4**: 1-2 hours (CI/CD)
- **Phase 5**: 1 hour (Dev environment)
- **Phase 6**: 2-3 hours (LLM documentation)
- **Phase 7**: 2-3 hours (Documentation)
- **Phase 8**: 1-2 hours (Publishing)
- **Phase 9-10**: 2-3 hours (QA and final touches)

**Total**: 13-20 hours of focused work

---

## Priority Order

For incremental implementation, prioritize:

1. **High Priority** (Core functionality):
   - Enhanced MCP component examples
   - Comprehensive test suite
   - CI workflow enhancements
   - Publishing workflow

2. **Medium Priority** (Quality & Automation):
   - Dependabot configuration
   - LLM documentation
   - Code quality tools setup
   - Documentation updates

3. **Low Priority** (Nice to have):
   - Template repository settings
   - Advanced examples
   - Additional integrations
   - Extended documentation

---

*End of Plan*
