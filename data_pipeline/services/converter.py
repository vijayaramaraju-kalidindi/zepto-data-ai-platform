"""
Currency conversion service.
"""

from __future__ import annotations

from models.book import Book
from config.settings import GBP_TO_INR_RATE


class CurrencyConverter:
    """
    Converts book prices from GBP to INR.
    """

    def convert_books(
        self,
        books: list[Book],
    ) -> list[Book]:
        """
        Convert all book prices from GBP to INR.

        Args:
            books: List of cleaned Book objects.

        Returns:
            Updated list of Book objects.
        """

        for book in books:

            book.price_inr = self.convert_price(
                book.price_gbp
            )

        return books

    @staticmethod
    def convert_price(
        price_gbp: float,
    ) -> float:
        """
        Convert GBP price to INR.

        Args:
            price_gbp: Price in GBP.

        Returns:
            Price in INR rounded to two decimal places.
        """

        return round(
            price_gbp * GBP_TO_INR_RATE,
            2,
        )