# Contributing to Audio Converter

Thank you for your interest in contributing!

## How to Contribute

### Reporting Bugs

1. Search existing issues first
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version, OS, FFmpeg version
   - Error messages or logs

### Suggesting Features

1. Search existing issues first
2. Open a new issue with:
   - Clear use case
   - Expected behavior
   - Alternative solutions considered

### Pull Requests

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and create a Pull Request

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings for functions
- Include type hints where helpful

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/audio-converter.git
cd audio-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python audio_tool.py info test_audio.mp3
```

## Project Structure

```
audio-converter/
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
├── scripts/
│   └── audio_tool.py    # Main CLI tool
└── docs/
    └── README.cn.md     # Chinese documentation
```

## Questions?

Open an issue for discussion before submitting a PR.
