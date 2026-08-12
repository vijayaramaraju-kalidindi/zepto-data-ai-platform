# Zepto Data & AI Platform

## Project Overview

The **Zepto Data & AI Platform** is an end-to-end Artificial Intelligence and Machine Learning platform developed as part of the **AI & Machine Learning Capstone Project**.

The platform demonstrates the complete AI lifecycle, beginning with raw data collection and progressing through data engineering, analytics, machine learning, and Generative AI deployment.

The project is designed using production-oriented software engineering principles, including:

* Modular architecture
* Separation of concerns
* Reusable components
* Configuration management
* Centralized logging
* Exception handling
* Type hints
* Documentation
* API-based deployment
* Containerization
* Scalable project organization

The platform is divided into three major modules:

1. **Module 1: Data Engineering Pipeline**
2. **Module 2: Analytics & Machine Learning Pipeline**
3. **Module 3: GenAI Support Assistant**

---

# Overall Architecture

```text
                    +----------------------+
                    |   Raw Data Sources   |
                    +----------+-----------+
                               |
                               v
                  +------------------------+
                  | Module 1               |
                  | Data Engineering       |
                  |                        |
                  | Web Scraping           |
                  | Data Cleaning          |
                  | Validation             |
                  | Currency Conversion    |
                  | SQLite                 |
                  | SQL / Pandas           |
                  +----------+-------------+
                             |
                             v
                  Cleaned & Structured Data
                             |
                             v
                  +------------------------+
                  | Module 2               |
                  | Analytics & ML         |
                  |                        |
                  | EDA                    |
                  | Preprocessing          |
                  | Feature Engineering    |
                  | Classification         |
                  | Regression             |
                  | Model Evaluation       |
                  | Model Selection        |
                  | Model Serialization    |
                  +----------+-------------+
                             |
                             v
                    ML Models & Insights
                             |
                             v
                  +------------------------+
                  | Module 3               |
                  | GenAI Support Assistant|
                  |                        |
                  | Document Ingestion     |
                  | Embeddings             |
                  | ChromaDB               |
                  | Retrieval              |
                  | LangGraph              |
                  | Intent Routing         |
                  | Mock / Optional LLM    |
                  | FastAPI                |
                  | Docker                 |
                  +----------+-------------+
                             |
                             v
                    AI-powered Question
                         Answering
```

---

# Repository Structure

```text
zepto-data-ai-platform/
│
├── analytics/
│   ├── ...
│   └── README.md
│
├── data_pipeline/
│   ├── ...
│   └── README.md
│
├── support_assistant/
│   ├── ...
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

Each module has its own README containing implementation-level documentation.

---

# Module 1: Data Engineering Pipeline

**Status:** ✅ Completed

The Data Engineering Pipeline is responsible for collecting, cleaning, validating, transforming, and storing the source data.

The pipeline follows a complete ETL workflow:

```text
Web Source
    |
    v
Web Scraping
    |
    v
Raw CSV
    |
    v
Data Cleaning
    |
    v
Currency Conversion
    |
    v
Validation
    |
    v
SQLite Database
    |
    +----------------+
    |                |
    v                v
 SQL Queries     Pandas Validation
```

## Responsibilities

* Web scraping
* Raw data extraction
* Data cleaning
* Data validation
* Currency conversion
* SQLite database creation
* Database normalization
* SQL query execution
* Pandas-based validation
* Logging
* Exception handling

## Implementation

The pipeline is organized into reusable components including:

* `BookScraper`
* `DataCleaner`
* `CurrencyConverter`
* `DatabaseManager`
* Database schema and loader components
* SQL query components
* Pandas DataFrame query and validation components

The `main.py` module acts as the orchestration layer and coordinates the complete pipeline using structured error handling and cleanup.

## Final Execution

The completed pipeline successfully processed **69 books** across the following categories:

| Category           |  Books |
| ------------------ | -----: |
| Travel             |     11 |
| Mystery            |     32 |
| Historical Fiction |     26 |
| **Total**          | **69** |

The pipeline successfully generated:

* Raw CSV data
* Cleaned CSV data
* Normalized SQLite database
* SQL query results
* Pandas validation results
* Application logs

Logs are generated under:

```text
outputs/logs/application.log
```

Generated outputs and runtime logs are excluded from Git where appropriate.

## Module Documentation

Detailed implementation documentation is available in:

```text
data_pipeline/README.md
```

---

# Module 2: Analytics & Machine Learning Pipeline

**Status:** ✅ Completed

Module 2 builds the analytics and machine learning layer on top of the cleaned and structured data produced by Module 1.

The objective is to demonstrate the complete machine learning workflow from exploratory analysis through model training, evaluation, comparison, and serialization.

## Analytics Workflow

```text
Cleaned Data
     |
     v
