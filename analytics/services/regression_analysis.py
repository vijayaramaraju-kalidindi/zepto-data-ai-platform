"""
Task B.7 - Regression Analysis.

Predict passenger fare using
Multivariate Linear Regression.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class RegressionAnalysisService:
    """
    Multivariate Linear Regression.
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
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Execute Task B.7.
        """

        logger.info(
            "Starting Task B.7 - Regression Analysis."
        )

        logger.info(
            "Preparing regression dataset."
        )
        
        (
            X_train,
            X_test,
            y_train,
            y_test,
        ) = self.prepare_dataset(
            dataframe,
        )

        preprocessor = (
            self.build_preprocessor()
        )

        pipeline = self.train_model(
            X_train,
            y_train,
            preprocessor,
        )

        predictions = pipeline.predict(
            X_test,
        )
        
        logger.info(
            "Regression predictions generated."
        )
        
        metrics = self.evaluate_model(
            y_test=y_test,
            predictions=predictions,
            feature_count=X_train.shape[1],
        )

        self.generate_residual_plot(
            predictions=predictions,
            y_test=y_test,
        )

        self.save_results(
            metrics,
        )

        logger.info(
            "Task B.7 completed successfully."
        )

       
    def prepare_dataset(
        self,
        dataframe: pd.DataFrame,
    ):
        """
        Prepare train/test datasets
        for regression.
        """

        logger.info(
            "Preparing regression features and target."
        )

        features = [
            "pclass",
            "sex",
            "age",
            "sibsp",
            "parch",
            "embarked",
            "survived",
        ]

        target = "fare"

        X = dataframe[
            features
        ]

        y = dataframe[
            target
        ]

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42,
            )
        )

        logger.info(
            "Training Samples : %s",
            len(X_train),
        )

        logger.info(
            "Testing Samples : %s",
            len(X_test),
        )

        return (
            X_train,
            X_test,
            y_train,
            y_test,
        )
        
    def build_preprocessor(
        self,
    ) -> ColumnTransformer:
        """
        Build preprocessing pipeline
        for regression.
        """

        numeric_features = [
            "pclass",
            "age",
            "sibsp",
            "parch",
            "survived",
        ]

        categorical_features = [
            "sex",
            "embarked",
        ]

        numeric_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median",
                    ),
                ),
                (
                    "scaler",
                    StandardScaler(),
                ),
            ],
        )

        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="most_frequent",
                    ),
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore",
                    ),
                ),
            ],
        )

        return ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    numeric_pipeline,
                    numeric_features,
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    categorical_features,
                ),
            ],
        )

    def train_model(
        self,
        X_train,
        y_train,
        preprocessor,
    ):
        """
        Train Linear Regression.
        """

        logger.info(
            "Training Linear Regression model."
        )

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor,
                ),
                (
                    "regressor",
                    LinearRegression(),
                ),
            ],
        )

        pipeline.fit(
            X_train,
            y_train,
        )

        logger.info(
            "Linear Regression model trained successfully."
        )

        return pipeline

    def evaluate_model(
        self,
        y_test: pd.Series,
        predictions: np.ndarray,
        feature_count: int,
    ) -> dict:
        """
        Evaluate Linear Regression model.
        """

        logger.info(
            "Evaluating regression model."
        )

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions,
            )
        )

        r2 = r2_score(
            y_test,
            predictions,
        )

        adjusted_r2 = (
            1
            - (
                (1 - r2)
                * (len(y_test) - 1)
                / (
                    len(y_test)
                    - feature_count
                    - 1
                )
            )
        )

        logger.info(
            "MAE : %.4f",
            mae,
        )

        logger.info(
            "RMSE : %.4f",
            rmse,
        )

        logger.info(
            "R² : %.4f",
            r2,
        )

        logger.info(
            "Adjusted R² : %.4f",
            adjusted_r2,
        )

        return {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "Adjusted R2": adjusted_r2,
        }
        
    def generate_residual_plot(
        self,
        predictions: np.ndarray,
        y_test: pd.Series,
    ) -> None:
        """
        Generate residual plot.
        """

        logger.info(
            "Generating residual plot."
        )

        residuals = (
            y_test
            - predictions
        )

        plt.figure(
            figsize=(
                8,
                6,
            ),
        )

        plt.scatter(
            predictions,
            residuals,
            alpha=0.7,
        )

        plt.axhline(
            y=0,
            color="red",
            linestyle="--",
        )

        plt.xlabel(
            "Predicted Fare",
        )

        plt.ylabel(
            "Residuals",
        )

        plt.title(
            "Residual Plot",
        )

        plt.grid(
            alpha=0.3,
        )

        figure_path = (
            self.figures_directory
            / "regression_residual_plot.png"
        )

        plt.tight_layout()

        plt.savefig(
            figure_path,
            dpi=300,
        )

        plt.close()

        logger.info(
            "Residual plot saved to %s",
            figure_path,
        )

    def save_results(
        self,
        metrics: dict,
    ) -> None:
        """
        Save regression metrics and
        interpretation.
        """

        metrics_df = pd.DataFrame(
            [metrics]
        ).round(
            4,
        )

        metrics_path = (
            self.reports_directory
            / "regression_metrics.csv"
        )

        metrics_df.to_csv(
            metrics_path,
            index=False,
        )

        conclusion_path = (
            self.reports_directory
            / "regression_conclusion.txt"
        )

        with open(
            conclusion_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                (
                    "Regression Analysis\n"
                    "===================\n\n"
                    f"MAE : {metrics['MAE']:.4f}\n"
                    f"RMSE : {metrics['RMSE']:.4f}\n"
                    f"R² : {metrics['R2']:.4f}\n"
                    f"Adjusted R² : {metrics['Adjusted R2']:.4f}\n\n"
                    "Residual Plot Interpretation\n"
                    "----------------------------\n"
                    "Inspect the residual plot for a "
                    "random scatter around zero. "
                    "If residuals show a funnel shape "
                    "or systematic pattern, it suggests "
                    "heteroscedasticity. Otherwise, a "
                    "random spread indicates that the "
                    "constant variance assumption is "
                    "reasonably satisfied."
                )
            )

        logger.info(
            "Regression metrics saved to %s",
            metrics_path,
        )

        logger.info(
            "Regression interpretation saved to %s",
            conclusion_path,
        )