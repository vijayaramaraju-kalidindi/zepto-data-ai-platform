"""
Custom exceptions used throughout the project.
"""


class ScrapingError(Exception):
    """Raised when scraping fails."""


class ParsingError(Exception):
    """Raised when parsing HTML fails."""


class ValidationError(Exception):
    """Raised when validation fails."""


class DatabaseError(Exception):
    """Raised for SQLite database errors."""