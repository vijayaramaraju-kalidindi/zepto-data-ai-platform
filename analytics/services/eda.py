"""
Exploratory Data Analysis (EDA) service.
"""

from __future__ import annotations

from io import StringIO

import pandas as pd

from config.logging_config import get_logger
from config.settings import (
    DATASET_BACKUP_PATH,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class EDAService:
    """
    Performs Task A.1 of the analytics pipeline.
    """

    def __init__(
        self,
    ) -> None:

        REPORTS_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute dataset profiling.

        Args:
            dataframe:
                Titanic DataFrame.

        Returns:
            Original DataFrame.
        """

        logger.info(
            "Starting dataset profiling."
        )

        self.save_dataset(
            dataframe,
        )

        self.dataset_shape(
            dataframe,
        )

        self.dataset_info(
            dataframe,
        )

        self.dataset_description(
            dataframe,
        )

        self.missing_value_report(
            dataframe,
        )

        logger.info(
            "Dataset profiling completed."
        )

        logger.info(
            "Task A.1 completed successfully."
        )
        return dataframe

    def save_dataset(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Save dataset as offline backup.
        """

        dataframe.to_csv(
            DATASET_BACKUP_PATH,
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Dataset backup saved to %s",
            DATASET_BACKUP_PATH,
        )

    def dataset_shape(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Print dataset shape.
        """

        print("\nDataset Shape\n")

        print(
            dataframe.shape,
        )

    def dataset_info(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Print and save dataframe info.
        """

        buffer = StringIO()

        dataframe.info(
            buf=buffer,
        )

        info_text = buffer.getvalue()

        print("\nDataset Information\n")

        print(
            info_text,
        )

        with open(
            REPORTS_DIRECTORY
            / "dataset_info.txt",
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                info_text,
            )

    def dataset_description(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Print and save descriptive statistics.
        """

        description = dataframe.describe(
            include="all",
        )

        print("\nDataset Description\n")

        print(
            description,
        )

        description.to_csv(
            REPORTS_DIRECTORY
            / "dataset_description.csv",
            encoding="utf-8-sig",
        )

    def missing_value_report(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Compute percentage of missing values.
        """

        missing = (
            dataframe.isnull()
            .mean()
            .mul(100)
            .round(2)
        )

        missing = missing[
            missing > 0
        ]

        report = pd.DataFrame(
            {
                "Missing Percentage":
                missing,
            }
        )

        print("\nMissing Values (%)\n")

        print(
            report,
        )

        report.to_csv(
            REPORTS_DIRECTORY
            / "missing_values.csv",
            encoding="utf-8-sig",
        )

        logger.info(
            "Missing value report generated."
        )