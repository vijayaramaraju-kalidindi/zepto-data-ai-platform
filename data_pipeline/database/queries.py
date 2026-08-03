"""
Database query service.
"""

from __future__ import annotations

import pandas as pd

from config.settings import OUTPUTS_DIRECTORY
from database.database import DatabaseManager


class DatabaseQueries:
    """
    Executes SQL queries and exports the results.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:
        """
        Initialize the query service.

        Args:
            database: SQLite database manager.
        """

        self.database = database

        self.output_directory = (
            OUTPUTS_DIRECTORY / "sql_results"
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def execute_all_queries(
        self,
    ) -> None:
        """
        Execute all required SQL queries.
        """

        self.top_ten_highest_rated_books()

        self.high_rated_books()

        self.books_in_price_range()

        self.distinct_categories()

        self.average_price_by_category()

    def top_ten_highest_rated_books(
        self,
    ) -> None:
        """
        Top 10 highest-rated books.
        Demonstrates:
        SELECT, ORDER BY, LIMIT.
        """

        query = """
        SELECT
            title,
            rating,
            price_inr
        FROM books
        ORDER BY
            rating DESC,
            price_inr DESC
        LIMIT 10;
        """

        self.export_query(
            query,
            "top_10_highest_rated_books.csv",
        )

    def high_rated_books(
        self,
    ) -> None:
        """
        Books having rating 4 or 5.
        Demonstrates:
        WHERE, IN.
        """

        query = """
        SELECT
            title,
            rating,
            price_inr
        FROM books
        WHERE rating IN (4, 5)
        ORDER BY
            rating DESC,
            price_inr DESC;
        """

        self.export_query(
            query,
            "high_rated_books.csv",
        )

    def books_in_price_range(
        self,
    ) -> None:
        """
        Books priced between ₹3000 and ₹5000.
        Demonstrates:
        BETWEEN.
        """

        query = """
        SELECT
            title,
            price_inr
        FROM books
        WHERE price_inr
        BETWEEN 3000
        AND 5000
        ORDER BY
            price_inr DESC;
        """

        self.export_query(
            query,
            "books_price_range.csv",
        )

    def distinct_categories(
        self,
    ) -> None:
        """
        List unique categories.
        Demonstrates:
        DISTINCT.
        """

        query = """
        SELECT DISTINCT
            category_name
        FROM categories
        ORDER BY
            category_name;
        """

        self.export_query(
            query,
            "distinct_categories.csv",
        )

    def average_price_by_category(
        self,
    ) -> None:
        """
        Average INR price by category.
        Demonstrates:
        JOIN.
        """

        query = """
        SELECT
            c.category_name,
            COUNT(*) AS total_books,
            ROUND(
                AVG(
                    b.price_inr
                ),
                2
            ) AS average_price_inr
        FROM books b
        INNER JOIN categories c
            ON b.category_id = c.category_id
        GROUP BY
            c.category_name
        ORDER BY
            average_price_inr DESC;
        """

        self.export_query(
            query,
            "average_price_by_category.csv",
        )

    def export_query(
        self,
        query: str,
        output_file: str,
    ) -> None:
        """
        Execute a SQL query and save the
        result to a CSV file.

        Args:
            query: SQL query.
            output_file: CSV filename.
        """

        dataframe = pd.read_sql_query(
            query,
            self.database.connection,
        )

        dataframe.to_csv(
            self.output_directory / output_file,
            index=False,
            encoding="utf-8-sig",
        )