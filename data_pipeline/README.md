# Data Engineering Pipeline

## Project Overview

The Data Engineering Pipeline is the first module of the **Zepto Data & AI Platform**. It is responsible for collecting raw book data from a public website, cleaning and transforming the data, loading it into a normalized SQLite database, and validating the stored data using SQL and Pandas.

The pipeline follows a production-oriented ETL (Extract, Transform, Load) workflow and demonstrates software engineering best practices such as modular architecture, logging, exception handling, type hints, reusable services, and configuration management.

---

# Architecture

```
                   +----------------------+
                   |  BooksToScrape Site  |
                   +----------+-----------+
                              |
                              v
                     Web Scraper (Requests +
                     BeautifulSoup)
                              |
                              v
                     Raw Book Records
                              |
                              v
                     Data Cleaning
                              |
                              v
                 Currency Conversion (GBP → INR)
                              |
                              v
                     Cleaned Book Objects
                              |
                              v
                    SQLite Database (Normalized)
                              |
               +--------------+--------------+
               |                             |
               v                             v
          SQL Queries                 Pandas Validation
               |                             |
               +--------------+--------------+
                              |
                              v
                        CSV Result Files
```

---

# Folder Structure

```text
data_pipeline/
│
├── config/
├── database/
├── models/
├── outputs/
│   ├── csv/
│   ├── database/
│   ├── dataframe_results/
│   └── sql_results/
├── scraper/
├── services/
├── utils/
├── .env
├── main.py
└── README.md
```

---

# Technologies Used

- Python 3.13
- Requests
- BeautifulSoup4
- Pandas
- SQLite (`sqlite3`)
- python-dotenv
- Logging
- Dataclasses

---

# ETL Workflow

## Extract

- Scrapes books from **BooksToScrape**
- Extracts:
  - Title
  - Price
  - Rating
  - Availability
  - Category

Categories scraped:

- Travel
- Mystery
- Historical Fiction

Total books collected:

- **69**

---

## Transform

The cleaning stage performs:

- Removes currency symbols
- Converts price to float
- Converts star rating to integer
- Converts stock availability to Boolean
- Converts GBP to INR using a fixed conversion rate
- Validates records before loading

---

## Load

The cleaned data is loaded into a normalized SQLite database.

Database contains two tables.

### Categories

| Column | Type |
|---------|------|
| category_id | INTEGER PRIMARY KEY |
| category_name | TEXT UNIQUE |

### Books

| Column | Type |
|---------|------|
| book_id | INTEGER PRIMARY KEY |
| title | TEXT UNIQUE |
| price_gbp | REAL |
| price_inr | REAL |
| rating | INTEGER |
| in_stock | INTEGER |
| category_id | INTEGER (Foreign Key) |

---

# SQL Queries

The pipeline executes SQL queries demonstrating:

- SELECT
- WHERE
- ORDER BY
- LIMIT
- DISTINCT
- IN
- INNER JOIN

Results are exported to:

```text
outputs/sql_results/
```

---

# Pandas Validation

The pipeline demonstrates:

- `pd.read_sql_query()`
- `pd.merge()`

The SQL JOIN result is compared against the Pandas merge result to verify both produce identical outputs.

---

# Output Files

```text
outputs/

csv/
    raw_books.csv
    cleaned_books.csv

database/
    books.db

sql_results/
    average_price_by_category.csv
    books_price_range.csv
    distinct_categories.csv
    high_rated_books.csv
    top_10_highest_rated_books.csv

dataframe_results/
    books_dataframe.csv
    categories_dataframe.csv
    books_with_categories.csv
```

---

# Installation

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Configuration

Configuration values are stored in the `.env` file.

Example:

```text
BASE_URL=https://books.toscrape.com/
GBP_TO_INR_RATE=105.50
REQUEST_TIMEOUT=30
```

---

# Execution

Run the pipeline from the repository root.

```bash
python data_pipeline/main.py
```

---

## Logging

The pipeline uses Python's built-in `logging` module to record execution details.

Log messages are written to both:

- Console
- `outputs/logs/application.log`

The log captures each stage of the ETL workflow, including:

- Pipeline startup
- Web scraping progress
- Data cleaning
- Currency conversion
- SQLite schema creation
- Database loading
- SQL query execution
- Pandas validation
- Pipeline completion
- Error details (if any)

# Sample Log Output

```text
2026-08-03 18:06:47 | INFO | Starting Zepto Data Pipeline...
2026-08-03 18:06:51 | INFO | Books scraped: 69
2026-08-03 18:06:51 | INFO | Books cleaned: 69
2026-08-03 18:06:51 | INFO | Currency conversion completed.
2026-08-03 18:06:51 | INFO | Connected to SQLite database.
2026-08-03 18:06:51 | INFO | Database schema created successfully.
2026-08-03 18:06:51 | INFO | Book data loaded successfully.
2026-08-03 18:06:51 | INFO | SQL queries executed successfully.
2026-08-03 18:06:51 | INFO | SQL JOIN and pandas merge produced identical results.
2026-08-03 18:06:51 | INFO | Zepto Data Pipeline completed successfully.
2026-08-03 18:06:51 | INFO | Database connection closed.
```

---

# Design Decisions

The project was designed with modularity and maintainability in mind.

Key decisions include:

- Separation of concerns using dedicated service classes.
- SQLite normalization using separate Books and Categories tables.
- Configuration through environment variables.
- Centralized logging.
- Reusable database abstraction.
- Validation before database insertion.
- Idempotent data loading using `INSERT OR IGNORE`.
- Verification of SQL JOIN using Pandas merge.

---

# Challenges

- Handling pagination while scraping.
- Cleaning inconsistent price and rating formats.
- Preventing duplicate records during repeated ETL executions.
- Designing a normalized relational schema.
- Keeping SQL and Pandas implementations consistent.

---

# Future Improvements

- Configurable category selection.
- Parallel scraping for improved performance.
- Automated unit and integration testing.
- Scheduled ETL execution.
- Support for PostgreSQL and MySQL.
- Cloud deployment using Docker and CI/CD.
- Real-time currency conversion using an external API.

---

# Author

Developed as part of the **Zepto Data & AI Platform** capstone project.
