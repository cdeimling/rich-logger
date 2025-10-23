"""Tests for the rich_reporter core functionality."""

import logging
from io import StringIO
from pathlib import Path
import tempfile

import pytest
from rich.console import Console

from rich_reporter import Reporter, get_reporter


class TestReporterInitialization:
    """Test Reporter initialization and configuration."""
    
    def test_reporter_creation(self):
        """Test basic reporter creation."""
        reporter = get_reporter("test")
        assert reporter.name == "test"
        assert reporter.console is not None
        assert reporter.logger is not None
    
    def test_reporter_with_custom_level(self):
        """Test reporter with custom log level."""
        reporter = get_reporter("test", level=logging.DEBUG)
        assert reporter.logger.level == logging.DEBUG
    
    def test_reporter_with_custom_console(self):
        """Test reporter with custom console."""
        custom_console = Console()
        reporter = get_reporter("test", console=custom_console)
        assert reporter.console is custom_console
    
    def test_reporter_file_handler_requires_path(self):
        """Test that file handler requires a file path."""
        with pytest.raises(ValueError, match="file_path must be provided"):
            get_reporter("test", enable_file_handler=True)
    
    def test_reporter_with_file_handler(self):
        """Test reporter with file handler."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
            tmp_path = tmp.name
        
        try:
            reporter = get_reporter(
                "test",
                enable_file_handler=True,
                file_path=tmp_path
            )
            reporter.info("Test message")
            
            # Verify log file was created and contains message
            log_content = Path(tmp_path).read_text()
            assert "Test message" in log_content
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestReporterLogging:
    """Test Reporter logging functionality."""
    
    def test_debug_logging(self):
        """Test debug level logging."""
        reporter = get_reporter("test", level=logging.DEBUG)
        reporter.debug("Debug message")
        assert reporter.get_stats()["debug"] == 1
    
    def test_info_logging(self):
        """Test info level logging."""
        reporter = get_reporter("test")
        reporter.info("Info message")
        assert reporter.get_stats()["info"] == 1
    
    def test_warning_logging(self):
        """Test warning level logging."""
        reporter = get_reporter("test")
        reporter.warning("Warning message")
        assert reporter.get_stats()["warning"] == 1
    
    def test_error_logging(self):
        """Test error level logging."""
        reporter = get_reporter("test")
        reporter.error("Error message")
        assert reporter.get_stats()["error"] == 1
    
    def test_critical_logging(self):
        """Test critical level logging."""
        reporter = get_reporter("test")
        reporter.critical("Critical message")
        assert reporter.get_stats()["critical"] == 1
    
    def test_exception_logging(self):
        """Test exception logging."""
        reporter = get_reporter("test")
        try:
            raise ValueError("Test exception")
        except ValueError:
            reporter.exception("Exception occurred")
        
        # Exception uses error level
        assert reporter.get_stats()["error"] == 1
    
    def test_multiple_log_messages(self):
        """Test multiple log messages update statistics correctly."""
        reporter = get_reporter("test", level=logging.DEBUG)
        
        reporter.debug("Debug 1")
        reporter.debug("Debug 2")
        reporter.info("Info 1")
        reporter.info("Info 2")
        reporter.info("Info 3")
        reporter.warning("Warning 1")
        reporter.error("Error 1")
        reporter.error("Error 2")
        
        stats = reporter.get_stats()
        assert stats["debug"] == 2
        assert stats["info"] == 3
        assert stats["warning"] == 1
        assert stats["error"] == 2
        assert stats["critical"] == 0
    
    def test_log_level_filtering(self):
        """Test that log level filtering works correctly."""
        reporter = get_reporter("test", level=logging.WARNING)
        
        reporter.debug("Debug message")
        reporter.info("Info message")
        reporter.warning("Warning message")
        reporter.error("Error message")
        
        stats = reporter.get_stats()
        # Debug and info should not be counted due to level filtering
        assert stats["debug"] == 0
        assert stats["info"] == 0
        assert stats["warning"] == 1
        assert stats["error"] == 1


class TestReporterConsole:
    """Test Reporter console output functionality."""
    
    def test_print_method(self):
        """Test that print method forwards to console."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("test", console=console)
        
        reporter.print("Test message")
        
        output_text = output.getvalue()
        assert "Test message" in output_text
    
    def test_print_with_styling(self):
        """Test print with Rich styling."""
        output = StringIO()
        console = Console(file=output, width=80, legacy_windows=False)
        reporter = get_reporter("test", console=console)
        
        reporter.print("[bold red]Styled message[/bold red]")
        
        output_text = output.getvalue()
        assert "Styled message" in output_text


