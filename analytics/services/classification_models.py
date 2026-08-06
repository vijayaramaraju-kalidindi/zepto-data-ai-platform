"""
Task B.3 - Classification Models.

Train Logistic Regression,
Decision Tree and Random Forest
using the same preprocessing
pipeline and train/test split.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline

from sklearn.linear_model import (
    LogisticRegression,
)

from sklearn.tree import (
    DecisionTreeClassifier, 
    plot_tree,
)

from sklearn.ensemble import (
    RandomForestClassifier,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    OUTPUTS_DIRECTORY,
)

logger = get_logger(__name__)


class ClassificationModelsService:
    """
    Train classification models
    required for Task B.3.
    """

    def __init__(
        self,
    ) -> None:

        self.models_directory = (
            OUTPUTS_DIRECTORY
            / "models"
        )

        self.figures_directory = (
            OUTPUTS_DIRECTORY
            / "figures"
        )

        self.models_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.figures_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        column_transformer,
    ) -> dict:
        """
        Train all classification
        models.

        Args:
            X_train:
                Training features.

            y_train:
                Training target.

            column_transformer:
                Preprocessing pipeline.

        Returns
        -------
        dict
            Dictionary containing all
            trained pipelines.
        """

        logger.info(
            "Starting Task B.3 - Classification Models."
        )

        models = {}

        models[
            "logistic_regression"
        ] = self.train_pipeline(
            model_name="Logistic Regression",
            estimator=LogisticRegression(
                random_state=42,
                max_iter=1000,
            ),
            model_file="logistic_regression_pipeline.pkl",
            X_train=X_train,
            y_train=y_train,
            column_transformer=column_transformer,
        )

        decision_tree_pipeline = (
            self.train_pipeline(
                model_name="Decision Tree",
                estimator=DecisionTreeClassifier(
                random_state=42,
                ),
                model_file="decision_tree_pipeline.pkl",
                X_train=X_train,
                y_train=y_train,
                column_transformer=column_transformer,
    )
)

        models[
            "decision_tree"
            ] = decision_tree_pipeline

        self.generate_decision_tree_visualization(
            decision_tree_pipeline,
)
        
        models[
            "random_forest"
        ] = self.train_pipeline(
            model_name="Random Forest",
            estimator=RandomForestClassifier(
                random_state=42,
            ),
            model_file="random_forest_pipeline.pkl",
            X_train=X_train,
            y_train=y_train,
            column_transformer=column_transformer,
        )

        logger.info(
            "Task B.3 completed successfully."
        )

        return models

    def train_pipeline(
        self,
        model_name: str,
        estimator,
        model_file: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        column_transformer,
    ) -> Pipeline:
        """
        Build, train and save a
        classification pipeline.

        Args:
            model_name:
                Name of the classifier.

            estimator:
                Scikit-learn estimator.

            model_file:
                Output filename.

            X_train:
                Training features.

            y_train:
                Training labels.

            column_transformer:
                Preprocessing pipeline.

        Returns
        -------
        Pipeline
            Trained pipeline.
        """

        logger.info(
            "Training %s model.",
            model_name,
        )

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    column_transformer,
                ),
                (
                    "classifier",
                    estimator,
                ),
            ],
        )

        logger.info(
            "Fitting preprocessing pipeline and %s using only the training dataset.",
            model_name,
        )

        pipeline.fit(
            X_train,
            y_train,
        )

        logger.info(
            "%s model training completed.",
            model_name,
        )

        model_path = (
            self.models_directory
            / model_file
        )

        joblib.dump(
            pipeline,
            model_path,
        )

        logger.info(
            "%s pipeline saved to %s",
            model_name,
            model_path,
        )

        transformed_feature_count = len(
            pipeline.named_steps[
                "preprocessor"
            ].get_feature_names_out()
        )

        selected_feature_count = (
            len(
                pipeline.named_steps[
                "preprocessor"
            ].feature_names_in_
    )
)

        logger.info(
            "Selected Input Features : %s",
            selected_feature_count,
        )

        
        logger.info(
            "Transformed Features : %s",
            transformed_feature_count,
        )

        return pipeline

    def generate_decision_tree_visualization(
        self,
        pipeline: Pipeline,
    ) -> None:
        """
        Generate and save the Decision
        Tree visualization.

        Args:
            pipeline:
                Trained Decision Tree
                pipeline.
        """

        logger.info(
            "Generating Decision Tree visualization."
        )

        decision_tree = (
            pipeline.named_steps[
                "classifier"
            ]
        )

        feature_names = (
            pipeline.named_steps[
                "preprocessor"
            ].get_feature_names_out()
        )

        plt.figure(
            figsize=(
                24,
                12,
            ),
        )

        plot_tree(
            decision_tree,
            feature_names=feature_names,
            class_names=[
                "Not Survived",
                "Survived",
            ],
            filled=True,
            rounded=True,
            fontsize=8,
        )

        figure_path = (
            self.figures_directory
            / "decision_tree.png"
        )

        plt.tight_layout()

        plt.savefig(
            figure_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Decision Tree visualization saved to %s",
            figure_path,
        )
        