Data Loading
     |
     v
Exploratory Data Analysis
     |
     v
Data Preprocessing
     |
     v
Feature Engineering
     |
     v
Train / Test Split
     |
     +--------------------+
     |                    |
     v                    v
Classification        Regression
     |                    |
     v                    v
Model Training        Model Training
     |                    |
     +---------+----------+
               |
               v
       Model Evaluation
               |
               v
      Model Comparison
               |
               v
       Hyperparameter
          Tuning
               |
               v
       Final Model
               |
               v
     Model Serialization
```

## Responsibilities

Module 2 is designed to cover:

* Exploratory Data Analysis
* Statistical analysis
* Data preprocessing
* Missing-value handling
* Feature engineering
* Feature selection
* Train/test dataset preparation
* Classification
* Regression
* Model evaluation
* Hyperparameter tuning
* Model comparison
* Handling class imbalance
* Model serialization
* Business-oriented interpretation of model results

## Machine Learning Technologies

The analytics layer uses:

* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Imbalanced-learn
* SMOTE

## Classification

The classification workflow evaluates suitable classification algorithms against the prepared dataset.

The workflow includes:

```text
Dataset
   |
   v
Preprocessing
   |
   v
Feature Engineering
   |
   v
Class Distribution Analysis
   |
   v
SMOTE / Imbalance Handling
   |
   v
Classification Models
   |
   v
Evaluation
   |
   v
Model Comparison
   |
   v
Best Model
```

Evaluation is based on appropriate classification metrics rather than accuracy alone, particularly where class imbalance is present.

## Regression

The regression workflow follows:

```text
Dataset
   |
   v
Feature Preparation
   |
   v
Train/Test Split
   |
   v
Regression Models
   |
   v
Prediction
   |
   v
Regression Metrics
   |
   v
Model Comparison
```

Appropriate regression metrics are used to understand prediction performance.

## Model Selection

The final model selection process considers:

* Model performance
* Generalization capability
* Evaluation metrics
* Hyperparameter performance
* Complexity
* Business relevance

The selected model can then be serialized for downstream usage.

## Module Documentation

Detailed analytics implementation and experiment documentation is maintained under:

```text
analytics/README.md
```

---

# Module 3: GenAI Support Assistant

**Status:** ✅ Completed

Module 3 implements an AI-powered customer support assistant using a **Retrieval-Augmented Generation (RAG)** architecture.

The assistant combines:

* Document ingestion
* Text embeddings
* Vector storage
* Semantic retrieval
* Intent classification
* LangGraph orchestration
* Answer generation
* Pydantic response validation
* FastAPI REST API
* Docker containerization

The implementation also provides an **offline deterministic/mock LLM mode** so that the complete workflow can be demonstrated without depending on an external LLM service.

---

# Module 3 Architecture

The implemented RAG architecture follows:

```text
                 Support Documents
                        |
                        v
                Document Ingestion
                        |
                        v
                 Text Processing
                        |
                        v
                  Embeddings
                        |
                        v
              all-MiniLM-L6-v2
                        |
                        v
                  ChromaDB
                        |
                        |
User Question ----------+
        |
        v
   FastAPI /ask
        |
        v
   LangGraph Workflow
        |
        v
  Intent Classification
        |
        +-----------------------------+
        |                             |
        v                             v
Direct Answer                  RAG Retrieval
        |                             |
        |                             v
        |                       ChromaDB
        |                             |
        |                             v
        |                       Top-3 Results
        |                             |
        |                             v
        |                       Answer Generation
        |                             |
        +--------------+--------------+
                       |
                       v
                Pydantic Response
                       |
                       v
                    JSON API
```

---

# Document Ingestion

The support assistant uses a controlled support-document corpus consisting of **8 documents**.

The documents are processed during ingestion and converted into vector embeddings.

The embedding model used is:

```text
all-MiniLM-L6-v2
```

The generated embeddings are stored in ChromaDB.

The vector database collection is:

```text
support_assistant
```

---

# Vector Database

**ChromaDB** is used as the vector store for semantic document retrieval.

The workflow is:

```text
Support Document
      |
      v
Text Chunk
      |
      v
Embedding Model
      |
      v
Vector
      |
      v
ChromaDB
```

At query time:

```text
User Question
      |
      v
Question Embedding
      |
      v
ChromaDB Similarity Search
      |
      v
