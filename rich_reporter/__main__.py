"""CLI demo for rich_reporter.

Demonstrates the capabilities of the rich_reporter package including:
- Direct console output with styling
- Structured logging at various levels
- Automatic statistics collection
- Summary reporting
"""

import logging
import sys
from rich_reporter import get_reporter


def main() -> int:
    """Run the CLI demo."""
    # Create reporter with debug level to show all messages
    reporter = get_reporter("demo", level=logging.DEBUG)
    
    # Header
    reporter.print("\n[bold blue]═══════════════════════════════════════════════════════[/bold blue]")
    reporter.print("[bold blue]   Rich Reporter Demo - Logging & Reporting Utility   [/bold blue]")
    reporter.print("[bold blue]═══════════════════════════════════════════════════════[/bold blue]\n")
    
    # Direct console output with styling
    reporter.print("[bold green]✓[/bold green] Starting demo application...", style="dim")
    
    # Various log levels
    reporter.debug("Debug message: Detailed diagnostic information")
    reporter.info("Info message: Application started successfully")
    reporter.warning("Warning message: Using deprecated configuration option")
    reporter.info("Info message: Processing batch 1 of 3")
    reporter.info("Info message: Processing batch 2 of 3")
    reporter.warning("Warning message: Retrying failed connection")
    reporter.error("Error message: Failed to connect to external service")
    reporter.info("Info message: Processing batch 3 of 3")
    
    # More console output
    reporter.print("\n[yellow]⚠[/yellow]  Some operations completed with warnings", style="dim")
    reporter.print("[red]✗[/red] Some operations failed\n", style="dim")
    
    # Additional logs for statistics
    reporter.debug("Debug message: Cache hit ratio: 85%")
    reporter.info("Info message: All batches processed")
    reporter.error("Error message: 2 items could not be processed")
    
    # Final console message
    reporter.print("[bold]Generating summary report...[/bold]\n")
    
    # Display summary report
    stats = reporter.report(title="Demo Run Summary")
    
    # Exit with appropriate code
    if stats["error"] > 0 or stats["critical"] > 0:
        reporter.print("\n[red]Demo completed with errors[/red]")
        return 1
    elif stats["warning"] > 0:
        reporter.print("\n[yellow]Demo completed with warnings[/yellow]")
        return 0
    else:
        reporter.print("\n[green]Demo completed successfully[/green]")
        return 0


def demo_context_manager() -> None:
    """Demonstrate context manager usage."""
    print("\n" + "="*60)
    print("Context Manager Demo")
    print("="*60 + "\n")
    
    with get_reporter("context_demo", level=logging.INFO) as reporter:
        reporter.print("[bold]Running with context manager...[/bold]")
        reporter.info("Context manager automatically calls report() on exit")
        reporter.warning("This is a test warning")
        reporter.info("Operation completed")
    # report() is automatically called here
    
    print("\n[Context manager demo completed]\n")


if __name__ == "__main__":
    exit_code = main()
    
    # Optionally show context manager demo
    if len(sys.argv) > 1 and sys.argv[1] == "--with-context":
        demo_context_manager()
    
    sys.exit(exit_code)
