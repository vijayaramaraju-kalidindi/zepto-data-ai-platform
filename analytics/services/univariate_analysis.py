"""
Task A.3 - Univariate Analysis.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from config.logging_config import get_logger
from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class UnivariateAnalysisService:
    """
    Performs univariate analysis
    for Age and Fare.
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

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Execute Task A.3.
        """

        logger.info(
            "Starting Task A.3 - Univariate Analysis."
        )

        report = []

        for column in [
            "age",
            "fare",
        ]:

            logger.info(
                "Analyzing '%s'.",
                column,
            )

            report.append(
                self.analyze_column(
                    dataframe,
                    column,
                )
            )

            self.plot_histogram(
                dataframe,
                column,
            )

            self.plot_boxplot(
                dataframe,
                column,
            )

        report_df = pd.DataFrame(
            report,
        )

        report_df.to_csv(
            REPORTS_DIRECTORY
            / "univariate_analysis.csv",
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Task A.3 completed successfully."
        )

    def analyze_column(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> dict:
        """
        Analyze one numerical column.
        """

        series = dataframe[
            column
        ]

        mean = series.mean()

        median = series.median()

        mode = series.mode().iloc[0]

        q1 = series.quantile(
            0.25,
        )

        q3 = series.quantile(
            0.75,
        )

        iqr = q3 - q1

        lower_bound = (
            q1
            - 1.5 * iqr
        )

        upper_bound = (
            q3
            + 1.5 * iqr
        )

        outliers = series[
            (series < lower_bound)
            | (series > upper_bound)
        ]

        skewness = series.skew()

        if skewness > 0.5:

            distribution = (
                "Right Skewed"
            )

        elif skewness < -0.5:

            distribution = (
                "Left Skewed"
            )

        else:

            distribution = (
                "Approximately Symmetric"
            )

        logger.info(
            "%s -> Mean: %.2f Median: %.2f Mode: %.2f",
            column,
            mean,
            median,
            mode,
        )

        logger.info(
            "%s -> Q1: %.2f Q3: %.2f IQR: %.2f",
            column,
            q1,
            q3,
            iqr,
        )

        logger.info(
            "%s -> Lower Bound: %.2f Upper Bound: %.2f",
            column,
            lower_bound,
            upper_bound,
        )

        logger.info(
            "%s -> Outliers: %s",
            column,
            len(outliers),
        )

        logger.info(
            "%s -> Distribution: %s",
            column,
            distribution,
        )

        return {
            "column": column,
            "mean": round(
                mean,
                2,
            ),
            "median": round(
                median,
                2,
            ),
            "mode": round(
                mode,
                2,
            ),
            "q1": round(
                q1,
                2,
            ),
            "q3": round(
                q3,
                2,
            ),
            "iqr": round(
                iqr,
                2,
            ),
            "lower_bound": round(
                lower_bound,
                2,
            ),
            "upper_bound": round(
                upper_bound,
                2,
            ),
            "number_of_outliers": len(
                outliers,
            ),
            "distribution": distribution,
        }

    def plot_histogram(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> None:
        """
        Generate histogram.
        """

        plt.figure(
            figsize=(8, 5),
        )

        dataframe[
            column
        ].hist(
            bins=20,
        )

        plt.title(
            f"{column.title()} Histogram",
        )

        plt.xlabel(
            column.title(),
        )

        plt.ylabel(
            "Frequency",
        )

        plt.tight_layout()

        plt.savefig(
            self.figure_directory
            / f"{column}_histogram.png"
        )

        plt.close()

    def plot_boxplot(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> None:
        """
        Generate box plot.
        """

        plt.figure(
            figsize=(6, 4),
        )

        plt.boxplot(
            dataframe[
                column
            ],
            vert=True,
        )

        plt.title(
            f"{column.title()} Box Plot",
        )

        plt.tight_layout()

        plt.savefig(
            self.figure_directory
            / f"{column}_boxplot.png"
        )

        plt.close()