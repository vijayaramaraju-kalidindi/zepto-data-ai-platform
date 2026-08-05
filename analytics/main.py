"""
Entry point for Analytics module.
"""

from config.logging_config import get_logger
from datasets.titanic_loader import TitanicDatasetLoader


logger = get_logger(__name__)


def main() -> None:
    """
    Execute Analytics pipeline.
    """

    logger.info(
        "Starting Analytics Pipeline..."
    )

    loader = TitanicDatasetLoader()

    dataframe = loader.load_dataset()

    logger.info(
        "Rows: %s",
        len(dataframe),
    )

    logger.info(
        "Analytics Pipeline initialized successfully."
    )


if __name__ == "__main__":

    main()