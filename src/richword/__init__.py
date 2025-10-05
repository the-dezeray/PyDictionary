"""PyDictionary - A feature-rich terminal dictionary application."""

# Initialize logging when package is imported
from .util.logger import setup_logger
from .main import main

__version__ = "0.1.0"
__author__ = "the-dezeray"
__email__ = "your.email@example.com"

# Set up the main logger for the application
logger = setup_logger("richword")

__all__ = ["main", "logger"]