Top 3 Relevant Documents
```

The implementation uses **top-3 retrieval** to provide relevant context to the answer-generation stage.

---

# LangGraph Workflow

The support assistant uses LangGraph to orchestrate the processing workflow.

The implemented graph contains the following logical nodes:

```text
                 User Question
                       |
                       v
               classify_intent
                       |
             +---------+---------+
             |                   |
             v                   v
      direct_answer      retrieve_and_answer
             |                   |
             |                   v
             |             ChromaDB Search
             |                   |
             |                   v
             |              Top-3 Context
             |                   |
             |                   v
             |            Answer Generation
             |                   |
             +---------+---------+
                       |
                       v
                 Final Response
```

## `classify_intent`

Determines how the incoming question should be processed.

The workflow can route the request toward either:

* Direct answer processing
* Retrieval-augmented answer processing

## `retrieve_and_answer`

This path:

1. Converts the question into an embedding
2. Searches ChromaDB
3. Retrieves the most relevant support documents
4. Uses the retrieved context to generate the response
5. Returns the answer together with retrieval information

## `direct_answer`

Handles questions that do not require retrieval from the support knowledge base.

---

# Offline Deterministic Mode

The support assistant includes a configurable mock/offline execution mode.

The behavior is controlled using:

```text
MOCK_LLM
```

This allows the complete application workflow to be demonstrated without requiring an external LLM service.

The architecture therefore supports:

```text
                  User Question
                       |
                       v
                Intent Routing
                       |
             +---------+---------+
             |                   |
             v                   v
          Direct              RAG
             |                   |
             +---------+---------+
                       |
                       v
                 MOCK_LLM Branch
                       |
                       v
              Deterministic Answer
```

This is particularly useful for:

* Offline demonstrations
* Automated testing
* Reproducible evaluation
* Development environments
* Environments without external LLM credentials

---

# Support Assistant Services

The implementation follows a service-oriented structure.

Key services include:

```text
embedding_service.py
vector_store.py
retrieval_service.py
graph_service.py
```

### `embedding_service.py`

Responsible for generating embeddings using:

```text
all-MiniLM-L6-v2
```

### `vector_store.py`

Responsible for ChromaDB interaction and vector collection management.

### `retrieval_service.py`

Responsible for semantic search and retrieval of relevant support documents.

The configured retrieval depth is:

```text
Top K = 3
```

### `graph_service.py`

Responsible for constructing and executing the LangGraph workflow.

---

# API Layer

The GenAI assistant is exposed through **FastAPI**.

The primary endpoint is:

```text
POST /ask
```

A typical request is:

```json
{
  "question": "How can I return an order?"
}
```

The API processes the question through the LangGraph workflow and returns a structured response.

The response is validated using **Pydantic** models.

The response structure includes:

```text
answer
sources
confidence
```

This provides a consistent API contract between the GenAI service and consuming applications.

---

# RAG Response Flow

A typical RAG request follows:

```text
POST /ask
    |
    v
Pydantic Request Validation
    |
    v
LangGraph
    |
    v
Intent Classification
    |
    v
Retrieval Decision
    |
    v
Question Embedding
    |
    v
ChromaDB
    |
    v
Top-3 Relevant Documents
    |
    v
Context Construction
    |
    v
Answer Generation
    |
    v
Pydantic Response Validation
    |
    v
JSON Response
```

---

# Docker Deployment

The support assistant is containerized using Docker.

The container packages the application and its runtime dependencies so that the service can be deployed consistently across environments.

The Module 3 implementation includes a:

```text
Dockerfile
```

The intended deployment model is:

```text
                  Docker Container
              +----------------------+
              | FastAPI Application  |
              |                      |
              | LangGraph            |
              | Retrieval            |
              | ChromaDB              |
              | Embeddings            |
              | Pydantic             |
              +----------+-----------+
                         |
                         v
                    REST API
