"""
SQLite database service.
"""

from __future__ import annotations

import sqlite3

from config.settings import DATABASE_DIRECTORY, DATABASE_NAME


class DatabaseManager:
    """
    SQLite database manager.
    """

    def __init__(self) -> None:
        """
        Initialize the SQLite database connection.
        """

        DATABASE_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.database_path = (
            DATABASE_DIRECTORY / DATABASE_NAME
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        self.cursor = self.connection.cursor()

    def execute(
        self,
        query: str,
        parameters: tuple = (),
    ) -> None:
        """
        Execute a single SQL statement.

        Args:
            query: SQL query to execute.
            parameters: Query parameters.
        """

        self.cursor.execute(
            query,
            parameters,
        )

    def executemany(
        self,
        query: str,
        parameters: list[tuple],
    ) -> None:
        """
        Execute a SQL statement for multiple records.

        Args:
            query: SQL query to execute.
            parameters: List of query parameters.
        """

        self.cursor.executemany(
            query,
            parameters,
        )

    def fetchone(
        self,
    ) -> tuple | None:
        """
        Fetch a single row.

        Returns:
            One database row or None.
        """

        return self.cursor.fetchone()

    def fetchall(
        self,
    ) -> list[tuple]:
        """
        Fetch all rows.

        Returns:
            List of database rows.
        """

        return self.cursor.fetchall()

    def commit(
        self,
    ) -> None:
        """
        Commit the current transaction.
        """

        self.connection.commit()

    def close(
        self,
    ) -> None:
        """
        Close the database connection.
        """

        self.connection.close()