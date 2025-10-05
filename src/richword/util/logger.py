# logger.py
import logging
import os
from pathlib import Path

def setup_logger(name: str = "richword", level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Console handler with colored output for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler for persistent logging
    file_handler = logging.FileHandler(log_dir / "richword.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Debug file handler for detailed debugging
    debug_handler = logging.FileHandler(log_dir / "richword_debug.log", encoding='utf-8')
    debug_handler.setLevel(logging.DEBUG)
    
    # Create formatters
    console_formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(message)s"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s"
    )
    
    # Set formatters
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    debug_handler.setFormatter(detailed_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(debug_handler)
    
    return logger

def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        module_name: Name of the module requesting the logger
    
    Returns:
        Logger instance for the module
    """
    return logging.getLogger(f"richword.{module_name}")

# Initialize the main logger
main_logger = setup_logger()

# Export commonly used loggers
__all__ = ["setup_logger", "get_logger", "main_logger"]
