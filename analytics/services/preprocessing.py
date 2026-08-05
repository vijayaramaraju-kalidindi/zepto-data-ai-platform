"""
Data preprocessing service for Task A.2.
"""

from __future__ import annotations

import pandas as pd

from config.logging_config import get_logger
from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class PreprocessingService:
    """
    Handles missing values according
    to the rubric thresholds.
    """

    def __init__(
        self,
    ) -> None:

        self.cleaned_dataset_path = (
            OUTPUTS_DIRECTORY
            / "cleaned_titanic.csv"
        )

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute preprocessing.

        Args:
            dataframe:
                Titanic dataframe.

        Returns:
            Cleaned dataframe.
        """

        logger.info(
            "Starting missing value handling."
        )

        report = []

        dataframe = dataframe.copy()

        missing_percentages = (
            dataframe.isnull()
            .mean()
            .mul(100)
        )

        for column in dataframe.columns:

            missing_percentage = (
                missing_percentages[column]
            )

            if missing_percentage == 0:

                continue

            logger.info(
                "Column '%s' has %.2f%% missing values.",
                column,
                missing_percentage,
            )

            action = ""

            justification = ""

            if missing_percentage < 5:

                before = len(
                    dataframe,
                )

                dataframe = dataframe.dropna(
                    subset=[
                        column,
                    ],
                )

                after = len(
                    dataframe,
                )

                action = (
                    "Drop Rows"
                )

                justification = (
                    "Missing percentage is below 5%. "
                    "Rows containing missing values "
                    "were removed as specified by "
                    "the rubric."
                )

                logger.info(
                    "Strategy selected for '%s': Drop Rows.",
                    column,
                )

            elif missing_percentage <= 30:

                median = dataframe[
                    column
                ].median()

                dataframe[column] = (
                    dataframe[column]
                    .fillna(
                        median,
                    )
                )

                action = (
                    "Median Imputation"
                )

                justification = (
                    "Missing percentage is between "
                    "5% and 30%. Median imputation "
                    "was applied as specified by "
                    "the rubric."
                )

                logger.info(
                    "Strategy selected for '%s': Median Imputation.",
                    column,
                )

            else:

                dataframe = dataframe.drop(
                    columns=[
                        column,
                    ],
                )

                action = (
                    "Drop Column"
                )

                justification = (
                    "Missing percentage is above "
                    "30%. The column was dropped "
                    "because imputation would be "
                    "unreliable for such a high "
                    "proportion of missing values."
                )

                logger.info(
                    "Strategy selected for '%s': Drop Column.",
                    column,
                )

            report.append(
                {
                    "column":
                        column,

                    "missing_percentage":
                        round(
                            missing_percentage,
                            2,
                        ),

                    "action":
                        action,

                    "justification":
                        justification,
                }
            )

        report_df = pd.DataFrame(
            report,
        )

        report_df.to_csv(
            REPORTS_DIRECTORY
            / "missing_value_handling_report.csv",
            index=False,
            encoding="utf-8-sig",
        )

        dataframe.to_csv(
            self.cleaned_dataset_path,
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Missing value handling report generated."
        )

        logger.info(
            "Cleaned dataset saved to %s",
            self.cleaned_dataset_path,
        )

        logger.info(
            "Task A.2 completed successfully."
        )

        return dataframe