"""
Task B.6 - Hyperparameter Tuning.

Tune Random Forest using GridSearchCV
and report the best parameter
combination together with the
Out-of-Bag (OOB) score.
"""

from __future__ import annotations

import joblib
import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
)

from sklearn.model_selection import (
    GridSearchCV,
)

from sklearn.pipeline import (
    Pipeline,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class HyperparameterTuningService:
    """
    Perform GridSearchCV on a
    Random Forest classifier.
    """

    def __init__(
        self,
    ) -> None:

        self.models_directory = (
            OUTPUTS_DIRECTORY
            / "models"
        )

        self.reports_directory = (
            REPORTS_DIRECTORY
        )

        self.models_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.reports_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        column_transformer,
    ):
        """
        Execute Task B.6.
        """

        logger.info(
            "Starting Task B.6 - Hyperparameter Tuning."
        )

        logger.info(
            "Preparing GridSearchCV pipeline."
        )
        
        pipeline = self.build_pipeline(
            column_transformer,
        )

        parameter_grid = (
            self.build_parameter_grid()
        )

        logger.info(
            "Initializing GridSearchCV."
        )

        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=parameter_grid,
            scoring="accuracy",
            cv=5,
            n_jobs=-1,
            verbose=1,
        )

        logger.info(
            "Starting GridSearchCV training."
        )

        grid_search.fit(
            X_train,
            y_train,
        )

        logger.info(
            "GridSearchCV completed successfully."
        )
        
        (
            best_pipeline,
            best_parameters,
            best_cv_score,
            oob_score,
        ) = self.save_results(
            grid_search,
        )

        parameter_report = pd.DataFrame(
            [best_parameters],
        )

        parameter_path = (
            self.reports_directory
            / "best_random_forest_parameters.csv"
        )

        parameter_report.to_csv(
            parameter_path,
            index=False,
        )

        summary_path = (
            self.reports_directory
            / "hyperparameter_tuning_summary.txt"
        )

        with open(
            summary_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                (
                    "Random Forest Hyperparameter Tuning\n"
                    "===================================\n\n"
                    f"Best Parameters\n"
                    f"{best_parameters}\n\n"
                    f"Best Cross Validation Accuracy : "
                    f"{best_cv_score:.4f}\n\n"
                    f"Out-of-Bag Score : "
                    f"{oob_score:.4f}\n"
                )
            )

        model_path = (
            self.models_directory
            / "best_random_forest_pipeline.pkl"
        )

        joblib.dump(
            best_pipeline,
            model_path,
        )

        logger.info(
            "Best pipeline saved to %s",
            model_path,
        )

        logger.info(
            "Best parameter report saved to %s",
            parameter_path,
        )

        logger.info(
            "Summary saved to %s",
            summary_path,
        )

        logger.info(
            "Task B.6 completed successfully."
        )

        return best_pipeline
        
    def build_pipeline(
        self,
        column_transformer,
    ) -> Pipeline:
        """
        Build Random Forest training
        pipeline.
        """

        logger.info(
            "Creating Random Forest pipeline."
        )

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    column_transformer,
                ),
                (
                    "classifier",
                    RandomForestClassifier(
                        random_state=42,
                        bootstrap=True,
                        oob_score=True,
                    ),
                ),
            ],
        )

        return pipeline

    def build_parameter_grid(
        self,
    ) -> dict:
        """
        Build GridSearchCV parameter
        grid.
        """

        logger.info(
            "Creating parameter grid."
        )

        parameter_grid = {
            "classifier__n_estimators": [
                100,
                200,
                300,
            ],
            "classifier__max_depth": [
                None,
                5,
                10,
                20,
            ],
            "classifier__max_features": [
                "sqrt",
                "log2",
            ],
        }

        logger.info(
            "Parameter combinations : %s",
            (
                len(parameter_grid["classifier__n_estimators"])
                * len(parameter_grid["classifier__max_depth"])
                * len(parameter_grid["classifier__max_features"])
            ),
        )

        return parameter_grid

    def save_results(
        self,
        grid_search: GridSearchCV,
    ) -> Pipeline:
        """
        Save the tuned Random Forest model
        together with the tuning summary.

        Returns
        -------
        Pipeline
            Best trained pipeline.
        """

        logger.info(
            "Extracting best model."
        )

        best_pipeline = (
            grid_search.best_estimator_
        )

        best_classifier = (
            best_pipeline.named_steps[
                "classifier"
            ]
        )

        best_parameters = (
            grid_search.best_params_
        )

        best_cv_score = (
            grid_search.best_score_
        )

        oob_score = (
            best_classifier.oob_score_
        )

        logger.info(
            "Best Parameters : %s",
            best_parameters,
        )

        logger.info(
            "Best Cross Validation Accuracy : %.4f",
            best_cv_score,
        )

        logger.info(
            "Out-of-Bag Score : %.4f",
            oob_score,
        )

        return (
            best_pipeline,
            best_parameters,
            best_cv_score,
            oob_score,
        )