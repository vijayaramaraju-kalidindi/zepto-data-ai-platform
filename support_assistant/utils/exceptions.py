"""
Custom exceptions.

Defines project-specific exceptions
used throughout the Support Assistant
module.
"""

from __future__ import annotations


class SupportAssistantError(Exception):
    """
    Base exception for the Support
    Assistant module.
    """

    pass


class DocumentLoadingError(
    SupportAssistantError,
):
    """
    Raised when document loading
    fails.
    """

    pass

class EmbeddingGenerationError(
    SupportAssistantError,
):
    """
    Raised when embedding generation
    fails.
    """

    pass


class VectorStoreError(
    SupportAssistantError,
):
    """
    Raised when interacting with the
    Chroma vector database fails.
    """

    pass


class RetrievalError(
    SupportAssistantError,
):
    """
    Raised when document retrieval
    fails.
    """

    pass


class PromptGenerationError(
    SupportAssistantError,
):
    """
    Raised when prompt construction
    fails.
    """

    pass


class LLMServiceError(
    SupportAssistantError,
):
    """
    Raised when the language model
    cannot generate a response.
    """

    pass


class GraphExecutionError(
    SupportAssistantError,
):
    """
    Raised when LangGraph workflow
    execution fails.
    """

    pass


class ValidationError(
    SupportAssistantError,
):
    """
    Raised when request or response
    validation fails.
    """

    pass
