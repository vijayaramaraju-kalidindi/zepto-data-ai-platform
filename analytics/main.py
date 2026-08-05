"""
Entry point for Analytics module.
"""

from config.logging_config import get_logger
from datasets.titanic_loader import TitanicDatasetLoader
from services.preprocessing import PreprocessingService
from services.univariate_analysis import (UnivariateAnalysisService,)
from services.bivariate_analysis import (BivariateAnalysisService,)
from services.multivariate_analysis import (MultivariateAnalysisService,)
from services.standardization_check import (StandardizationCheckService,)


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
    
    from services.eda import EDAService
    eda = EDAService()

    dataframe = eda.run(
        dataframe,
    )

    preprocessor = PreprocessingService()

    dataframe = preprocessor.run(
        dataframe,
    )
    
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
    
    logger.info(
        "Rows: %s",
        len(dataframe),
    )

    logger.info(
        "Analytics Pipeline initialized successfully."
    )


if __name__ == "__main__":

    main()