```

---

# Module 3 Design Principles

The GenAI module follows several production-oriented principles:

* Separation of embedding and retrieval responsibilities
* Service-oriented architecture
* Explicit workflow orchestration
* Structured API contracts
* Pydantic validation
* Configurable mock LLM mode
* Vector database abstraction
* Containerized deployment
* Deterministic offline execution
* Clear separation between retrieval and generation

---

# Technology Stack

## Programming Language

```text
Python 3.13
```

## Data Engineering

* Requests
* BeautifulSoup4
* Pandas
* SQLite

## Machine Learning

* Scikit-learn
* NumPy
* Matplotlib
* Seaborn
* Imbalanced-learn
* SMOTE

## Generative AI

* LangChain
* LangGraph
* ChromaDB
* Sentence Transformers
* `all-MiniLM-L6-v2`

## API

* FastAPI
* Pydantic

## Deployment

* Docker

## Development Tools

* VS Code
* Git
* GitHub
* Docker

---

# Engineering Principles

The complete platform follows modern software engineering practices.

### Modular Architecture

Each major capability is isolated into its own module.

```text
data_pipeline/
analytics/
support_assistant/
```

### Separation of Concerns

Data ingestion, processing, analytics, retrieval, orchestration, and API responsibilities are separated into independent components.

### Reusable Components

Services and utilities are designed to be reusable rather than embedding all functionality inside a single script.

### Type Safety

Type hints and Pydantic models are used where appropriate.

### Logging

Application-level logging is implemented to make pipeline execution and failures easier to diagnose.

### Exception Handling

Critical execution paths include exception handling and cleanup.

### Configuration

Environment variables are used where runtime configuration is required.

### Containerization

The GenAI support assistant is packaged as a Docker container for consistent deployment.

---

# End-to-End Project Workflow

The complete project can be viewed as the following lifecycle:

```text
                    RAW DATA
                       |
                       v
              +----------------+
              |    Module 1    |
              | Data Engineering|
              +-------+--------+
                      |
                      v
             Cleaned Structured Data
                      |
                      v
              +----------------+
              |    Module 2    |
              | Analytics & ML |
              +-------+--------+
                      |
                      v
                ML Models
                & Insights
                      |
                      v
              +----------------+
              |    Module 3    |
              |     GenAI      |
              | Support Assistant|
              +-------+--------+
                      |
                      v
              Retrieval + Generation
                      |
                      v
                  FastAPI
                      |
                      v
              Docker Deployment
                      |
                      v
              AI-powered Support
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

Run the completed data engineering pipeline:

```bash
python data_pipeline/main.py
```

The pipeline performs the complete extraction, transformation, validation, and database loading workflow.

---

## Module 2

The analytics module is developed independently under:

```text
analytics/
```

The module is intended to execute the EDA and machine learning workflow using the structured data generated by Module 1.

Refer to:

```text
analytics/README.md
```

for module-specific execution instructions.

---

## Module 3

The GenAI Support Assistant is located under:

```text
support_assistant/
```

The module provides:

* Document ingestion
* Embedding generation
* ChromaDB storage
* Semantic retrieval
* LangGraph orchestration
* Intent routing
* Mock LLM execution
* FastAPI REST API
* Docker deployment

Refer to:

```text
support_assistant/README.md
```

for detailed setup and execution instructions.

---

# Project Status

| Module                            | Status         | Key Deliverables                                                                       |
| --------------------------------- | -------------- | -------------------------------------------------------------------------------------- |
| Module 1: Data Engineering        | ✅ Completed    | Scraping, cleaning, validation, currency conversion, SQLite, SQL, Pandas               |
| Module 2: Analytics & ML          | ✅ Completed    | EDA, preprocessing, feature engineering, classification, regression, evaluation        |
| Module 3: GenAI Support Assistant | ✅ Completed    | RAG, ChromaDB, LangGraph, intent routing, FastAPI, Pydantic, Docker, offline/mock mode |

---

# Key Project Outcomes

The platform demonstrates a progression from traditional data engineering to modern AI application development.

### Module 1 demonstrates

```text
Raw Web Data
    ↓
ETL
    ↓
Data Quality
    ↓
Structured Database
    ↓
SQL / Pandas Analytics
```

### Module 2 demonstrates

```text
Structured Data
    ↓
EDA
    ↓
Feature Engineering
    ↓
Machine Learning
    ↓
Model Evaluation
    ↓
Model Artifacts
```

### Module 3 demonstrates

```text
Knowledge Documents
    ↓
Embeddings
    ↓
Vector Database
    ↓
Semantic Retrieval
    ↓
LangGraph
    ↓
Answer Generation
    ↓
FastAPI
    ↓
Docker
```

Together, the three modules demonstrate an end-to-end AI/ML application lifecycle.

---

# Future Enhancements

The following capabilities can be considered for future iterations of the platform:

* PostgreSQL support
* Cloud deployment
* CI/CD pipelines
* Automated unit and integration testing
* Docker Compose deployment
* Kubernetes deployment
* Real-time data ingestion
* External currency exchange API integration
* Production-grade external LLM integration
* Monitoring and observability
* Authentication and authorization
* API rate limiting
* Production vector database scaling

---

# Project Documentation

Detailed documentation is maintained at the module level.

```text
data_pipeline/README.md
analytics/README.md
support_assistant/README.md
```

The root README provides the overall architecture, project workflow, technology stack, and module-level status.

---

# Author

Developed as part of the **AI & Machine Learning Capstone Project** for the **Zepto Data & AI Platform**.

---

# License

This project is intended for educational purposes as part of the **AI & Machine Learning Capstone Project**.
