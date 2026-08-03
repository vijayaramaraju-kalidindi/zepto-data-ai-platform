"""
Pandas DataFrame operations using SQLite.
"""

from __future__ import annotations
import pandas as pd
from config.settings import OUTPUTS_DIRECTORY
from database.database import DatabaseManager
from config.logging_config import get_logger

logger = get_logger(__name__)

class DataFrameQueries:
    """
    Demonstrates pandas read_sql_query()
    and pd.merge() using SQLite tables.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:
        """
        Initialize DataFrame query service.

        Args:
            database: SQLite database manager.
        """

        self.database = database

        self.output_directory = (
            OUTPUTS_DIRECTORY / "dataframe_results"
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def execute_all(
        self,
    ) -> None:
        """
        Execute all pandas-based tasks.
        """

        self.read_books()

        self.read_categories()

        self.merge_tables()

    def read_books(
        self,
    ) -> None:
        """
        Read books table using pandas.
        """

        books_df = pd.read_sql_query(
            """
            SELECT *
            FROM books;
            """,
            self.database.connection,
        )

        books_df.to_csv(
            self.output_directory / "books_dataframe.csv",
            index=False,
            encoding="utf-8-sig",
        )

    def read_categories(
        self,
    ) -> None:
        """
        Read categories table using pandas.
        """

        categories_df = pd.read_sql_query(
            """
            SELECT *
            FROM categories;
            """,
            self.database.connection,
        )

        categories_df.to_csv(
            self.output_directory / "categories_dataframe.csv",
            index=False,
            encoding="utf-8-sig",
        )

    def merge_tables(
        self,
    ) -> None:
        """
        Reproduce SQL JOIN using pandas merge().
        """

        books_df = pd.read_sql_query(
            """
            SELECT *
            FROM books;
            """,
            self.database.connection,
        )

        categories_df = pd.read_sql_query(
            """
            SELECT *
            FROM categories;
            """,
            self.database.connection,
        )

        merged_df = pd.merge(
            books_df,
            categories_df,
            on="category_id",
            how="inner",
        )
 
        sql_join_df = pd.read_sql_query(
            """
            SELECT
                b.book_id,
                b.title,
                b.price_gbp,
                b.price_inr,
                b.rating,
                b.in_stock,
                b.category_id,
                c.category_name
            FROM books b
            INNER JOIN categories c
                ON b.category_id = c.category_id
            ORDER BY
                b.book_id;
            """,
                    self.database.connection,
        )       
 

        merged_df = merged_df.sort_values(
            by="book_id"
        ).reset_index(
        drop=True
)

        sql_join_df = sql_join_df.reset_index(
        drop=True
)
        assert sql_join_df.equals(
           merged_df
        ), (
            "SQL JOIN result does not match "
            "pandas merge result."
        )

        logger.info(
            "SQL JOIN and pandas merge "
            "produced identical results."
)

        merged_df.to_csv(
            self.output_directory / "books_with_categories.csv",
            index=False,
            encoding="utf-8-sig",
        )