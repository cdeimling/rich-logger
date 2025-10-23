# rich-reporter

[![CI](https://github.com/cdeimling/rich-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/cdeimling/rich-logger/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Unified Rich-based Logging & Reporting Utility**

A lightweight Python package that combines [Rich](https://github.com/Textualize/rich) Console functionality with structured logging and automatic statistics collection. Get a fully configured logger and beautiful console output in a single call!

## ✨ Features

- 🎨 **Beautiful Console Output**: Built on Rich for gorgeous terminal output
- 📊 **Automatic Statistics**: Tracks log counts at all levels (debug, info, warning, error, critical)
- 🔧 **Zero Boilerplate**: Get a fully configured logger and console in one call
- 📋 **Summary Reports**: Generate beautiful summary panels at the end of your process
- 🎯 **Context Manager Support**: Automatic reporting when using `with` statements
- 📁 **File Logging**: Optional file handler support
- 🔌 **Flexible Configuration**: Customize log levels, formatting, and more

## 🚀 Quick Start

### Installation

Using `uv` (recommended):
```bash
uv sync
```

Using `pip`:
```bash
pip install -e .
```

### Basic Usage

```python
from rich_reporter import get_reporter

# Create a reporter
reporter = get_reporter("myapp")

# Direct console output with Rich styling
reporter.print("Starting up...", style="bold green")

# Structured logging
reporter.info("Process started")
reporter.warning("Using deprecated flag")
reporter.error("Failed to load config")

# Show summary and get statistics
stats = reporter.report()
```

### Output Example

![Rich Reporter Demo](docs/demo-screenshot.png)

The reporter automatically tracks all log messages and displays a beautiful summary panel:

```
╭─────────── Report Summary ───────────╮
│ Level      Count                     │
│ ─────────────────                    │
│ DEBUG         2                      │
│ INFO          5                      │
│ WARNING       2                      │
│ ERROR         1                      │
│ CRITICAL      0                      │
╰──────────────────────────────────────╯
```

## 📖 Documentation

For detailed documentation, API reference, and examples, see [rich_reporter/README.md](rich_reporter/README.md).

### Key Features

**Context Manager**
```python
with get_reporter("myapp") as reporter:
    reporter.info("Processing...")
    reporter.warning("Warning occurred")
# Report is automatically shown on exit
```

**File Logging**
```python
reporter = get_reporter(
    "myapp",
    enable_file_handler=True,
    file_path="app.log"
)
```

**Custom Configuration**
```python
import logging
from rich_reporter import get_reporter

reporter = get_reporter(
    name="myapp",
    level=logging.DEBUG,
    show_time=True,
    show_path=False
)
```

## 🧪 Development

### Setup Development Environment

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/cdeimling/rich-logger.git
cd rich-logger
uv sync --all-extras
```

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=rich_reporter --cov-report=html

# Run specific test file
uv run pytest tests/test_reporter.py -v
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Format code
uv run ruff format .

# Security check
uv run bandit -r rich_reporter/
```

### Try the Demo

```bash
# Basic demo
python -m rich_reporter

# Demo with context manager example
python -m rich_reporter --with-context
```

## 🎯 Use Cases

- **CLI Applications**: Beautiful output with automatic error tracking
- **Data Pipelines**: Track processing statistics and warnings
- **Automation Scripts**: Professional logging with summary reports
- **Testing & CI/CD**: Structured logging with statistics for analysis
- **Long-running Processes**: Monitor progress with rich console output

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please ensure:
- All tests pass (`pytest`)
- Code is formatted (`ruff format`)
- Linting passes (`ruff check`)
- Security checks pass (`bandit`)

## 🙏 Acknowledgments

Built with [Rich](https://github.com/Textualize/rich) by [Textualize](https://www.textualize.io/)

## 📝 Changelog

### v0.1.0 (Initial Release)
- Core Reporter class with logging and console output
- Automatic statistics collection
- Summary reporting with Rich panels
- Context manager support
- File logging support
- Comprehensive test suite
- CI/CD with GitHub Actions
