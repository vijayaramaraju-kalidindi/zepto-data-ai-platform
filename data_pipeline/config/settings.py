"""
Application configuration.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIRECTORY = BASE_DIR / "outputs"

CSV_DIRECTORY = OUTPUTS_DIRECTORY / "csv"

DATABASE_DIRECTORY = OUTPUTS_DIRECTORY / "database"

LOG_DIRECTORY = OUTPUTS_DIRECTORY / "logs"

BASE_URL = os.getenv(
    "BASE_URL",
    "https://books.toscrape.com/",
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "books.db",
)

GBP_TO_INR_RATE = float(
    os.getenv(
        "GBP_TO_INR_RATE",
        "105.50",
    )
)

REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "30",
    )
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)