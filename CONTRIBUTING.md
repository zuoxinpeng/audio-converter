# Contributing to Audio Converter

Thank you for your interest in contributing! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/audio-converter.git
   cd audio-converter
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/zuoxinpeng/audio-converter.git
   ```

## Development Setup

### Prerequisites

- Python 3.10+
- FFmpeg
- Git

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (if any)
pip install flake8 black isort

# Verify installation
python scripts/audio_tool.py info --help
```

## Making Changes

### 1. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# OR bug fix branch
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, maintainable code
- Add docstrings to functions
- Include type hints where appropriate
- Add tests if applicable

### 3. Test Your Changes

```bash
# Run syntax check
python -m py_compile scripts/audio_tool.py

# Test with sample files
python scripts/audio_tool.py info test.mp3

# Run linter
flake8 scripts/audio_tool.py --max-line-length=120
```

### 4. Commit Your Changes

```bash
# Stage changes
git add .

# Write clear commit message
git commit -m "Add feature: description

- What changed
- Why it changed
- How to test"
```

## Pull Request Process

1. **Update documentation** if needed
2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Open a Pull Request** on GitHub
4. **Fill in the PR template** completely
5. **Wait for review** - typically 1-3 business days

### PR Title Format

```
<type>: <short description>

Types:
  - feat:     New feature
  - fix:      Bug fix
  - docs:     Documentation only
  - refactor: Code refactoring
  - test:     Adding or updating tests
  - chore:    Maintenance tasks
```

Example:
```
feat: Add batch conversion support for NCM files
```

## Style Guide

### Python Code

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Add docstrings to all public functions
- Maximum line length: 120 characters

### Documentation

- Use clear, concise language
- Include code examples
- Keep README and docs in sync with code

### Git Commits

- Use present tense ("Add feature" not "Added feature")
- First line: 72 characters max
- Include body for detailed explanation

## 🐛 Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) and include:

- Python version
- Operating System
- FFmpeg version
- Steps to reproduce
- Expected vs actual behavior
- Error messages

## 💡 Suggesting Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) and include:

- Clear use case
- Proposed solution
- Alternatives considered

## 📝 Additional Resources

- [GitHub Documentation](https://docs.github.com/)
- [Python Packaging Guide](https://packaging.python.org/)

## Questions?

Open an issue with the "question" label for discussion before submitting a PR.
