"""
Task B.8 - Model Comparison.

Combine classification and regression
metrics into a single comparison report
and generate the final recommendation.
"""

from __future__ import annotations

import pandas as pd

from config.logging_config import (
    get_logger,
)

from config.settings import (
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class ModelComparisonService:
    """
    Generate the final model
    comparison report.
    """

    def __init__(
        self,
    ) -> None:

        self.reports_directory = (
            REPORTS_DIRECTORY
        )

        self.reports_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
    ) -> None:
        """
        Execute Task B.8.
        """

        logger.info(
            "Starting Task B.8 - Model Comparison."
        )

        classification = pd.read_csv(
            self.reports_directory
            / "classification_model_comparison.csv"
        )

        regression = pd.read_csv(
            self.reports_directory
            / "regression_metrics.csv"
        )

        comparison_table = (
            self.build_comparison_table(
                classification,
                regression,
            )
        )

        self.save_recommendation(
            classification,
        )

        logger.info(
            "Task B.8 completed successfully."
        )

        return comparison_table

    def build_comparison_table(
        self,
        classification: pd.DataFrame,
        regression: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create the combined model
        comparison table.

        Classification and regression
        metrics are presented as two
        separate metric groups.
        """

        logger.info(
            "Creating combined comparison table."
        )

        comparison = classification.copy()

        comparison.insert(
            0,
            "Model Type",
            "Classification",
        )

        comparison["MAE"] = "N/A"
        comparison["RMSE"] = "N/A"
        comparison["R2"] = "N/A"
        comparison["Adjusted R2"] = "N/A"

        regression_row = pd.DataFrame(
            [
                {
                    "Model Type": "Regression",
                    "Model": "Linear Regression",
                    "Accuracy": "N/A",
                    "Precision": "N/A",
                    "Recall": "N/A",
                    "F1 Score": "N/A",
                    "AUC": "N/A",
                    "MAE": regression.loc[0, "MAE"],
                    "RMSE": regression.loc[0, "RMSE"],
                    "R2": regression.loc[0, "R2"],
                    "Adjusted R2": regression.loc[
                        0,
                        "Adjusted R2",
                    ],
                }
            ]
        )

        comparison = pd.concat(
            [
                comparison,
                regression_row,
            ],
            ignore_index=True,
        )

        report_path = (
            self.reports_directory
            / "final_model_comparison.csv"
        )

        comparison.to_csv(
            report_path,
            index=False,
        )

        logger.info(
            "Final comparison table saved to %s",
            report_path,
        )

        logger.info(
            "\n%s",
            comparison.to_string(
                index=False,
            ),
        )

        return comparison

    def save_recommendation(
        self,
        classification: pd.DataFrame,
    ) -> None:
        """
        Generate the final deployment
        recommendation.
        """

        best_model = classification.loc[
            classification[
                "F1 Score"
            ].idxmax()
        ]

        recommendation_path = (
            self.reports_directory
            / "model_recommendation.txt"
        )

        with open(
            recommendation_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                (
                    "Final Model Recommendation\n"
                    "==========================\n\n"
                    f"The {best_model['Model']} classifier "
                    "is recommended for deployment because "
                    "it achieved the highest overall balance "
                    "between precision and recall.\n\n"
                    f"It achieved an Accuracy of "
                    f"{best_model['Accuracy']:.4f}, "
                    f"Precision of {best_model['Precision']:.4f}, "
                    f"Recall of {best_model['Recall']:.4f}, "
                    f"F1 Score of {best_model['F1 Score']:.4f}, "
                    f"and an AUC of {best_model['AUC']:.4f}.\n\n"
                    "Among the evaluated classifiers, this "
                    "model provides the strongest overall "
                    "classification performance while maintaining "
                    "good discrimination between survivors and "
                    "non-survivors. Based on these evaluation "
                    "metrics, it is the most suitable model for "
                    "deployment."
                )
            )

        logger.info(
            "Recommendation saved to %s",
            recommendation_path,
        )   

