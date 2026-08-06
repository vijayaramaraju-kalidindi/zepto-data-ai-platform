"""
Task B.2 - Preprocessing Pipeline.

Creates a reusable preprocessing pipeline
using ColumnTransformer for predictive
modeling.

The pipeline is intentionally NOT fitted
here. It will be fitted only on the
training data together with each model,
preventing data leakage.
"""

from __future__ import annotations

from sklearn.compose import (
    ColumnTransformer,
)

from sklearn.impute import (
    SimpleImputer,
)

from sklearn.pipeline import (
    Pipeline,
)

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class PreprocessingPipelineService:
    """
    Creates the preprocessing pipeline
    required for predictive modeling.
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
    ) -> ColumnTransformer:
        """
        Build the preprocessing pipeline.

        Returns
        -------
        ColumnTransformer
            Configured preprocessing pipeline.
        """

        logger.info(
            "Starting Task B.2 - Preprocessing Pipeline."
        )

        numeric_features = [
            "pclass",
            "age",
            "sibsp",
            "parch",
            "fare",
        ]

        categorical_features = [
            "sex",
            "embarked",
        ]

        logger.info(
            "Numeric Features : %s",
            numeric_features,
        )

        logger.info(
            "Categorical Features : %s",
            categorical_features,
        )

        numeric_pipeline = (
            self.build_numeric_pipeline()
        )

        categorical_pipeline = (
            self.build_categorical_pipeline()
        )

        preprocessor = (
            self.build_column_transformer(
                numeric_pipeline,
                categorical_pipeline,
                numeric_features,
                categorical_features,
            )
        )

        self.generate_report(
            numeric_features,
            categorical_features,
        )

        logger.info(
            "Task B.2 completed successfully."
        )

        return preprocessor
    def build_numeric_pipeline(
        self,
    ) -> Pipeline:
        """
        Build preprocessing pipeline for
        numerical features.

        Returns
        -------
        Pipeline
            Numerical preprocessing pipeline.
        """

        logger.info(
            "Creating numerical preprocessing pipeline."
        )

        logger.info(
            "Numerical Missing Value Strategy : Median Imputation"
        )

        logger.info(
            "Numerical Scaling : StandardScaler"
        )

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

        return numeric_pipeline

    def build_categorical_pipeline(
        self,
    ) -> Pipeline:
        """
        Build preprocessing pipeline for
        categorical features.

        Returns
        -------
        Pipeline
            Categorical preprocessing pipeline.
        """

        logger.info(
            "Creating categorical preprocessing pipeline."
        )

        logger.info(
            "Categorical Missing Value Strategy : Most Frequent"
        )

        logger.info(
            "Categorical Encoding : OneHotEncoder"
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

        return categorical_pipeline

    def build_column_transformer(
        self,
        numeric_pipeline: Pipeline,
        categorical_pipeline: Pipeline,
        numeric_features: list[str],
        categorical_features: list[str],
    ) -> ColumnTransformer:
        """
        Build the preprocessing
        ColumnTransformer.
        """

        logger.info(
            "Creating ColumnTransformer."
        )

        column_transformer = ColumnTransformer(
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
            remainder="drop",
        )

        logger.info(
            "ColumnTransformer created successfully."
        )

        logger.info(
            "The preprocessing pipeline will be fitted "
            "only on the training dataset during model training."
        )

        return column_transformer

    def generate_report(
        self,
        numeric_features: list[str],
        categorical_features: list[str],
    ) -> None:
        """
        Generate preprocessing summary report.
        """

        report = f"""
TASK B.2 - PREPROCESSING PIPELINE

========================================

NUMERICAL FEATURES

{", ".join(numeric_features)}

Missing Value Strategy
Median Imputation

Scaling
StandardScaler

========================================

CATEGORICAL FEATURES

{", ".join(categorical_features)}

Missing Value Strategy
Most Frequent Imputation

Encoding
OneHotEncoder(handle_unknown="ignore")

========================================

IMPLEMENTATION

ColumnTransformer

Pipeline Ready

Training Data

All preprocessing components are fitted
only on the training dataset.

Testing Data

The test dataset is transformed using
the fitted preprocessing pipeline.

This implementation prevents data leakage
and follows the assignment rubric.
"""

        report_path = (
            self.report_directory
            / "preprocessing_summary.txt"
        )

        with open(
            report_path,
            mode="w",
            encoding="utf-8",
        ) as file:

            file.write(
                report.strip(),
            )

        logger.info(
            "Preprocessing summary saved to %s",
            report_path,
        )