# rich_reporter

**Unified Rich-based Logging & Reporting Utility**

A lightweight Python package that combines Rich Console functionality with structured logging and automatic statistics collection.

## Features

- 🎨 **Beautiful Console Output**: Built on Rich for gorgeous terminal output
- 📊 **Automatic Statistics**: Tracks log counts at all levels (debug, info, warning, error, critical)
- 🔧 **Zero Boilerplate**: Get a fully configured logger and console in one call
- 📋 **Summary Reports**: Generate beautiful summary panels at the end of your process
- 🎯 **Context Manager Support**: Automatic reporting when using `with` statements
- 📁 **File Logging**: Optional file handler support
- 🔌 **Flexible Configuration**: Customize log levels, formatting, and more

## Installation

Using `uv`:
```bash
uv sync
```

Using `pip`:
```bash
pip install -e .
```

## Quick Start

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

### Context Manager

```python
from rich_reporter import get_reporter

with get_reporter("myapp") as reporter:
    reporter.info("Processing data...")
    reporter.warning("Cache miss")
    reporter.info("Processing complete")
# report() is called automatically on exit
```

### Advanced Configuration

```python
import logging
from rich_reporter import get_reporter

reporter = get_reporter(
    name="myapp",
    level=logging.DEBUG,  # Set log level
    show_time=True,       # Show timestamps
    show_path=False,      # Hide file paths
    enable_file_handler=True,  # Enable file logging
    file_path="app.log"   # Log file path
)

reporter.debug("Detailed diagnostic info")
reporter.info("Normal operation")
```

## API Reference

### `get_reporter(name, **kwargs)`

Creates and returns a configured Reporter instance.

**Parameters:**
- `name` (str): Name for the logger and reporter
- `level` (int): Logging level (default: `logging.INFO`)
- `console` (Console, optional): Rich Console instance (creates new if None)
- `show_time` (bool): Show timestamps in log messages (default: True)
- `show_path` (bool): Show file path in log messages (default: False)
- `enable_file_handler` (bool): Enable file logging (default: False)
- `file_path` (str, optional): Path for log file (required if `enable_file_handler=True`)

**Returns:** `Reporter` instance

### Reporter Methods

#### Console Output
- `print(*args, **kwargs)`: Print using Rich Console with full styling support

#### Logging Methods
- `debug(message, *args, **kwargs)`: Log debug message
- `info(message, *args, **kwargs)`: Log info message
- `warning(message, *args, **kwargs)`: Log warning message
- `error(message, *args, **kwargs)`: Log error message
- `critical(message, *args, **kwargs)`: Log critical message
- `exception(message, *args, **kwargs)`: Log exception with traceback

#### Statistics & Reporting
- `get_stats()`: Returns dict with log counts for each level
- `report(title="Report Summary")`: Display summary panel and return statistics

#### Context Manager
- `__enter__()`: Returns self
- `__exit__()`: Automatically calls `report()`

## CLI Demo

Run the included demo to see rich_reporter in action:

```bash
# Basic demo
python -m rich_reporter

# Demo with context manager example
python -m rich_reporter --with-context
```

## Examples

### Simple Script

```python
from rich_reporter import get_reporter

reporter = get_reporter("backup")

reporter.print("[bold blue]Starting backup process...[/bold blue]")
reporter.info("Connecting to database")
reporter.info("Backing up 1000 records")
reporter.warning("Skipped 5 corrupted records")
reporter.error("Failed to backup user preferences")
reporter.info("Backup completed")

stats = reporter.report(title="Backup Summary")

if stats["error"] > 0:
    exit(1)
```

### Data Processing Pipeline

```python
from rich_reporter import get_reporter
import logging

reporter = get_reporter("pipeline", level=logging.DEBUG)

reporter.print("[bold]Data Processing Pipeline[/bold]\n")

for i in range(5):
    reporter.info(f"Processing batch {i+1}/5")
    if i == 3:
        reporter.warning(f"Batch {i+1} took longer than expected")

reporter.print("\n[green]All batches processed![/green]\n")
reporter.report(title="Pipeline Statistics")
```

### Error Handling

```python
from rich_reporter import get_reporter

reporter = get_reporter("app")

try:
    # Your code here
    reporter.info("Starting operation")
    raise ValueError("Something went wrong")
except Exception as e:
    reporter.exception("Operation failed")
finally:
    reporter.report()
```

## Use Cases

- **CLI Applications**: Beautiful output with automatic error tracking
- **Data Pipelines**: Track processing statistics and warnings
- **Automation Scripts**: Professional logging with summary reports
- **Testing & CI/CD**: Structured logging with statistics for analysis
- **Long-running Processes**: Monitor progress with rich console output

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please ensure all tests pass and code meets the project's style guidelines (ruff, bandit).

## Development

### Setup Development Environment

```bash
uv sync --all-extras
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=rich_reporter --cov-report=html
```

### Linting

```bash
ruff check .
```

### Security Checks

```bash
bandit -r rich_reporter/
```
