"""
Data cleaning service.
"""

from __future__ import annotations

from typing import Any

from models.book import Book
from utils.constants import RATING_MAP
from utils.exceptions import ValidationError


class DataCleaner:
    """
    Cleans and validates scraped book data.
    """

    def clean_books(
        self,
        books: list[dict[str, Any]],
    ) -> list[Book]:
        """
        Clean all scraped books.

        Args:
            books: Raw scraped books.

        Returns:
            List of cleaned Book objects.
        """

        cleaned_books: list[Book] = []

        for book in books:
            cleaned_books.append(
                self.validate_book(book)
            )

        return cleaned_books

    def validate_book(
        self,
        book: dict[str, Any],
    ) -> Book:
        """
        Validate and transform one raw book.

        Args:
            book: Raw scraped book.

        Returns:
            Clean Book object.
        """
        return Book(
            title=book["title"].strip(),
            category_name=book["category"].strip(),
            price_gbp=self.clean_price(book["price"]),
            rating=self.clean_rating(book["star_rating"]),
            in_stock=self.clean_stock(book["availability"]),
        )
        

    @staticmethod
    def clean_price(price: str) -> float:
        """
        Convert price text to float.

        Example:
            £45.17 -> 45.17
        """

        try:
            return float(
                price.replace("£", "").strip()
            )

        except ValueError as exc:
            raise ValidationError(
                f"Invalid price: {price}"
            ) from exc

    @staticmethod
    def clean_rating(rating: str) -> int:
        """
        Convert rating text to integer.

        Example:
            Three -> 3
        """

        try:
            return RATING_MAP[rating]

        except KeyError as exc:
            raise ValidationError(
                f"Invalid rating: {rating}"
            ) from exc

    @staticmethod
    def clean_stock(
        availability: str,
    ) -> bool:
        """
        Convert stock text to boolean.
        """

        return "In stock" in availability