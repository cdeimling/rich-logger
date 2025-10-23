"""rich_reporter - Unified Rich-based Logging & Reporting Utility

This package provides a lightweight, unified Rich-based logging and reporting utility
that enables developers to obtain a fully configured Rich Console and logger in a single call.
"""

import logging
from typing import Any, Optional, Dict
from contextlib import contextmanager

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table


class Reporter:
    """Unified Rich-based logging and reporting utility.
    
    Combines Rich Console functionality with structured logging while automatically
    gathering log statistics.
    
    Attributes:
        console: Rich Console instance for direct output
        logger: Configured logger with RichHandler
        name: Reporter name
    """
    
    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        console: Optional[Console] = None,
        show_time: bool = True,
        show_path: bool = False,
        enable_file_handler: bool = False,
        file_path: Optional[str] = None,
    ):
        """Initialize a new Reporter instance.
        
        Args:
            name: Name for the logger and reporter
            level: Logging level (default: INFO)
            console: Optional Rich Console instance (creates new if None)
            show_time: Show timestamps in log messages
            show_path: Show file path in log messages
            enable_file_handler: Enable file logging
            file_path: Path for log file (required if enable_file_handler=True)
        """
        self.name = name
        self.console = console or Console()
        
        # Initialize statistics counters
        self._stats: Dict[str, int] = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
        }
        
        # Configure logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Remove any existing handlers
        self.logger.handlers.clear()
        
        # Add RichHandler
        rich_handler = RichHandler(
            console=self.console,
            show_time=show_time,
            show_path=show_path,
            rich_tracebacks=True,
        )
        rich_handler.setLevel(level)
        formatter = logging.Formatter("%(message)s")
        rich_handler.setFormatter(formatter)
        self.logger.addHandler(rich_handler)
        
        # Add file handler if requested
        if enable_file_handler:
            if not file_path:
                raise ValueError("file_path must be provided when enable_file_handler=True")
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Create custom filter to count log events
        self.logger.addFilter(self._count_log_event)
    
    def _count_log_event(self, record: logging.LogRecord) -> bool:
        """Filter that counts log events by level."""
        level_name = record.levelname.lower()
        if level_name in self._stats:
            self._stats[level_name] += 1
        return True
    
    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print output using Rich Console.
        
        Args:
            *args: Positional arguments passed to console.print()
            **kwargs: Keyword arguments passed to console.print()
        """
        self.console.print(*args, **kwargs)
    
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message.
        
        Args:
            message: Debug message
            *args: Positional arguments for string formatting
            **kwargs: Keyword arguments passed to logger.debug()
        """
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message.
        
        Args:
            message: Info message
            *args: Positional arguments for string formatting
            **kwargs: Keyword arguments passed to logger.info()
        """
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message.
        
        Args:
            message: Warning message
            *args: Positional arguments for string formatting
            **kwargs: Keyword arguments passed to logger.warning()
        """
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message.
        
        Args:
            message: Error message
            *args: Positional arguments for string formatting
            **kwargs: Keyword arguments passed to logger.error()
        """
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message.
        
        Args:
            message: Critical message
            *args: Positional arguments for string formatting
            **kwargs: Keyword arguments passed to logger.critical()
        """
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an exception message with traceback.
        
        Args:
            message: Exception message
            *args: Positional arguments for string formatting
            **kwargs: Keyword arguments passed to logger.exception()
        """
        self.logger.exception(message, *args, **kwargs)
    
    def get_stats(self) -> Dict[str, int]:
        """Get current log statistics.
        
        Returns:
            Dictionary with counts for each log level
        """
        return self._stats.copy()
    
    def report(self, title: str = "Report Summary") -> Dict[str, int]:
        """Display a summary panel and return statistics.
        
        Args:
            title: Title for the summary panel
            
        Returns:
            Dictionary with log statistics
        """
        # Create table for statistics
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Level", style="cyan", width=12)
        table.add_column("Count", justify="right", style="green")
        
        for level, count in self._stats.items():
            level_display = level.upper()
            # Add styling based on level
            if level == "error" or level == "critical":
                count_style = "bold red"
            elif level == "warning":
                count_style = "bold yellow"
            else:
                count_style = "green"
            
            table.add_row(level_display, f"[{count_style}]{count}[/{count_style}]")
        
        # Display panel
        panel = Panel(
            table,
            title=f"[bold blue]{title}[/bold blue]",
            border_style="blue",
        )
        self.console.print(panel)
        
        return self.get_stats()
    
    def __enter__(self) -> "Reporter":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - automatically show report."""
        self.report()


def get_reporter(
    name: str,
    level: int = logging.INFO,
    console: Optional[Console] = None,
    show_time: bool = True,
    show_path: bool = False,
    enable_file_handler: bool = False,
    file_path: Optional[str] = None,
) -> Reporter:
    """Get a configured Reporter instance.
    
    Args:
        name: Name for the logger and reporter
        level: Logging level (default: INFO)
        console: Optional Rich Console instance (creates new if None)
        show_time: Show timestamps in log messages
        show_path: Show file path in log messages
        enable_file_handler: Enable file logging
        file_path: Path for log file (required if enable_file_handler=True)
        
    Returns:
        Configured Reporter instance
    """
    return Reporter(
        name=name,
        level=level,
        console=console,
        show_time=show_time,
        show_path=show_path,
        enable_file_handler=enable_file_handler,
        file_path=file_path,
    )


__all__ = ["Reporter", "get_reporter"]
