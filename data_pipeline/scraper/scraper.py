"""
Web scraper for Books to Scrape.
"""

from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from config.logging_config import get_logger
from config.settings import BASE_URL, REQUEST_TIMEOUT
from scraper.parser import parse_book
from utils.constants import CATEGORY_URLS
from utils.exceptions import ScrapingError

logger = get_logger(__name__)


class BookScraper:
    """
    Scrapes books from BooksToScrape website.
    """

    def __init__(self) -> None:
        self.session = requests.Session()

    def scrape_categories(self) -> list[dict[str, Any]]:
        """
        Scrape all configured categories.

        Returns:
            List of raw book dictionaries.
        """

        books: list[dict[str, Any]] = []

        for category, relative_url in CATEGORY_URLS.items():
            logger.info("Scraping category: %s", category)
            books.extend(
                self.scrape_category(category, relative_url)
            )

        logger.info("Total books scraped: %s", len(books))

        return books

    def scrape_category(
        self,
        category: str,
        relative_url: str,
    ) -> list[dict[str, Any]]:
        """
        Scrape one category including pagination.

        Args:
            category: Category name.
            relative_url: Relative category URL.

        Returns:
            List of books.
        """

        books: list[dict[str, Any]] = []

        next_page = relative_url

        while next_page:

            soup = self.fetch_page(next_page)

            articles = soup.find_all(
                "article",
                class_="product_pod",
            )

            for article in articles:
                books.append(
                    parse_book(article, category)
                )

            next_button = soup.find(
                "li",
                class_="next",
            )

            if next_button:

                next_href = (
                    next_button.find("a")
                    .get("href")
                )

                next_page = (
                    next_page.rsplit("/", 1)[0]
                    + "/"
                    + next_href
                )

            else:
                next_page = None

        logger.info(
            "%s books collected from %s",
            len(books),
            category,
        )

        return books

    def fetch_page(
        self,
        relative_url: str,
    ) -> BeautifulSoup:
        """
        Download one page.

        Args:
            relative_url: Relative page URL.

        Returns:
            BeautifulSoup object.

        Raises:
            ScrapingError: If the page cannot be downloaded.
        """

        url = BASE_URL + relative_url

        try:

            response = self.session.get(
                url,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            return BeautifulSoup(
                response.content,
                "html.parser",
            )

        except requests.RequestException as exc:

            logger.exception(
                "Failed downloading %s",
                url,
            )

            raise ScrapingError(
                f"Unable to download {url}"
            ) from exc