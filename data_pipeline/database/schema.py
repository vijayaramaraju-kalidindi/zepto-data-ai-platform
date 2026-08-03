"""
Database schema creation.
"""

from database.database import DatabaseManager


class DatabaseSchema:
    """
    Creates the SQLite database schema.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:

        self.database = database

    def create_tables(self) -> None:
        """
        Create all required database tables.
        """

        self.create_categories_table()

        self.create_books_table()

        self.database.commit()

    def create_categories_table(self) -> None:
        """
        Create categories table.
        """

        self.database.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories
            (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE
            );
            """
        )

    def create_books_table(self) -> None:
        """
        Create books table.
        """

        self.database.execute(
            """
            CREATE TABLE IF NOT EXISTS books
            (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL UNIQUE,

                price_gbp REAL NOT NULL,

                price_inr REAL NOT NULL,

                rating INTEGER NOT NULL,

                in_stock INTEGER NOT NULL,

                category_id INTEGER NOT NULL,

                FOREIGN KEY(category_id)
                REFERENCES categories(category_id)
            );
            """
        )