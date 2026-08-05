"""
Exploratory Data Analysis (EDA) service.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config.logging_config import get_logger
from config.settings import (
    FIGURES_DIRECTORY,
    OUTPUTS_DIRECTORY,
)

logger = get_logger(__name__)


class EDAService:
    """
    Performs exploratory data analysis on the Titanic dataset.
    """

    def __init__(
        self,
    ) -> None:

        self.report_directory = (
            OUTPUTS_DIRECTORY / "reports"
        )

        self.report_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        FIGURES_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Execute all EDA tasks.

        Args:
            dataframe:
                Titanic dataset.
        """

        logger.info(
            "Starting Exploratory Data Analysis."
        )

        self.dataset_overview(
            dataframe,
        )

        self.summary_statistics(
            dataframe,
        )

        self.missing_values(
            dataframe,
        )

        self.target_distribution(
            dataframe,
        )

        logger.info(
            "EDA completed successfully."
        )

    def dataset_overview(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Save dataset overview.
        """

        overview = pd.DataFrame(
            {
                "Column": dataframe.columns,
                "Data Type": dataframe.dtypes.astype(str),
                "Missing Values": dataframe.isnull().sum().values,
            }
        )

        overview.to_csv(
            self.report_directory
            / "dataset_overview.csv",
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Dataset overview saved."
        )

    def summary_statistics(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Save descriptive statistics.
        """

        dataframe.describe(
            include="all",
        ).transpose().to_csv(
            self.report_directory
            / "summary_statistics.csv",
            encoding="utf-8-sig",
        )

        logger.info(
            "Summary statistics saved."
        )

    def missing_values(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Save missing value report.
        """

        missing = pd.DataFrame(
            {
                "Missing Values":
                dataframe.isnull().sum(),

                "Percentage":
                (
                    dataframe.isnull().mean()
                    * 100
                ).round(2),
            }
        )

        missing.to_csv(
            self.report_directory
            / "missing_values.csv",
            encoding="utf-8-sig",
        )

        logger.info(
            "Missing value report saved."
        )

    def target_distribution(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Plot survival distribution.
        """

        plt.figure(
            figsize=(6, 4),
        )

        sns.countplot(
            data=dataframe,
            x="survived",
        )

        plt.title(
            "Survival Distribution",
        )

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIRECTORY
            / "survival_distribution.png"
        )

        plt.close()

        logger.info(
            "Survival distribution figure saved."
        )