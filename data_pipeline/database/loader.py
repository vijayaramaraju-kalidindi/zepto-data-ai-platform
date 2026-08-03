"""
Database loading service.
"""

from __future__ import annotations

from models.book import Book

from database.database import DatabaseManager


class DatabaseLoader:
    """
    Loads cleaned book data into the SQLite database.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:
        """
        Initialize the database loader.

        Args:
            database: SQLite database manager.
        """

        self.database = database

    def load_data(
        self,
        books: list[Book],
    ) -> None:
        """
        Load all book data into the database.

        Args:
            books: List of cleaned book objects.
        """

        self.insert_categories(books)

        category_mapping = (
            self.get_category_mapping()
        )

        self.insert_books(
            books,
            category_mapping,
        )

        self.database.commit()

    def insert_categories(
        self,
        books: list[Book],
    ) -> None:
        """
        Insert unique categories.

        Args:
            books: List of cleaned books.
        """

        categories = sorted(
            {
                book.category_name
                for book in books
            }
        )

        category_records = [
            (category,)
            for category in categories
        ]

        self.database.executemany(
            """
            INSERT OR IGNORE
            INTO categories
            (
                category_name
            )
            VALUES
            (?);
            """,
            category_records,
        )

    def get_category_mapping(
        self,
    ) -> dict[str, int]:
        """
        Retrieve category mapping.

        Returns:
            Dictionary of
            category_name -> category_id
        """

        self.database.execute(
            """
            SELECT
                category_id,
                category_name
            FROM categories;
            """
        )

        rows = self.database.fetchall()

        return {
            category_name: category_id
            for category_id, category_name in rows
        }

    def insert_books(
        self,
        books: list[Book],
        category_mapping: dict[str, int],
    ) -> None:
        """
        Insert books into SQLite.

        Args:
            books: Cleaned books.
            category_mapping: Category lookup.
        """

        book_records = []

        for book in books:

            book_records.append(
                (
                    book.title,
                    book.price_gbp,
                    book.price_inr,
                    book.rating,
                    int(book.in_stock),
                    category_mapping[
                        book.category_name
                    ],
                )
            )

        self.database.executemany(
            """
            INSERT OR IGNORE
            INTO books
            (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES
            (?, ?, ?, ?, ?, ?);
            """,
            book_records,
        )