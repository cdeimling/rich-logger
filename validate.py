#!/usr/bin/env python3
"""Simple validation script to test rich_reporter functionality."""

import logging
import tempfile
from pathlib import Path
from io import StringIO
from rich.console import Console

from rich_reporter import get_reporter, Reporter


def test_basic_functionality():
    """Test basic reporter functionality."""
    print("Testing basic functionality...")
    
    # Test 1: Basic reporter creation
    reporter = get_reporter("test")
    assert reporter.name == "test", "Reporter name should be 'test'"
    print("✓ Reporter creation works")
    
    # Test 2: Logging increments statistics
    reporter.info("Test info")
    reporter.warning("Test warning")
    reporter.error("Test error")
    stats = reporter.get_stats()
    assert stats["info"] == 1, f"Expected 1 info, got {stats['info']}"
    assert stats["warning"] == 1, f"Expected 1 warning, got {stats['warning']}"
    assert stats["error"] == 1, f"Expected 1 error, got {stats['error']}"
    print("✓ Statistics counting works")
    
    # Test 3: Print method works
    output = StringIO()
    console = Console(file=output, width=80)
    reporter2 = get_reporter("test2", console=console)
    reporter2.print("Hello World")
    assert "Hello World" in output.getvalue(), "Print should output to console"
    print("✓ Console print works")
    
    # Test 4: Report displays and returns stats
    output2 = StringIO()
    console2 = Console(file=output2, width=80)
    reporter3 = get_reporter("test3", console=console2)
    reporter3.info("Test")
    reported_stats = reporter3.report()
    assert reported_stats["info"] == 1, "Report should return stats"
    assert "Report Summary" in output2.getvalue(), "Report should display panel"
    print("✓ Report functionality works")
    
    # Test 5: Context manager
    output3 = StringIO()
    console3 = Console(file=output3, width=80)
    with get_reporter("test4", console=console3) as reporter:
        reporter.info("Context test")
    output_text = output3.getvalue()
    assert "Report Summary" in output_text, "Context manager should auto-report"
    print("✓ Context manager works")
    
    # Test 6: File handler
    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
        tmp_path = tmp.name
    
    try:
        reporter4 = get_reporter(
            "test5",
            enable_file_handler=True,
            file_path=tmp_path
        )
        reporter4.info("File test")
        log_content = Path(tmp_path).read_text()
        assert "File test" in log_content, "Should write to log file"
        print("✓ File handler works")
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    
    # Test 7: Log level filtering
    reporter5 = get_reporter("test6", level=logging.WARNING)
    reporter5.debug("Debug message")
    reporter5.info("Info message")
    reporter5.warning("Warning message")
    stats5 = reporter5.get_stats()
    assert stats5["debug"] == 0, "Debug should be filtered"
    assert stats5["info"] == 0, "Info should be filtered"
    assert stats5["warning"] == 1, "Warning should be counted"
    print("✓ Log level filtering works")
    
    # Test 8: Multiple log messages
    reporter6 = get_reporter("test7")
    for i in range(5):
        reporter6.info(f"Message {i}")
    assert reporter6.get_stats()["info"] == 5, "Should count all messages"
    print("✓ Multiple messages counting works")
    
    print("\n✅ All tests passed!")
    return True


def test_error_cases():
    """Test error handling."""
    print("\nTesting error handling...")
    
    # Test: File handler without path should raise error
    try:
        get_reporter("test", enable_file_handler=True)
        print("✗ Should have raised ValueError")
        return False
    except ValueError as e:
        if "file_path must be provided" in str(e):
            print("✓ File handler validation works")
        else:
            print(f"✗ Wrong error message: {e}")
            return False
    
    print("✅ Error handling tests passed!")
    return True


def test_direct_instantiation():
    """Test direct Reporter class instantiation."""
    print("\nTesting direct instantiation...")
    
    reporter = Reporter("direct_test")
    assert reporter.name == "direct_test"
    reporter.info("Direct test")
    assert reporter.get_stats()["info"] == 1
    
    print("✓ Direct instantiation works")
    print("✅ Direct instantiation tests passed!")
    return True


if __name__ == "__main__":
    try:
        test_basic_functionality()
        test_error_cases()
        test_direct_instantiation()
        print("\n" + "="*60)
        print("🎉 All validation tests completed successfully!")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
