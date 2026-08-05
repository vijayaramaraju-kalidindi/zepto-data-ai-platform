"""
Task A.6 - Standardization Sanity Check.

Standardizes the Age and Fare columns
using z-score normalization for
exploratory analysis only.

This standardized data is NOT used by
the machine learning pipeline.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

from config.logging_config import get_logger
from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class StandardizationCheckService:
    """
    Performs an exploratory standardization
    check on Age and Fare.

    The original dataframe remains unchanged.
    """

    def __init__(
        self,
    ) -> None:

        self.figure_directory = (
            OUTPUTS_DIRECTORY
            / "figures"
        )

        self.figure_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.report_directory = (
            REPORTS_DIRECTORY
        )

        self.report_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Execute Task A.6.

        Args:
            dataframe:
                Cleaned Titanic dataframe.
        """

        logger.info(
            "Starting Task A.6 - Standardization Sanity Check."
        )

        scaled_dataframe = (
            dataframe.copy()
        )

        scaler = StandardScaler()

        scaled_dataframe[
            [
                "age",
                "fare",
            ]
        ] = scaler.fit_transform(
            scaled_dataframe[
                [
                    "age",
                    "fare",
                ]
            ]
        )

        self.calculate_statistics(
            original_dataframe=dataframe,
            scaled_dataframe=scaled_dataframe,
        )

        self.plot_age_distribution(
            original_dataframe=dataframe,
            scaled_dataframe=scaled_dataframe,
        )

        self.plot_fare_distribution(
            original_dataframe=dataframe,
            scaled_dataframe=scaled_dataframe,
        )

        logger.info(
            "Task A.6 completed successfully."
        )
        
    def calculate_statistics(
        self,
        original_dataframe: pd.DataFrame,
        scaled_dataframe: pd.DataFrame,
    ) -> None:
        """
        Compare statistics before and after
        standardization.

        Args:
            original_dataframe:
                Original cleaned dataframe.

            scaled_dataframe:
                Standardized dataframe.
        """

        logger.info(
            "Calculating standardization statistics."
        )

        rows = []

        for column in [
            "age",
            "fare",
        ]:

            before_mean = (
                original_dataframe[column]
                .mean()
            )

            before_std = (
                original_dataframe[column]
                .std()
            )

            after_mean = (
                scaled_dataframe[column]
                .mean()
            )

            after_std = (
                scaled_dataframe[column]
                .std()
            )

            logger.info(
                "%s Before -> Mean: %.4f Std: %.4f",
                column.capitalize(),
                before_mean,
                before_std,
            )

            logger.info(
                "%s After  -> Mean: %.4f Std: %.4f",
                column.capitalize(),
                after_mean,
                after_std,
            )

            rows.append(
                {
                    "column":
                        column,

                    "before_mean":
                        round(
                            before_mean,
                            4,
                        ),

                    "before_std":
                        round(
                            before_std,
                            4,
                        ),

                    "after_mean":
                        round(
                            after_mean,
                            4,
                        ),

                    "after_std":
                        round(
                            after_std,
                            4,
                        ),
                }
            )

        summary = pd.DataFrame(
            rows,
        )

        summary.to_csv(
            self.report_directory
            / "standardization_summary.csv",
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Standardization summary saved to %s",
            self.report_directory
            / "standardization_summary.csv",
        )

        logger.info(
            "EDA sanity check verified that "
            "the standardized features have "
            "approximately mean 0 and "
            "standard deviation 1."
        )
    
    def plot_age_distribution(
        self,
        original_dataframe: pd.DataFrame,
        scaled_dataframe: pd.DataFrame,
    ) -> None:
        """
        Compare original and standardized
        Age distributions.

        Args:
            original_dataframe:
                Original dataframe.

            scaled_dataframe:
                Standardized dataframe.
        """

        logger.info(
            "Generating Age standardization comparison plot."
        )

        plt.figure(
            figsize=(10, 6),
        )

        plt.hist(
            original_dataframe["age"],
            bins=30,
            alpha=0.6,
            label="Original Age",
            density=True,
        )

        plt.hist(
            scaled_dataframe["age"],
            bins=30,
            alpha=0.6,
            label="Standardized Age",
            density=True,
        )

        plt.title(
            "Age Distribution Before and After Standardization",
        )

        plt.xlabel(
            "Age / Standardized Age",
        )

        plt.ylabel(
            "Density",
        )

        plt.legend()

        plt.tight_layout()

        chart_path = (
            self.figure_directory
            / "age_standardization.png"
        )

        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Age standardization comparison saved to %s",
            chart_path,
        )
    def plot_fare_distribution(
        self,
        original_dataframe: pd.DataFrame,
        scaled_dataframe: pd.DataFrame,
    ) -> None:
        """
        Compare original and standardized
        Fare distributions.

        Args:
            original_dataframe:
                Original dataframe.

            scaled_dataframe:
                Standardized dataframe.
        """

        logger.info(
            "Generating Fare standardization comparison plot."
        )

        plt.figure(
            figsize=(10, 6),
        )

        plt.hist(
            original_dataframe["fare"],
            bins=30,
            alpha=0.6,
            density=True,
            label="Original Fare",
        )

        plt.hist(
            scaled_dataframe["fare"],
            bins=30,
            alpha=0.6,
            density=True,
            label="Standardized Fare",
        )

        plt.title(
            "Fare Distribution Before and After Standardization",
        )

        plt.xlabel(
            "Fare / Standardized Fare",
        )

        plt.ylabel(
            "Density",
        )

        plt.legend()

        plt.tight_layout()

        chart_path = (
            self.figure_directory
            / "fare_standardization.png"
        )

        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Fare standardization comparison saved to %s",
            chart_path,
        )