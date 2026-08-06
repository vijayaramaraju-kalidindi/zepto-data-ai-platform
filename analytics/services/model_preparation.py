"""
Task B.1 - Model Preparation.

Splits the cleaned Titanic dataset into
training and testing datasets using a
stratified train/test split.

The target variable is 'survived'.
"""

from __future__ import annotations

import pandas as pd

from sklearn.model_selection import (
    train_test_split,
)

from config.logging_config import get_logger
from config.settings import (
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class ModelPreparationService:
    """
    Prepares the dataset for predictive
    modeling by performing a stratified
    train/test split.
    """

    def __init__(
        self,
    ) -> None:

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
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.Series,
        pd.Series,
    ]:
        """
        Execute Task B.1.

        Args:
            dataframe:
                Cleaned Titanic dataframe.

        Returns:
            X_train,
            X_test,
            y_train,
            y_test
        """

        logger.info(
            "Starting Task B.1 - Model Preparation."
        )

        logger.info(
            "Original dataset size: %s",
            len(
                dataframe,
            ),
        )

        logger.info(
            "Classification target: survived"
        )

        feature_columns = [
            "pclass",
            "age",
            "sibsp",
            "parch",
            "fare",
            "sex",
            "embarked",
        ]

        X = dataframe[
            feature_columns
        ].copy()

        y = dataframe[
            "survived"
        ]

        self.generate_class_distribution(
            y,
        )

        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = self.perform_split(
            X,
            y,
        )

        logger.info(
            "Task B.1 completed successfully."
        )

        return (
            X_train,
            X_test,
            y_train,
            y_test,
        )
    def generate_class_distribution(
        self,
        target: pd.Series,
    ) -> None:
        """
        Generate class distribution report
        and justify the use of stratified
        sampling.

        Args:
            target:
                Classification target.
        """

        logger.info(
            "Analyzing class distribution."
        )

        distribution = (
            target.value_counts()
            .sort_index()
        )

        percentages = (
            target.value_counts(
                normalize=True,
            )
            .sort_index()
            .mul(
                100,
            )
            .round(
                2,
            )
        )

        class_distribution = pd.DataFrame(
            {
                "class": [
                    "Not Survived",
                    "Survived",
                ],
                "count": distribution.values,
                "percentage": percentages.values,
            }
        )

        report_path = (
            self.report_directory
            / "class_distribution.csv"
        )

        class_distribution.to_csv(
            report_path,
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Class distribution saved to %s",
            report_path,
        )

        logger.info(
            "\n%s",
            class_distribution.to_string(index=False),
        )
        
        
        logger.info(
            "\n%s",
            class_distribution,
        )

        survived_percentage = (
            percentages.loc[
                1,
            ]
        )

        not_survived_percentage = (
            percentages.loc[
                0,
            ]
        )

        justification = (
            "The cleaned Titanic dataset contains "
            f"{survived_percentage:.2f}% survivors and "
            f"{not_survived_percentage:.2f}% non-survivors. "
            "A stratified train/test split preserves this "
            "class distribution in both training and testing "
            "datasets, ensuring representative sampling and "
            "reducing the risk of biased model evaluation."
        )

        justification_path = (
            self.report_directory
            / "stratification_justification.txt"
        )

        with open(
            justification_path,
            mode="w",
            encoding="utf-8",
        ) as file:

            file.write(
                justification,
            )

        logger.info(
            "Stratification justification saved to %s",
            justification_path,
        )

        logger.info(
            justification,
        )
    def perform_split(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.Series,
        pd.Series,
    ]:
        """
        Perform stratified train/test split.

        Args:
            X:
                Feature dataframe.

            y:
                Target series.

        Returns:
            X_train,
            X_test,
            y_train,
            y_test
        """

        logger.info(
            "Applying stratified train/test split "
            "(test_size=0.20, random_state=42)."
)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y,
        )

        training_percentage = (
            len(X_train)
            / len(X)
            * 100
        )

        testing_percentage = (
            len(X_test)
            / len(X)
            * 100
        )

        logger.info(
            "Training Samples : %s (%.0f%%)",
            len(
                X_train,
            ),
            training_percentage,
        )

        logger.info(
            "Testing Samples  : %s (%.0f%%)",
            len(
                X_test,
            ),
        testing_percentage,
        )

        train_distribution = (
            y_train.value_counts(
                normalize=True,
            )
            .sort_index()
            .mul(
                100,
            )
            .round(
                2,
            )
        )

        test_distribution = (
            y_test.value_counts(
                normalize=True,
            )
            .sort_index()
            .mul(
                100,
            )
            .round(
                2,
            )
        )

        logger.info(
            "Training Class Distribution"
        )

        logger.info(
            "\nNot Survived : %.2f%%"
            "\nSurvived     : %.2f%%",
            train_distribution.loc[
                0,
            ],
            train_distribution.loc[
                1,
            ],
        )

        logger.info(
            "Testing Class Distribution"
        )

        logger.info(
            "\nNot Survived : %.2f%%"
            "\nSurvived     : %.2f%%",
            test_distribution.loc[
                0,
            ],
            test_distribution.loc[
                1,
            ],
        )

        summary = pd.DataFrame(
            [
                {
                    "dataset": "Original",
                    "rows": len(
                        X,
                    ),
                },
                {
                    "dataset": "Training",
                    "rows": len(
                        X_train,
                    ),
                },
                {
                    "dataset": "Testing",
                    "rows": len(
                        X_test,
                    ),
                },
            ]
        )

        summary_path = (
            self.report_directory
            / "train_test_summary.csv"
        )

        summary.to_csv(
            summary_path,
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Train/Test summary saved to %s",
            summary_path,
        )

        return (
            X_train,
            X_test,
            y_train,
            y_test,
        )
