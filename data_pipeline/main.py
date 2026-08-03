"""
Entry point for the Data Pipeline.
"""

from dataclasses import asdict
import pandas as pd
from config.logging_config import get_logger
from config.settings import CSV_DIRECTORY
from scraper.scraper import BookScraper
from services.cleaner import DataCleaner
from services.converter import CurrencyConverter
from database.database import DatabaseManager
from database.schema import DatabaseSchema
from database.loader import DatabaseLoader
from database.queries import DatabaseQueries
from database.dataframe_queries import DataFrameQueries

logger = get_logger(__name__)


def main() -> None:
    """
    Execute the data pipeline.
    """

    logger.info(
    "Starting Zepto Data Pipeline..."
)
    
    database = None
    
    try:

        scraper = BookScraper()

        raw_books = scraper.scrape_categories()

        logger.info(
            "Books scraped: %s",
            len(raw_books),
        )

        output_dir = CSV_DIRECTORY

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        raw_books_path = output_dir / "raw_books.csv"

        raw_df = pd.DataFrame(raw_books)

        raw_df.to_csv(
            raw_books_path,
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Raw data saved to %s",
            raw_books_path,
        )

        cleaner = DataCleaner()

        cleaned_books = cleaner.clean_books(raw_books)

        logger.info(
            "Books cleaned: %s",
            len(cleaned_books),
        )

        converter = CurrencyConverter()

        converted_books = converter.convert_books(
            cleaned_books
        )

        logger.info(
            "Currency conversion completed."
        )
        
        cleaned_books_path = output_dir / "cleaned_books.csv"

        cleaned_df = pd.DataFrame(
            [
                asdict(book)
                for book in converted_books
            ]
        )

        cleaned_df.to_csv(
            cleaned_books_path,
            index=False,
            encoding="utf-8-sig",
        )

        logger.info(
            "Cleaned data saved to %s",
            cleaned_books_path,
        )

        logger.info(
            "Books per category:\n%s",
            cleaned_df["category_name"].value_counts(),
    )

        logger.info(
            "Sample cleaned records:\n%s",
            cleaned_df.sample(
                5,
                random_state=42,
            ),
        )

        database = DatabaseManager()
        
        logger.info(
    "Connected to SQLite database."
)
        
        schema = DatabaseSchema(database)

        schema.create_tables()
        logger.info(
    "Database schema created successfully."
)
        
        loader = DatabaseLoader(database)

        loader.load_data(converted_books)

        logger.info(
    "Book data loaded successfully."
)   
        
        queries = DatabaseQueries(database)

        queries.execute_all_queries()
        logger.info(
            "SQL queries executed successfully."
        )
            
        dataframe_queries = DataFrameQueries(
            database
    )

        dataframe_queries.execute_all()

        logger.info(
            "Pandas DataFrame queries completed successfully."
        )
        logger.info(
    "Zepto Data Pipeline completed successfully."
)

    except Exception:

        logger.exception(
            "Data pipeline execution failed."
        )

        raise

    finally:

        if database is not None:

            database.close()

            logger.info(
                "Database connection closed."
            )        
   
if __name__ == "__main__":
    main()