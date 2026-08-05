"""
Dataset loader for the Titanic dataset.
"""

from __future__ import annotations

import pandas as pd
import seaborn as sns

from config.logging_config import get_logger

logger = get_logger(__name__)


class TitanicDatasetLoader:
    """
    Loads the Titanic dataset using Seaborn.
    """

    def load_dataset(
        self,
    ) -> pd.DataFrame:
        """
        Load the Titanic dataset.

        Returns:
            Loaded pandas DataFrame.
        """

        logger.info(
            "Loading Titanic dataset using seaborn."
        )

        dataframe = sns.load_dataset(
            "titanic",
        )

        logger.info(
            "Dataset loaded successfully."
        )

        logger.info(
            "Dataset shape: %s",
            dataframe.shape,
        )

        return dataframe