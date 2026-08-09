"""
Application configuration.

Centralized configuration for the
Support Assistant module.
"""

from __future__ import annotations

import os

from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --------------------------------------------------
# Project Directories
# --------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[2]
)

MODULE_ROOT = (
    PROJECT_ROOT
    / "support_assistant"
)

DOCUMENTS_DIRECTORY = (
    MODULE_ROOT
    / "docs"
)

OUTPUTS_DIRECTORY = (
    MODULE_ROOT
    / "outputs"
)

LOGS_DIRECTORY = (
    OUTPUTS_DIRECTORY
    / "logs"
)

CHROMA_DIRECTORY = (
    MODULE_ROOT
    / "chroma_db"
)

# --------------------------------------------------
# Embedding Configuration
# --------------------------------------------------

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2",
)

# --------------------------------------------------
# Chroma Configuration
# --------------------------------------------------

CHROMA_COLLECTION = os.getenv(
    "CHROMA_COLLECTION",
    "support_assistant",
)

# --------------------------------------------------
# LLM Configuration
# --------------------------------------------------

MOCK_LLM = (
    os.getenv(
        "MOCK_LLM",
        "true",
    ).lower()
    == "true"
)

# --------------------------------------------------
# Runtime
# --------------------------------------------------

RANDOM_STATE = 42
