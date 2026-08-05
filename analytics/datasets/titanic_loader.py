"""
Dataset loader for the Titanic dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import seaborn as sns

from config.logging_config import get_logger
from config.settings import DATASET_PATH


logger = get_logger(__name__)


class TitanicDatasetLoader:
    """
    Loads the Titanic dataset.
    """

    def load_dataset(
        self,
    ) -> pd.DataFrame:
        """
        Load the Titanic CSV file.

        Returns:
            Loaded pandas DataFrame.

        Raises:
            FileNotFoundError
                If dataset is missing.
        """

        if not DATASET_PATH.exists():

            raise FileNotFoundError(
                f"Dataset not found: {DATASET_PATH}"
            )

        dataframe = sns.load_dataset(
            "titanic"
        )

        logger.info(
            "Dataset loaded successfully."
        )

        logger.info(
            "Dataset shape: %s",
            dataframe.shape,
        )

        return dataframe