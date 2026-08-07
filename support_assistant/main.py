"""
Support Assistant.

Application entry point.
"""

from __future__ import annotations

from config.logging_config import (
    get_logger,
)

from services.ingestion_service import (
    IngestionService,
)

logger = get_logger(__name__)


def main() -> None:
    """
    Execute the Support Assistant
    document ingestion pipeline.
    """

    logger.info(
        "Support Assistant initialized."
    )

    ingestion_service = (
        IngestionService()
    )

    ingestion_service.run()

    logger.info(
        "Support Assistant completed successfully."
    )


if __name__ == "__main__":
    main()