"""
Task B.5 - Imbalance Handling Comparison.

Compare different techniques for
handling class imbalance using
Random Forest.

Strategies
----------
1. Baseline
2. class_weight='balanced'
3. SMOTE
"""

from __future__ import annotations

import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
)

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)


from imblearn.pipeline import (
    Pipeline,
)
from imblearn.over_sampling import (
    SMOTE,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class ImbalanceAnalysisService:
    """
    Compare imbalance handling
    strategies.
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
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        column_transformer,
    ) -> pd.DataFrame:
        """
        Execute Task B.5.

        Returns
        -------
        DataFrame
            Strategy comparison table.
        """

        logger.info(
            "Starting Task B.5 - Imbalance Handling Comparison."
        )

        logger.info(
            "Training classifier using three imbalance handling strategies."
        )

        class_balance = (
            y_train.value_counts()
            .rename(index={
                0: "Not Survived",
                1: "Survived",
            })
            .to_frame(name="Count")
        )

        # Remove the index name for cleaner output
        class_balance.index.name = None

        class_balance["Percentage"] = (
            class_balance["Count"]
            / class_balance["Count"].sum()
            * 100
        ).round(2)

        class_balance_path = (
            self.reports_directory
            / "class_balance_before_smote.csv"
        )

        class_balance.to_csv(
            class_balance_path,
        )

        logger.info(
            "Training class distribution\n%s",
            class_balance.to_string(),
        )

        logger.info(
            "Class balance report saved to %s",
            class_balance_path,
        )
        
        
        comparison_results = []

        baseline_pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    column_transformer,
                ),
                (
                    "classifier",
                    RandomForestClassifier(
                        random_state=42,
                    ),
                ),
            ],
        )

        comparison_results.append(
            self.train_and_evaluate(
                strategy_name="Baseline",
                pipeline=baseline_pipeline,
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
            )
        )
        
        balanced_pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    column_transformer,
                ),
                (
                    "classifier",
                    RandomForestClassifier(
                        random_state=42,
                        class_weight="balanced",
                    ),
                ),
            ],
        )

        comparison_results.append(
            self.train_and_evaluate(
                strategy_name="Class Weight Balanced",
                pipeline=balanced_pipeline,
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
            )
        )

        smote_pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    column_transformer,
                ),
                (
                    "smote",
                    SMOTE(
                        random_state=42,
                    ),
                ),
                (
                    "classifier",
                    RandomForestClassifier(
                        random_state=42,
                    ),
                ),
            ],
        )

        comparison_results.append(
            self.train_and_evaluate(
                strategy_name="SMOTE",
                pipeline=smote_pipeline,
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
            )
        )

        comparison_table = pd.DataFrame(
            comparison_results,
        )

        comparison_table = comparison_table.round(
            4,
        )

        report_path = (
            self.reports_directory
            / "imbalance_comparison.csv"
        )

        comparison_table.to_csv(
            report_path,
            index=False,
        )

        logger.info(
            "Imbalance comparison saved to %s",
            report_path,
        )

        logger.info(
            "\n%s",
            comparison_table.to_string(
                index=False,
            ),
        )

        best_strategy = comparison_table.loc[
            comparison_table[
                "F1 Score"
            ].idxmax()
        ]

        conclusion_path = (
            self.reports_directory
            / "imbalance_conclusion.txt"
        )

        with open(
            conclusion_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                (
                    "Imbalance Handling Comparison\n"
                    "============================\n\n"
                    f"Best Strategy : {best_strategy['Strategy']}\n\n"
                    f"Precision : {best_strategy['Precision']:.4f}\n"
                    f"Recall    : {best_strategy['Recall']:.4f}\n"
                    f"F1 Score  : {best_strategy['F1 Score']:.4f}\n\n"
                    "Three strategies were evaluated:\n"
                    "1. Baseline Random Forest\n"
                    "2. Random Forest with class_weight='balanced'\n"
                    "3. Random Forest with SMOTE oversampling\n\n"
                    "The selected strategy achieved the highest "
                    "F1 Score while maintaining a good balance "
                    "between precision and recall. Since F1 Score "
                    "combines both metrics into a single measure, "
                    "it is the most appropriate metric for comparing "
                    "performance on moderately imbalanced datasets."
                )
            )

        logger.info(
            "Conclusion saved to %s",
            conclusion_path,
        )

        logger.info(
            "Task B.5 completed successfully."
        )

        return comparison_table
        

    def train_and_evaluate(
        self,
        strategy_name: str,
        pipeline,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ) -> dict:
        """
        Train and evaluate one imbalance
        handling strategy.

        Parameters
        ----------
        strategy_name : str
            Name of the strategy.

        pipeline : Pipeline
            Complete ML pipeline.

        Returns
        -------
        dict
            Evaluation metrics.
        """

        logger.info(
            "Training strategy : %s",
            strategy_name,
        )

        pipeline.fit(
            X_train,
            y_train,
        )

        y_pred = pipeline.predict(
            X_test,
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

        logger.info(
            "%s -> Precision : %.4f",
            strategy_name,
            precision,
        )

        logger.info(
            "%s -> Recall : %.4f",
            strategy_name,
            recall,
        )

        logger.info(
            "%s -> F1 Score : %.4f",
            strategy_name,
            f1,
        )

        return {
            "Strategy": strategy_name,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
        }
        
