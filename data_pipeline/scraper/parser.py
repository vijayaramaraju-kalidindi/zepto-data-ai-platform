"""
HTML parser for extracting book information from Books to Scrape.
"""

from bs4 import Tag

from utils.exceptions import ParsingError


def parse_book(book_soup: Tag, category: str) -> dict:
    """
    Extract raw book information from a single book card.

    Args:
        book_soup: BeautifulSoup Tag representing one book.
        category: Category name of the book.

    Returns:
        Dictionary containing raw book details.

    Raises:
        ParsingError: If mandatory fields cannot be extracted.
    """

    try:
        title = (
            book_soup.find("h3")
            .find("a")
            .get("title")
            .strip()
        )

        price = (
            book_soup.find("p", class_="price_color")
            .get_text(strip=True)
        )

        rating = (
            book_soup.find("p", class_="star-rating")
            .get("class")[1]
        )

        availability = (
            book_soup.find(
                "p",
                class_="instock availability"
            )
            .get_text(strip=True)
        )

        return {
            "title": title,
            "price": price,
            "star_rating": rating,
            "availability": availability,
            "category": category,
        }

    except (AttributeError, IndexError, TypeError) as exc:
        raise ParsingError(
            f"Unable to parse book information: {exc}"
        ) from exc