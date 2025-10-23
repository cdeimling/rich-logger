"""Integration tests for rich_reporter."""

import logging
import sys
import tempfile
from io import StringIO
from pathlib import Path

import pytest
from rich.console import Console

from rich_reporter import get_reporter


class TestIntegrationScenarios:
    """Test real-world usage scenarios."""
    
    def test_typical_application_flow(self):
        """Test a typical application flow with logging and reporting."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("app", console=console, level=logging.DEBUG)
        
        # Simulate application flow
        reporter.print("[bold blue]Application Starting[/bold blue]")
        reporter.debug("Loading configuration")
        reporter.info("Configuration loaded successfully")
        reporter.info("Connecting to database")
        reporter.warning("Using default timeout value")
        reporter.info("Database connected")
        reporter.error("Failed to load optional plugin")
        reporter.info("Application ready")
        
        stats = reporter.report(title="Application Startup")
        
        # Verify statistics
        assert stats["debug"] == 1
        assert stats["info"] == 4
        assert stats["warning"] == 1
        assert stats["error"] == 1
        
        # Verify output contains key elements
        output_text = output.getvalue()
        assert "Application Starting" in output_text
        assert "Application Startup" in output_text
    
    def test_data_processing_pipeline(self):
        """Test a data processing pipeline scenario."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("pipeline", console=console)
        
        total_records = 100
        processed = 0
        errors = 0
        
        reporter.print("[bold]Data Processing Pipeline[/bold]")
        reporter.info(f"Processing {total_records} records")
        
        # Simulate processing
        for i in range(10):
            batch_size = 10
            processed += batch_size
            
            if i == 5:
                reporter.warning(f"Slow batch detected: batch {i+1}")
            
            if i == 8:
                reporter.error(f"Failed to process 2 records in batch {i+1}")
                errors += 2
                processed -= 2
        
        reporter.info(f"Processed {processed} records successfully")
        reporter.info(f"Failed to process {errors} records")
        
        stats = reporter.report(title="Pipeline Summary")
        
        assert stats["info"] >= 2
        assert stats["warning"] == 1
        assert stats["error"] == 1
    
    def test_error_handling_scenario(self):
        """Test error handling with exception logging."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("error_test", console=console)
        
        reporter.info("Starting operation")
        
        try:
            reporter.info("Step 1: Validation")
            reporter.info("Step 2: Processing")
            raise ValueError("Simulated error in step 3")
        except ValueError as e:
            reporter.exception("Operation failed")
        
        stats = reporter.report()
        
        assert stats["info"] == 3
        assert stats["error"] == 1
    
    def test_context_manager_workflow(self):
        """Test complete workflow using context manager."""
        output = StringIO()
        console = Console(file=output, width=80)
        
        with get_reporter("workflow", console=console) as reporter:
            reporter.print("[bold]Starting workflow[/bold]")
            reporter.info("Task 1 completed")
            reporter.info("Task 2 completed")
            reporter.warning("Task 3 completed with warnings")
        
        output_text = output.getvalue()
        assert "Starting workflow" in output_text
        assert "Report Summary" in output_text
        assert "INFO" in output_text
        assert "WARNING" in output_text


class TestFileLogging:
    """Test file logging integration."""
    
    def test_file_and_console_logging(self):
        """Test simultaneous file and console logging."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log", mode="w") as tmp:
            tmp_path = tmp.name
        
        try:
            output = StringIO()
            console = Console(file=output, width=80)
            
            reporter = get_reporter(
                "filetest",
                console=console,
                enable_file_handler=True,
                file_path=tmp_path
            )
            
            reporter.info("Test message 1")
            reporter.warning("Test warning")
            reporter.error("Test error")
            
            # Verify console output
            console_output = output.getvalue()
            assert "Test message 1" in console_output
            
            # Verify file output
            file_content = Path(tmp_path).read_text()
            assert "Test message 1" in file_content
            assert "Test warning" in file_content
            assert "Test error" in file_content
            
            # Verify file has timestamps and log levels
            assert "INFO" in file_content
            assert "WARNING" in file_content
            assert "ERROR" in file_content
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestMultipleReporters:
    """Test using multiple reporters simultaneously."""
    
    def test_multiple_independent_reporters(self):
        """Test that multiple reporters maintain independent statistics."""
        reporter1 = get_reporter("app1", level=logging.INFO)
        reporter2 = get_reporter("app2", level=logging.INFO)
        
        reporter1.info("App1 message 1")
        reporter1.info("App1 message 2")
        reporter1.error("App1 error")
        
        reporter2.info("App2 message")
        reporter2.warning("App2 warning")
        
        stats1 = reporter1.get_stats()
        stats2 = reporter2.get_stats()
        
        assert stats1["info"] == 2
        assert stats1["error"] == 1
        assert stats1["warning"] == 0
        
        assert stats2["info"] == 1
        assert stats2["warning"] == 1
        assert stats2["error"] == 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_reporter(self):
        """Test reporter with no log messages."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("empty", console=console)
        
        stats = reporter.report()
        
        assert all(count == 0 for count in stats.values())
        output_text = output.getvalue()
        assert "Report Summary" in output_text
    
    def test_very_long_message(self):
        """Test logging very long messages."""
        reporter = get_reporter("longmsg")
        long_message = "x" * 10000
        
        reporter.info(long_message)
        
        stats = reporter.get_stats()
        assert stats["info"] == 1
    
    def test_special_characters_in_messages(self):
        """Test messages with special characters."""
        output = StringIO()
        console = Console(file=output, width=80)
        reporter = get_reporter("special", console=console)
        
        reporter.info("Message with emoji: 🎉 ✨")
        reporter.warning("Message with unicode: café résumé")
        reporter.error("Message with symbols: <>&\"'")
        
        stats = reporter.get_stats()
        assert stats["info"] == 1
        assert stats["warning"] == 1
        assert stats["error"] == 1
    
    def test_rapid_logging(self):
        """Test rapid successive logging calls."""
        reporter = get_reporter("rapid")
        
        for i in range(1000):
            reporter.info(f"Message {i}")
        
        stats = reporter.get_stats()
        assert stats["info"] == 1000
    
    def test_mixed_log_levels(self):
        """Test mixed log levels in various orders."""
        reporter = get_reporter("mixed", level=logging.DEBUG)
        
        reporter.critical("Critical 1")
        reporter.debug("Debug 1")
        reporter.error("Error 1")
        reporter.info("Info 1")
        reporter.warning("Warning 1")
        reporter.debug("Debug 2")
        reporter.critical("Critical 2")
        
        stats = reporter.get_stats()
        assert stats["debug"] == 2
        assert stats["info"] == 1
        assert stats["warning"] == 1
        assert stats["error"] == 1
        assert stats["critical"] == 2


class TestLoggerFormatting:
    """Test logger formatting options."""
    
    def test_show_time_option(self):
        """Test show_time parameter."""
        output = StringIO()
        console = Console(file=output, width=120)
        
        reporter1 = get_reporter("with_time", console=console, show_time=True)
        reporter1.info("Message with time")
        
        output2 = StringIO()
        console2 = Console(file=output2, width=120)
        reporter2 = get_reporter("without_time", console=console2, show_time=False)
        reporter2.info("Message without time")
        
        # Both should work without errors
        assert reporter1.get_stats()["info"] == 1
        assert reporter2.get_stats()["info"] == 1
    
    def test_show_path_option(self):
        """Test show_path parameter."""
        reporter1 = get_reporter("with_path", show_path=True)
        reporter1.info("Message with path")
        
        reporter2 = get_reporter("without_path", show_path=False)
        reporter2.info("Message without path")
        
        # Both should work without errors
        assert reporter1.get_stats()["info"] == 1
        assert reporter2.get_stats()["info"] == 1
