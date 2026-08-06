"""
Task B.4 - Model Evaluation.

Evaluate all trained classification
models using the same test dataset.

Metrics:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC Curve
- AUC
- Confusion Matrix
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
    precision_score,
    recall_score,
    roc_curve,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class ModelEvaluationService:
    """
    Evaluate trained classification
    models.
    """

    def __init__(
        self,
    ) -> None:

        self.figures_directory = (
            OUTPUTS_DIRECTORY
            / "figures"
        )

        self.reports_directory = (
            REPORTS_DIRECTORY
        )

        self.figures_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.reports_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        trained_models: dict,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> pd.DataFrame:
        """
        Evaluate every trained model.

        Returns
        -------
        pandas.DataFrame
            Comparison table.
        """

        logger.info(
            "Starting Task B.4 - Model Evaluation."
        )

        comparison_results = []

        for model_name, pipeline in (
            trained_models.items()
        ):

            result = self.evaluate_model(
                model_name=model_name,
                pipeline=pipeline,
                X_test=X_test,
                y_test=y_test,
            )

            comparison_results.append(
                result,
            )
            self.save_confusion_matrix(
                model_name,
                result["Confusion Matrix"],
)

        comparison_table = pd.DataFrame(
            comparison_results,
        )

        comparison_table = comparison_table[
            [
                "Model",
                "Accuracy",
                "Precision",
                "Recall",
                "F1 Score",
                "AUC",
            ]
        ]

        comparison_path = (
            self.reports_directory
            / "classification_model_comparison.csv"
        )

        comparison_table.to_csv(
            comparison_path,
            index=False,
        )

        logger.info(
            "Classification comparison table saved to %s",
            comparison_path,
        )

        logger.info(
            "\n%s",
            comparison_table.to_string(
                index=False,
            ),
        )

        self.generate_roc_curve(
            comparison_results,
        )

        logger.info(
            "Task B.4 completed successfully."
        )

        return comparison_table
    
    def evaluate_model(
        self,
        model_name: str,
        pipeline,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> dict:
        """
        Evaluate a trained classification model.

        Parameters
        ----------
        model_name : str
            Name of the classifier.

        pipeline : Pipeline
            Trained sklearn pipeline.

        X_test : DataFrame
            Testing features.

        y_test : Series
            Testing labels.

        Returns
        -------
        dict
            Evaluation metrics.
        """

        logger.info(
            "Evaluating %s model.",
            model_name,
        )

        # Predictions
        y_pred = pipeline.predict(
            X_test,
        )

        # Prediction probabilities for ROC/AUC
        y_probability = pipeline.predict_proba(
            X_test,
        )[:, 1]

        # Metrics
        accuracy = accuracy_score(
            y_test,
            y_pred,
        )

        precision = precision_score(
            y_test,
            y_pred,
        )

        recall = recall_score(
            y_test,
            y_pred,
        )

        f1 = f1_score(
            y_test,
            y_pred,
        )

        # ROC
        false_positive_rate, true_positive_rate, _ = roc_curve(
            y_test,
            y_probability,
        )

        roc_auc = auc(
            false_positive_rate,
            true_positive_rate,
        )

        logger.info(
            "%s -> Accuracy : %.4f",
            model_name,
            accuracy,
        )

        logger.info(
            "%s -> Precision : %.4f",
            model_name,
            precision,
        )

        logger.info(
            "%s -> Recall : %.4f",
            model_name,
            recall,
        )

        logger.info(
            "%s -> F1 Score : %.4f",
            model_name,
            f1,
        )

        logger.info(
            "%s -> AUC : %.4f",
            model_name,
            roc_auc,
        )

        return {
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "AUC": roc_auc,
            "Confusion Matrix": confusion_matrix(
                y_test,
                y_pred,
            ),
            "False Positive Rate": false_positive_rate,
            "True Positive Rate": true_positive_rate,
        }

    def save_confusion_matrix(
        self,
        model_name: str,
        confusion_matrix_values,
    ) -> None:
        """
        Save confusion matrix figure.
        """

        logger.info(
            "Generating confusion matrix for %s.",
            model_name,
        )

        display = ConfusionMatrixDisplay(
            confusion_matrix=confusion_matrix_values,
            display_labels=[
                "Not Survived",
                "Survived",
            ],
        )

        fig, ax = plt.subplots(
            figsize=(
                6,
                5,
            ),
        )

        display.plot(
            ax=ax,
            cmap="Blues",
            colorbar=False,
        )

        plt.title(
            f"{model_name} Confusion Matrix",
        )

        figure_path = (
            self.figures_directory
            / f"confusion_matrix_{model_name}.png"
        )

        plt.tight_layout()

        plt.savefig(
            figure_path,
            dpi=300,
        )

        plt.close()

        logger.info(
            "Confusion matrix saved to %s",
            figure_path,
        )
        
    def generate_roc_curve(
        self,
        evaluation_results: list[dict],
    ) -> None:
        """
        Generate ROC comparison curve
        for all classification models.
        """

        logger.info(
            "Generating ROC comparison curve."
        )

        plt.figure(
            figsize=(
                8,
                6,
            ),
        )

        for result in evaluation_results:

            plt.plot(
                result["False Positive Rate"],
                result["True Positive Rate"],
                linewidth=2,
                label=(
                    f'{result["Model"]} '
                    f'(AUC={result["AUC"]:.3f})'
                ),
            )

        plt.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            color="black",
            label="No Skill",
        )

        plt.xlabel(
            "False Positive Rate",
        )

        plt.ylabel(
            "True Positive Rate",
        )

        plt.title(
            "ROC Curve Comparison",
        )

        plt.legend()

        plt.grid(
            alpha=0.3,
        )

        figure_path = (
            self.figures_directory
            / "roc_curve_comparison.png"
        )

        plt.tight_layout()

        plt.savefig(
            figure_path,
            dpi=300,
        )

        plt.close()

        logger.info(
            "ROC comparison curve saved to %s",
            figure_path,
        )