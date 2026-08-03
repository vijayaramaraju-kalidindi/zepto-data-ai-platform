# Zepto Data & AI Platform

## Project Overview

The **Zepto Data & AI Platform** is an end-to-end Artificial Intelligence and Machine Learning platform developed as part of the AI & Machine Learning Capstone Project.

The platform demonstrates the complete AI lifecycle, beginning with raw data collection and progressing through data engineering, analytics, machine learning, and Generative AI deployment.

The project has been designed using production-oriented software engineering principles, including modular architecture, reusable components, configuration management, logging, exception handling, documentation, and scalable project organization.

---

# Overall Architecture

```text
                    +----------------------+
                    |   Raw Data Sources   |
                    +----------+-----------+
                               |
                               v
                  Module 1 : Data Pipeline
          Web Scraping • ETL • SQLite • SQL
                               |
                               v
                 Cleaned & Structured Data
                               |
                               v
               Module 2 : Analytics Pipeline
       EDA • Feature Engineering • Machine Learning
                               |
                               v
                  Trained ML Models & Insights
                               |
                               v
            Module 3 : GenAI Support Assistant
      ChromaDB • LangGraph • FastAPI • Docker
                               |
                               v
                 AI-powered Question Answering
```

---

# Repository Structure

```text
zepto-data-ai-platform/
│
├── analytics/
│
├── data_pipeline/
│
├── support_assistant/
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

---

# Modules

## Module 1 – Data Engineering Pipeline

**Status:** ✅ Completed

Responsible for:

- Web scraping
- Data cleaning
- Data validation
- Currency conversion
- SQLite normalization
- SQL queries
- Pandas validation

Outputs:

- Raw CSV
- Cleaned CSV
- SQLite database
- SQL query results
- Pandas validation results

Module documentation:

```text
data_pipeline/README.md
```

---

## Module 2 – Analytics Pipeline

**Status:** 🚧 Planned

This module will perform exploratory data analysis and machine learning using the cleaned datasets.

Planned responsibilities include:

- Exploratory Data Analysis (EDA)
- Data preprocessing
- Feature engineering
- Classification
- Regression
- Hyperparameter tuning
- Model comparison
- Model serialization
- Business recommendations

---

## Module 3 – GenAI Support Assistant

**Status:** 🚧 Planned

This module will implement an AI-powered customer support assistant using Retrieval-Augmented Generation (RAG).

Planned responsibilities include:

- Document ingestion
- Embedding generation
- ChromaDB vector database
- LangGraph workflow
- Intent routing
- FastAPI deployment
- Docker containerization
- Offline deterministic mode
- Optional LLM integration

---

# Technologies Used

## Programming Language

- Python 3.13

## Data Engineering

- Requests
- BeautifulSoup4
- Pandas
- SQLite (`sqlite3`)

## Machine Learning

- Scikit-learn
- NumPy
- Matplotlib
- Seaborn
- Imbalanced-learn (SMOTE)

## Generative AI

- LangChain
- LangGraph
- ChromaDB
- FastAPI
- Pydantic

## Development Tools

- VS Code
- Git
- GitHub
- Docker

---

# Engineering Principles

The project follows modern software engineering practices:

- Modular architecture
- Separation of concerns
- Object-oriented design
- Type hints
- Comprehensive docstrings
- Centralized logging
- Exception handling
- Environment variable configuration
- Reusable utility functions
- Layered project structure

---

# Project Workflow

```text
Raw Data
    │
    ▼
Data Engineering
    │
    ▼
Structured Database
    │
    ▼
Analytics & Machine Learning
    │
    ▼
Model Artifacts
    │
    ▼
GenAI Support Assistant
    │
    ▼
REST API Deployment
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd zepto-data-ai-platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Modules

## Module 1

```bash
python data_pipeline/main.py
```

## Module 2

To be implemented.

## Module 3

To be implemented.

---

# Current Project Status

| Module | Status |
|---------|--------|
| Data Engineering Pipeline | ✅ Completed |
| Analytics Pipeline | 🚧 In Progress |
| GenAI Support Assistant | 🚧 Planned |

---

# Future Enhancements

- PostgreSQL support
- Cloud deployment
- CI/CD pipelines
- Automated testing
- Docker Compose deployment
- Kubernetes deployment
- Real-time data ingestion
- External currency exchange API integration

---

# Author

Developed as part of the **AI & Machine Learning Capstone Project** for the **Zepto Data & AI Platform**.

---

# License

This project is intended for educational purposes as part of the AI & Machine Learning Capstone Project.