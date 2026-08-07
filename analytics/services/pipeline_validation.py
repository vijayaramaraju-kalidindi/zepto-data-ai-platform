"""
Task B.9 - Pipeline Validation.

Reload the saved pipeline and verify
that it predicts correctly on raw,
unprocessed input data.
"""

from __future__ import annotations

import joblib
import pandas as pd

from config.logging_config import (
    get_logger,
)

from config.settings import (
    OUTPUTS_DIRECTORY,
)

logger = get_logger(__name__)


class PipelineValidationService:
    """
    Validate the saved prediction
    pipeline.
    """

    def __init__(
        self,
    ) -> None:

        self.models_directory = (
            OUTPUTS_DIRECTORY
            / "models"
        )
        
    def run(
        self,
    ) -> None:
        """
        Execute Task B.9.
        """

        logger.info(
            "Starting Task B.9 - Pipeline Validation."
        )

        pipeline_path = (
            self.models_directory
            / "best_random_forest_pipeline.pkl"
        )

        logger.info(
            "Loading saved pipeline from %s",
            pipeline_path,
        )

        pipeline = joblib.load(
            pipeline_path,
        )

        logger.info(
            "Pipeline loaded successfully."
        )
        
        logger.info(
            "Creating raw passenger sample."
        )

        raw_input = pd.DataFrame(
            [
                {
                    "pclass": 1,
                    "age": 30,
                    "sibsp": 1,
                    "parch": 0,
                    "fare": 50.0,
                    "sex": "male",
                    "embarked": "S",
                }
            ]
        )
        
        logger.info(
        "Raw Passenger Input\n%s",
        raw_input.to_string(index=False),
    )

        logger.info(
            "Predicting directly from raw input."
        )

        prediction = pipeline.predict(
            raw_input,
        )[0]

        probability = pipeline.predict_proba(
            raw_input,
        )[0]
        
        logger.info(
            "Prediction : %s",
            prediction,
        )

        logger.info(
            "Prediction Probabilities : %s",
            probability,
        )

        logger.info(
            "Pipeline successfully performed "
            "end-to-end prediction on raw input."
        )

        logger.info(
            "Task B.9 completed successfully."
        )