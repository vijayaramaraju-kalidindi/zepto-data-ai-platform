"""
Task A.5 - Multivariate Analysis.

Creates a multivariate data story using
four visualizations that explain who was
more likely to survive and why.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config.logging_config import get_logger
from config.settings import (
    OUTPUTS_DIRECTORY,
    REPORTS_DIRECTORY,
)

logger = get_logger(__name__)


class MultivariateAnalysisService:
    """
    Performs Task A.5.

    Generates four charts together with
    written interpretations that build
    a coherent survival story.
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

        self.story_file = (
            REPORTS_DIRECTORY
            / "multivariate_story.md"
        )

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Execute Task A.5.
        """

        logger.info(
            "Starting Task A.5 - Multivariate Analysis."
        )

        story = []

        story.append(
            self.survival_by_sex_chart(
                dataframe,
            )
        )

        story.append(
            self.survival_by_class_chart(
                dataframe,
            )
        )

        story.append(
            self.age_survival_boxplot(
                dataframe,
            )
        )

        story.append(
            self.fare_age_scatter(
                dataframe,
            )
        )

        self.generate_story(
            story,
        )

        logger.info(
            "Task A.5 completed successfully."
        )
        
    def survival_by_sex_chart(
        self,
        dataframe: pd.DataFrame,
    ) -> str:
        """
        Create survival count by sex chart.

        Returns:
            Markdown interpretation.
        """

        logger.info(
            "Generating Chart 1 - Survival by Sex."
        )

        plot_dataframe = (
            dataframe.groupby(
                [
                    "sex",
                    "survived",
                ]
            )
            .size()
            .reset_index(
                name="count",
            )
        )

        plt.figure(
            figsize=(8, 6),
        )

        sns.barplot(
            data=plot_dataframe,
            x="sex",
            y="count",
            hue="survived",
        )

        plt.title(
            "Survival Count by Sex",
        )

        plt.xlabel(
            "Sex",
        )

        plt.ylabel(
            "Passenger Count",
        )

        plt.legend(
            title="Survived",
            labels=[
                "No",
                "Yes",
            ],
        )

        plt.tight_layout()

        chart_path = (
            self.figure_directory
            / "survival_by_sex.png"
        )

        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Chart 1 saved to %s",
            chart_path,
        )

        interpretation = (
            "## Chart 1 - Survival Count by Sex\n\n"
            "The bar chart shows that female passengers "
            "had a substantially higher number of survivors "
            "than male passengers. In contrast, the number "
            "of male passengers who did not survive is much "
            "greater than the number who survived. This "
            "indicates that passenger sex was strongly "
            "associated with survival outcomes in the "
            "Titanic dataset.\n"
        )

        logger.info(
            "Chart 1 interpretation generated."
        )

        return interpretation
    
    def survival_by_class_chart(
        self,
        dataframe: pd.DataFrame,
    ) -> str:
        """
        Create survival count by passenger class chart.

        Returns:
            Markdown interpretation.
        """

        logger.info(
            "Generating Chart 2 - Survival by Passenger Class."
        )

        plot_dataframe = (
            dataframe.groupby(
                [
                    "pclass",
                    "survived",
                ]
            )
            .size()
            .reset_index(
                name="count",
            )
        )

        plt.figure(
            figsize=(8, 6),
        )

        sns.barplot(
            data=plot_dataframe,
            x="pclass",
            y="count",
            hue="survived",
        )

        plt.title(
            "Survival Count by Passenger Class",
        )

        plt.xlabel(
            "Passenger Class",
        )

        plt.ylabel(
            "Passenger Count",
        )

        plt.legend(
            title="Survived",
            labels=[
                "No",
                "Yes",
            ],
        )

        plt.tight_layout()

        chart_path = (
            self.figure_directory
            / "survival_by_passenger_class.png"
        )

        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Chart 2 saved to %s",
            chart_path,
        )

        interpretation = (
            "## Chart 2 - Survival Count by Passenger Class\n\n"
            "The chart shows clear differences in survival "
            "across passenger classes. First-class passengers "
            "experienced substantially higher survival counts "
            "than passengers travelling in second and third "
            "class. This pattern suggests that passenger class "
            "was strongly associated with survival probability "
            "during the Titanic disaster.\n"
        )

        logger.info(
            "Chart 2 interpretation generated."
        )

        return interpretation
    
    def age_survival_boxplot(
        self,
        dataframe: pd.DataFrame,
    ) -> str:
        """
        Create age distribution box plot
        grouped by survival status.

        Returns:
            Markdown interpretation.
        """

        logger.info(
            "Generating Chart 3 - Age Distribution by Survival."
        )

        plt.figure(
            figsize=(8, 6),
        )

        sns.boxplot(
            data=dataframe,
            x="survived",
            y="age",
        )

        plt.title(
            "Age Distribution by Survival Status",
        )

        plt.xlabel(
            "Survived",
        )

        plt.ylabel(
            "Age",
        )

        plt.xticks(
            ticks=[
                0,
                1,
            ],
            labels=[
                "No",
                "Yes",
            ],
        )

        plt.tight_layout()

        chart_path = (
            self.figure_directory
            / "age_distribution_by_survival.png"
        )

        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Chart 3 saved to %s",
            chart_path,
        )

        survivor_median = (
            dataframe.loc[
                dataframe["survived"] == 1,
                "age",
            ].median()
        )

        non_survivor_median = (
            dataframe.loc[
                dataframe["survived"] == 0,
                "age",
            ].median()
        )

        if survivor_median < non_survivor_median:

            observation = (
                "Survivors had a slightly lower median age "
                "than non-survivors."
            )

        elif survivor_median > non_survivor_median:

            observation = (
                "Survivors had a slightly higher median age "
                "than non-survivors."
            )

        else:

            observation = (
                "Both groups had very similar median ages."
            )

        interpretation = (
            "## Chart 3 - Age Distribution by Survival\n\n"
            "The box plot compares the age distribution of "
            "survivors and non-survivors using their median, "
            "interquartile range and outliers. "
            f"{observation} "
            "Although age shows some variation between the two "
            "groups, the distributions overlap considerably, "
            "suggesting that age alone was not as strong an "
            "indicator of survival as passenger sex or class.\n"
        )

        logger.info(
            "Chart 3 interpretation generated."
        )

        return interpretation
    
    def fare_age_scatter(
        self,
        dataframe: pd.DataFrame,
    ) -> str:
        """
        Create scatter plot showing the
        relationship between fare, age
        and survival.

        Returns:
            Markdown interpretation.
        """

        logger.info(
            "Generating Chart 4 - Fare vs Age by Survival."
        )

        plt.figure(
            figsize=(10, 6),
        )

        sns.scatterplot(
            data=dataframe,
            x="age",
            y="fare",
            hue="survived",
            alpha=0.7,
        )

        plt.title(
            "Fare vs Age by Survival Status",
        )

        plt.xlabel(
            "Age",
        )

        plt.ylabel(
            "Fare",
        )

        plt.legend(
            title="Survived",
            labels=[
                "No",
                "Yes",
            ],
        )

        plt.tight_layout()

        chart_path = (
            self.figure_directory
            / "fare_vs_age_survival.png"
        )

        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Chart 4 saved to %s",
            chart_path,
        )

        average_survivor_fare = (
            dataframe.loc[
                dataframe["survived"] == 1,
                "fare",
            ].mean()
        )

        average_non_survivor_fare = (
            dataframe.loc[
                dataframe["survived"] == 0,
                "fare",
            ].mean()
        )

        if (
            average_survivor_fare
            >
            average_non_survivor_fare
        ):

            fare_observation = (
                "Passengers who survived generally "
                "paid higher fares than those who "
                "did not survive."
            )

        else:

            fare_observation = (
                "Average fare is similar for both "
                "survivors and non-survivors."
            )

        interpretation = (
            "## Chart 4 - Fare vs Age by Survival\n\n"
            "The scatter plot combines age, fare and "
            "survival status to reveal relationships "
            "between multiple variables simultaneously. "
            f"{fare_observation} "
            "The chart also shows that survival cannot "
            "be explained by age alone, as passengers "
            "of different ages appear in both survivor "
            "and non-survivor groups. Together with the "
            "previous charts, this suggests that "
            "passenger sex and class were stronger "
            "indicators of survival than age."
        )

        logger.info(
            "Chart 4 interpretation generated."
        )

        return interpretation
    
    def generate_story(
        self,
        story: list[str],
    ) -> None:
        """
        Generate the multivariate data story
        in Markdown format.

        Args:
            story:
                List containing the written
                interpretations of each chart.
        """

        logger.info(
            "Generating multivariate data story."
        )

        report = (
            "# Task A.5 - Multivariate Data Story\n\n"
            "## Objective\n\n"
            "The following four visualizations collectively "
            "explain which passengers were more likely to "
            "survive the Titanic disaster and identify the "
            "factors most strongly associated with survival.\n\n"
        )

        report += "\n\n---\n\n".join(
            story,
        )

        report += (
            "\n\n---\n\n"
            "## Overall Conclusion\n\n"
            "The four visualizations together indicate that "
            "passenger sex and passenger class were the "
            "strongest factors associated with survival. "
            "Female passengers consistently exhibited much "
            "higher survival rates than male passengers, and "
            "first-class passengers survived more frequently "
            "than those travelling in lower classes. Although "
            "age shows some variation between survivors and "
            "non-survivors, it is not a strong standalone "
            "predictor. Higher fares, which are closely related "
            "to passenger class, were also more common among "
            "survivors, reinforcing the conclusion that class "
            "and sex played the most important roles in survival."
        )

        with open(
            self.story_file,
            mode="w",
            encoding="utf-8",
        ) as file:

            file.write(
                report,
            )

        logger.info(
            "Multivariate story saved to %s",
            self.story_file,
        )