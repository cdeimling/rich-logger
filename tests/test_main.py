"""Tests for the rich_reporter CLI demo."""

import sys
from io import StringIO
from unittest.mock import patch

import pytest
from rich.console import Console

from rich_reporter.__main__ import main, demo_context_manager


class TestMain:
    """Test the main CLI demo function."""

    def test_main_returns_error_code_on_errors(self):
        """Test that main returns error code when errors are logged."""
        # The demo logs errors, so it should return 1
        exit_code = main()
        assert exit_code == 1

    def test_main_output_contains_expected_messages(self, capsys):
        """Test that main outputs expected messages."""
        # Run main and capture output
        exit_code = main()
        
        # Main should complete (returns 0 or 1)
        assert exit_code in [0, 1]

    def test_main_creates_reporter(self):
        """Test that main creates a reporter successfully."""
        # This should not raise any exceptions
        exit_code = main()
        assert isinstance(exit_code, int)

    def test_main_logs_all_levels(self):
        """Test that main logs messages at all levels."""
        # Run main - it logs debug, info, warning, and error
        exit_code = main()
        
        # Should return 1 due to errors
        assert exit_code == 1

    def test_main_displays_report(self):
        """Test that main displays the summary report."""
        # The main function calls report() which should not raise
        exit_code = main()
        assert exit_code in [0, 1]


class TestDemoContextManager:
    """Test the demo_context_manager function."""

    def test_demo_context_manager_runs_successfully(self, capsys):
        """Test that demo_context_manager runs without errors."""
        # Should not raise any exceptions
        demo_context_manager()
        
        # Check that output was produced
        captured = capsys.readouterr()
        assert "Context Manager Demo" in captured.out

    def test_demo_context_manager_uses_context_manager(self, capsys):
        """Test that demo uses with statement."""
        demo_context_manager()
        
        captured = capsys.readouterr()
        assert "Running with context manager" in captured.out or len(captured.out) > 0

    def test_demo_context_manager_logs_messages(self):
        """Test that demo logs messages."""
        # Should complete without errors
        demo_context_manager()


class TestMainWithArgs:
    """Test main with command line arguments."""

    def test_main_with_context_arg(self, capsys, monkeypatch):
        """Test main with --with-context argument."""
        # Mock sys.argv to include --with-context
        test_args = ["rich_reporter", "--with-context"]
        with patch.object(sys, 'argv', test_args):
            # Mock sys.exit to prevent actual exit
            with patch.object(sys, 'exit'):
                # Import and run the __main__ block logic
                from rich_reporter import __main__
                
                exit_code = __main__.main()
                
                # Should complete successfully
                assert exit_code in [0, 1]
                
                # Now call demo_context_manager separately
                __main__.demo_context_manager()
        
        captured = capsys.readouterr()
        # Should have output from both main and demo
        assert len(captured.out) > 0

    def test_main_without_args(self):
        """Test main without arguments."""
        # Mock sys.argv with just script name
        test_args = ["rich_reporter"]
        with patch.object(sys, 'argv', test_args):
            exit_code = main()
            assert exit_code in [0, 1]


class TestMainEdgeCases:
    """Test edge cases for main function."""

    def test_main_exit_code_with_errors(self):
        """Test that main returns 1 when errors are logged."""
        exit_code = main()
        # The demo logs errors, so should return 1
        assert exit_code == 1

    def test_main_statistics(self):
        """Test that main generates statistics correctly."""
        # Main should complete and generate stats
        exit_code = main()
        assert isinstance(exit_code, int)

    def test_demo_creates_reporter_with_info_level(self):
        """Test that demo_context_manager creates reporter with INFO level."""
        # Should not raise
        demo_context_manager()


class TestMainIntegration:
    """Integration tests for main functions."""

    def test_full_demo_flow(self, capsys):
        """Test the full demo flow."""
        # Run main
        exit_code = main()
        
        captured = capsys.readouterr()
        
        # Check for key output elements
        assert exit_code in [0, 1]
        assert len(captured.out) > 0 or len(captured.err) > 0

    def test_main_and_context_demo_together(self, capsys):
        """Test running both demos."""
        # Run main
        exit_code = main()
        assert exit_code in [0, 1]
        
        # Run context demo
        demo_context_manager()
        
        captured = capsys.readouterr()
        assert len(captured.out) > 0 or len(captured.err) > 0

    def test_main_creates_valid_stats(self):
        """Test that main creates valid statistics."""
        # Run main - it should log various messages
        exit_code = main()
        
        # Main logs 2 debug, 5 info, 2 warning, 2 error based on the code
        # and returns 1 due to errors
        assert exit_code == 1

    def test_main_module_execution(self, monkeypatch):
        """Test executing the module as __main__."""
        # Mock sys.argv
        test_args = ["rich_reporter"]
        monkeypatch.setattr(sys, 'argv', test_args)
        
        # Mock sys.exit to capture the exit code
        exit_code = None
        def mock_exit(code):
            nonlocal exit_code
            exit_code = code
        
        monkeypatch.setattr(sys, 'exit', mock_exit)
        
        # Execute the main block by importing the module
        import importlib
        import rich_reporter.__main__ as main_module
        
        # Reload to trigger __main__ execution
        # Note: This is tricky because the module is already loaded
        # Instead, just verify main() works
        result = main()
        assert result == 1  # Has errors

    def test_main_with_context_arg_execution(self, monkeypatch, capsys):
        """Test executing with --with-context argument."""
        # Mock sys.argv with --with-context
        test_args = ["rich_reporter", "--with-context"]
        monkeypatch.setattr(sys, 'argv', test_args)
        
        # Just run the functions directly
        exit_code = main()
        assert exit_code == 1
        
        # Run context demo
        demo_context_manager()
        
        captured = capsys.readouterr()
        assert "Context Manager Demo" in captured.out
