"""
Entry point for Analytics module.
"""

from config.logging_config import get_logger
from services.eda import EDAService
from datasets.titanic_loader import TitanicDatasetLoader
from services.preprocessing import PreprocessingService
from services.univariate_analysis import (UnivariateAnalysisService,)
from services.bivariate_analysis import (BivariateAnalysisService,)
from services.multivariate_analysis import (MultivariateAnalysisService,)
from services.standardization_check import (StandardizationCheckService,)
from services.model_preparation import (ModelPreparationService,)
from services.preprocessing_pipeline import (PreprocessingPipelineService,)
from services.classification_models import (ClassificationModelsService,)
from services.model_evaluation import (ModelEvaluationService,)
from services.imbalance_analysis import (ImbalanceAnalysisService,)
from services.hyperparameter_tuning import (HyperparameterTuningService,)
from services.regression_analysis import (RegressionAnalysisService,)
from services.model_comparison import (ModelComparisonService,)
from services.pipeline_validation import (PipelineValidationService,)


logger = get_logger(__name__)

def main() -> None:
    """
    Execute Analytics pipeline.
    """

    logger.info(
        "Starting Analytics Pipeline..."
    )

    loader = TitanicDatasetLoader()

    dataframe = loader.load_dataset()
    
    eda = EDAService()

    dataframe = eda.run(
        dataframe,
    )

    preprocessing_service = (PreprocessingService())

    dataframe = preprocessing_service.run(
        dataframe,
    )
    
 #   preprocessor = PreprocessingService()

 #   dataframe = preprocessor.run(
 #       dataframe,
 #   )
    
    univariate = (
        UnivariateAnalysisService()
    )

    univariate.run(
        dataframe,
    )

    bivariate = (
        BivariateAnalysisService()
    )

    bivariate.run(
        dataframe,
    )
    
    multivariate = (
        MultivariateAnalysisService()
    )

    multivariate.run(
        dataframe,
    )
    
    standardization = StandardizationCheckService()

    standardization.run(
        dataframe,
    )
    
    model_preparation = (
        ModelPreparationService()
    )
    
    (
    X_train,
    X_test,
    y_train,
    y_test,
    ) = model_preparation.run(
    dataframe,
    )

    preprocessing_pipeline = (
        PreprocessingPipelineService()
    )

    column_transformer = (
    preprocessing_pipeline.run()
    )
    classification_models = (
    ClassificationModelsService()
    )

    trained_models = (
        classification_models.run(
        X_train=X_train,
        y_train=y_train,
        column_transformer=column_transformer,
    )
)
    
    model_evaluation = (
    ModelEvaluationService()
    )

    comparison_table = (
        model_evaluation.run(
            trained_models=trained_models,
            X_test=X_test,
            y_test=y_test,
    )
)
    imbalance_analysis = (
    ImbalanceAnalysisService()
    )

    imbalance_comparison = (
        imbalance_analysis.run(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            column_transformer=column_transformer,
        )
    )
    
    hyperparameter_tuning = (
    HyperparameterTuningService()
    )

    best_pipeline = (
        hyperparameter_tuning.run(
            X_train=X_train,
            y_train=y_train,
            column_transformer=column_transformer,
        )
    )

    regression_analysis = (
        RegressionAnalysisService()
    )

    regression_analysis.run(
        dataframe,
    )
    
    model_comparison = (
    ModelComparisonService()
    )
    
    model_comparison.run()

    pipeline_validation = (
    PipelineValidationService()
    )

    pipeline_validation.run()
    
    logger.info(
        "Rows: %s",
        len(dataframe),
    )

    logger.info(
        "Analytics Pipeline initialized successfully."
    )


if __name__ == "__main__":

    main()