class TestReporterStatistics:
    """Test Reporter statistics functionality."""
    
    def test_get_stats_returns_copy(self):
        """Test that get_stats returns a copy of statistics."""
        reporter = get_reporter("test")
        reporter.info("Test")
        
        stats1 = reporter.get_stats()
        stats1["info"] = 999  # Modify the returned dict
        
        stats2 = reporter.get_stats()
        assert stats2["info"] == 1  # Original stats unchanged
    
    def test_initial_stats_are_zero(self):
        """Test that initial statistics are all zero."""
        reporter = get_reporter("test")
        stats = reporter.get_stats()
        
        assert stats["debug"] == 0
        assert stats["info"] == 0
        assert stats["warning"] == 0
        assert stats["error"] == 0
        assert stats["critical"] == 0
    
    def test_report_returns_stats(self):
        """Test that report() returns current statistics."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("test", console=console)
        
        reporter.info("Test 1")
        reporter.warning("Test 2")
        reporter.error("Test 3")
        
        stats = reporter.report()
        
        assert stats["info"] == 1
        assert stats["warning"] == 1
        assert stats["error"] == 1
    
    def test_report_displays_panel(self):
        """Test that report() displays a summary panel."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("test", console=console)
        
        reporter.info("Test")
        reporter.report(title="Test Summary")
        
        output_text = output.getvalue()
        assert "Test Summary" in output_text
        assert "INFO" in output_text
    
    def test_report_custom_title(self):
        """Test report with custom title."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("test", console=console)
        
        reporter.info("Test")
        reporter.report(title="Custom Title")
        
        output_text = output.getvalue()
        assert "Custom Title" in output_text


class TestReporterContextManager:
    """Test Reporter context manager functionality."""
    
    def test_context_manager_entry(self):
        """Test context manager entry returns reporter."""
        reporter = get_reporter("test")
        with reporter as ctx_reporter:
            assert ctx_reporter is reporter
    
    def test_context_manager_auto_report(self):
        """Test context manager automatically calls report."""
        output = StringIO()
        console = Console(file=output, width=80)
        
        with get_reporter("test", console=console) as reporter:
            reporter.info("Test message")
        
        output_text = output.getvalue()
        # Check that report was called (summary panel shown)
        assert "Report Summary" in output_text
    
    def test_context_manager_with_exception(self):
        """Test context manager handles exceptions gracefully."""
        output = StringIO()
        console = Console(file=output, width=80)
        
        try:
            with get_reporter("test", console=console) as reporter:
                reporter.info("Before exception")
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        output_text = output.getvalue()
        # Report should still be called even after exception
        assert "Report Summary" in output_text


class TestReporterDirectInstantiation:
    """Test direct Reporter class instantiation."""
    
    def test_direct_instantiation(self):
        """Test creating Reporter directly."""
        reporter = Reporter("test")
        assert reporter.name == "test"
        assert isinstance(reporter, Reporter)
    
    def test_direct_instantiation_with_params(self):
        """Test creating Reporter directly with parameters."""
        console = Console()
        reporter = Reporter(
            name="test",
            level=logging.DEBUG,
            console=console,
            show_time=False,
            show_path=True
        )
        assert reporter.name == "test"
        assert reporter.console is console
        assert reporter.logger.level == logging.DEBUG
