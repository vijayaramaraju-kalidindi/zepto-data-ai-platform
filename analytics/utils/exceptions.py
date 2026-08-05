"""
Custom exceptions for Analytics module.
"""


class AnalyticsError(
    Exception,
):
    """
    Base Analytics exception.
    """


class DatasetError(
    AnalyticsError,
):
    """
    Raised when dataset operations fail.
    """


class ModelTrainingError(
    AnalyticsError,
):
    """
    Raised when model training fails.
    """