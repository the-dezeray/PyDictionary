#!/usr/bin/env python3
"""
Test script to verify logging functionality in the RichWord project.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from richword.util.logger import get_logger, setup_logger

def test_logging():
    """Test the logging functionality"""
    
    # Set up the main logger
    main_logger = setup_logger("richword_test", level=10)  # DEBUG level
    
    # Get module-specific loggers
    test_logger = get_logger("test_module")
    another_logger = get_logger("another_module")
    
    # Test different log levels
    print("Testing logging functionality...")
    print("Check the logs/ directory for log files.")
    
    main_logger.debug("This is a debug message from main logger")
    main_logger.info("This is an info message from main logger")
    main_logger.warning("This is a warning message from main logger")
    main_logger.error("This is an error message from main logger")
    
    test_logger.info("This is an info message from test module")
    test_logger.debug("This is a debug message from test module")
    
    another_logger.warning("This is a warning from another module")
    
    # Test logging with exception info
    try:
        raise ValueError("This is a test exception")
    except Exception as e:
        test_logger.error("Caught an exception:", exc_info=True)
    
    print("Logging test completed. Check the console output and log files.")
    print("Log files should be created in the 'logs/' directory:")
    print("- richword.log (INFO and above)")
    print("- richword_debug.log (DEBUG and above)")

if __name__ == "__main__":
    test_logging()