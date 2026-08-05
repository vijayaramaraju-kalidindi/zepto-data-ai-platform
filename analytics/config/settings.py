"""
Application settings for the Analytics Pipeline.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================
# Base Directories
# ==========================================

BASE_DIRECTORY = Path(__file__).resolve().parent.parent

OUTPUTS_DIRECTORY = BASE_DIRECTORY / "outputs"

FIGURES_DIRECTORY = OUTPUTS_DIRECTORY / "figures"

METRICS_DIRECTORY = OUTPUTS_DIRECTORY / "metrics"

MODELS_DIRECTORY = BASE_DIRECTORY / "models" / "trained_models"


# ==========================================
# Logging
# ==========================================

LOG_DIRECTORY = OUTPUTS_DIRECTORY / "logs"

LOG_FILE_NAME = "application.log"

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

# ==========================================
# Model Parameters
# ==========================================

TEST_SIZE = float(
    os.getenv(
        "TEST_SIZE",
        0.20,
    )
)

RANDOM_STATE = int(
    os.getenv(
        "RANDOM_STATE",
        42,
    )
)

CROSS_VALIDATION_FOLDS = int(
    os.getenv(
        "CROSS_VALIDATION_FOLDS",
        5,
    )
)

# ==========================================
# Dataset Backup
# ==========================================

DATASET_BACKUP_NAME = "titanic.csv"

DATASET_BACKUP_PATH = (
    OUTPUTS_DIRECTORY
    / DATASET_BACKUP_NAME
)

REPORTS_DIRECTORY = (
    OUTPUTS_DIRECTORY
    / "reports"
)