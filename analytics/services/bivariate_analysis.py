"""
Task A.4 - Bivariate Analysis.
"""

from __future__ import annotations

import itertools

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config.logging_config import get_logger
from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class BivariateAnalysisService:
    """
    Performs Task A.4.
    """

    def __init__(
        self,
    ) -> None:

        self.figure_directory = (
            OUTPUTS_DIRECTORY
            / "figures"
        )

        self.figure_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Execute Task A.4.
        """

        logger.info(
            "Starting Task A.4 - Bivariate Analysis."
        )

        self.survival_by_sex(
            dataframe,
        )

        self.survival_by_pclass(
            dataframe,
        )

        self.survival_by_sex_pclass(
            dataframe,
        )

        self.correlation_analysis(
            dataframe,
        )

        logger.info(
            "Task A.4 completed successfully."
        )

    def survival_by_sex(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Survival rate by sex.
        """

        logger.info(
            "Computing survival rate by sex."
        )

        rows = []

        for sex in [
            "female",
            "male",
        ]:

            mask = (
                (dataframe["sex"] == sex)
                &
                (dataframe["survived"].isin([0, 1]))
            )
            
            survival_rate = (
                dataframe.loc[
                    mask,
                    "survived",
                ].mean()
                * 100
            )

            rows.append(
                {
                    "sex": sex,
                    "survival_rate": round(
                        survival_rate,
                        2,
                    ),
                }
            )

        result = pd.DataFrame(
            rows,
        )

        logger.info(
            "\n%s",
            result,
        )

        result.to_csv(
            REPORTS_DIRECTORY
            / "survival_rate_by_sex.csv",
            index=False,
            encoding="utf-8-sig",
        )

    def survival_by_pclass(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Survival rate by passenger class.
        """

        logger.info(
            "Computing survival rate by passenger class."
        )

        rows = []

        for pclass in [
            1,
            2,
            3,
        ]:

            mask = (
                (dataframe["pclass"] == pclass)
                &
                (dataframe["survived"].isin([0, 1]))
            )
            
            survival_rate = (
                dataframe.loc[
                    mask,
                    "survived",
                ].mean()
                * 100
            )

            rows.append(
                {
                    "pclass": pclass,
                    "survival_rate": round(
                        survival_rate,
                        2,
                    ),
                }
            )

        result = pd.DataFrame(
            rows,
        )

        logger.info(
            "\n%s",
            result,
        )

        result.to_csv(
            REPORTS_DIRECTORY
            / "survival_rate_by_pclass.csv",
            index=False,
            encoding="utf-8-sig",
        )

    def survival_by_sex_pclass(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Survival rate by sex and passenger class.
        """

        logger.info(
            "Computing survival rate by sex and passenger class."
        )

        rows = []

        for sex, pclass in itertools.product(
            [
                "female",
                "male",
            ],
            [
                1,
                2,
                3,
            ],
        ):

            mask = (
                (dataframe["sex"] == sex)
                &
                (dataframe["pclass"] == pclass)
            )

            survival_rate = (
                dataframe.loc[
                    mask,
                    "survived",
                ].mean()
                * 100
            )

            rows.append(
                {
                    "sex": sex,
                    "pclass": pclass,
                    "survival_rate": round(
                        survival_rate,
                        2,
                    ),
                }
            )

        result = pd.DataFrame(
            rows,
        )

        logger.info(
            "\n%s",
            result,
        )

        result.to_csv(
            REPORTS_DIRECTORY
            / "survival_rate_by_sex_pclass.csv",
            index=False,
            encoding="utf-8-sig",
        )

    def correlation_analysis(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Correlation analysis.
        """

        logger.info(
            "Computing correlation matrix."
        )

        columns = [
            "survived",
            "pclass",
            "age",
            "sibsp",
            "parch",
            "fare",
        ]

        correlation = dataframe[
            columns
        ].corr()

        correlation.to_csv(
            REPORTS_DIRECTORY
            / "correlation_matrix.csv",
            encoding="utf-8-sig",
        )

        plt.figure(
            figsize=(8, 6),
        )

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
        )

        plt.title(
            "Correlation Heatmap",
        )

        plt.tight_layout()

        plt.savefig(
            self.figure_directory
            / "correlation_heatmap.png"
        )

        plt.close()

        logger.info(
            "Correlation heatmap saved."
        )

        pairs = []

        for i in range(
            len(columns),
        ):

            for j in range(
                i + 1,
                len(columns),
            ):

                value = correlation.iloc[
                    i,
                    j,
                ]

                pairs.append(
                    {
                        "feature_1": columns[i],
                        "feature_2": columns[j],
                        "correlation": round(
                            value,
                            4,
                        ),
                        "absolute_correlation": abs(
                            value,
                        ),
                    }
                )

        top_pairs = (
            pd.DataFrame(
                pairs,
            )
            .sort_values(
                by="absolute_correlation",
                ascending=False,
            )
            .head(
                2,
            )
            .reset_index(
                drop=True,
            )
        )

        interpretations = []

        for _, row in top_pairs.iterrows():

            if (
                row["feature_1"] == "pclass"
                and row["feature_2"] == "fare"
            ) or (
                row["feature_1"] == "fare"
                and row["feature_2"] == "pclass"
            ):

                interpretation = (
                    "Passengers travelling in higher "
                    "passenger classes generally paid "
                    "higher fares, resulting in a "
                    "moderate negative correlation "
                    "between pclass and fare."
                )

            elif (
                row["feature_1"] == "sibsp"
                and row["feature_2"] == "parch"
            ) or (
                row["feature_1"] == "parch"
                and row["feature_2"] == "sibsp"
            ):

                interpretation = (
                    "Passengers travelling with "
                    "siblings or spouses often also "
                    "travelled with parents or "
                    "children, producing a moderate "
                    "positive correlation between "
                    "sibsp and parch."
                )

            else:

                interpretation = (
                    "The two variables exhibit a "
                    "strong relationship."
                )

            interpretations.append(
                interpretation,
            )

        top_pairs[
            "interpretation"
        ] = interpretations

        logger.info(
            "Top Correlation 1"
        )

        logger.info(
            "Features : %s ↔ %s",
            top_pairs.loc[
                0,
                "feature_1",
            ],
            top_pairs.loc[
                0,
                "feature_2",
            ],
        )

        logger.info(
            "Correlation : %.4f",
            top_pairs.loc[
                0,
                "correlation",
            ],
        )

        logger.info(
            "Interpretation : %s",
            top_pairs.loc[
                0,
                "interpretation",
            ],
        )

        logger.info(
            "-" * 60
        )

        logger.info(
            "Top Correlation 2"
        )

        logger.info(
            "Features : %s ↔ %s",
            top_pairs.loc[
                1,
                "feature_1",
            ],
            top_pairs.loc[
                1,
                "feature_2",
            ],
        )

        logger.info(
            "Correlation : %.4f",
            top_pairs.loc[
                1,
                "correlation",
            ],
        )

        logger.info(
            "Interpretation : %s",
            top_pairs.loc[
                1,
                "interpretation",
            ],
        )

        top_pairs.to_csv(
            REPORTS_DIRECTORY
            / "top_correlations.csv",
            index=False,
            encoding="utf-8-sig",
        )
        