# Support Assistant Module

## Module 3 - GenAI Support Assistant, RAG, LangGraph & FastAPI

---

## Overview

The Support Assistant module implements a complete Retrieval-Augmented Generation (RAG) based customer support service for Zepto.

The module combines:

* Document ingestion
* Text chunking
* Local semantic embeddings
* ChromaDB vector storage
* Semantic retrieval
* LangGraph workflow orchestration
* Deterministic offline LLM-mock execution
* Optional real-LLM generation
* Pydantic structured response validation
* FastAPI REST API
* Docker-based execution

The implementation is located under:

```text
/support_assistant
```

The design follows the IIT Patna Capstone Project Module 3 requirements.

The required graded path is implemented using the deterministic `MOCK_LLM` mode. This allows the complete application to run without an LLM API key or an external LLM provider.

The optional real-LLM path is controlled through:

```text
MOCK_LLM=0
```

Hugging Face deployment has **not yet been attempted** and is therefore not claimed as part of the current implementation.

---

## Objectives

The objectives of this module are:

* Build a small Zepto support knowledge corpus.
* Load and process all 8 corpus documents.
* Generate local embeddings using `all-MiniLM-L6-v2`.
* Store document embeddings in ChromaDB.
* Perform semantic top-3 retrieval.
* Create a structured prompt for optional LLM generation.
* Build a LangGraph `StateGraph`.
* Implement intent classification and conditional routing.
* Provide deterministic mock responses without network calls.
* Validate responses using Pydantic.
* Expose the assistant through a FastAPI `/ask` endpoint.
* Containerize the application using Docker.
* Keep the optional real-LLM and Hugging Face extensions separate from the required baseline.

---

# Technology Stack

The project was implemented using the following technologies.

## Programming Language

* Python 3

## RAG / Embeddings

* Sentence Transformers
* `all-MiniLM-L6-v2`

## Vector Database

* ChromaDB

## Workflow Orchestration

* LangGraph
* `StateGraph`
* `TypedDict`

## Structured Validation

* Pydantic

## API

* FastAPI
* Uvicorn

## Optional LLM

* Groq API through the optional `MOCK_LLM=0` path

## Testing

* Pytest

## Containerization

* Docker

## Development Environment

* Visual Studio Code
* Git
* GitHub

---

# Project Structure

The Module 3 implementation is organized as a service-oriented application.

```text
support_assistant/
│
├── api/
│   └── __pycache__/
│
├── chroma_db/
│   ├── 093f9d8a-91c4-4fc9-b404-fc7586bb2873
│   ├── 1822ffed-7db7-4675-9995-59d87eb46a7b
│   ├── 3ed7e383-2aba-47ce-8159-c5b152402220
│   ├── 44d49bfb-420b-444f-a8e4-83eaffa19cde
│   ├── 4ba8d9c7-a529-4a2f-9828-aee1b91b1049
│   ├── 5e2bb0dd-17c8-4a7c-8178-0bcdd2271486
│   ├── 698e9961-1e4b-4090-8014-367b2bfe4f19
│   ├── 76f9b3f5-d204-4a9e-8045-23fb4b741b84
│   ├── 7b86868a-b864-4f5c-9c8e-29f532830676
│   ├── c82b4d37-c7bd-403d-8224-f7eac8f056b0
│   └── cdabb0c9-55bf-417f-9b49-7fb726eea20f
│
├── config/
│   └── __pycache__/
│
├── docs/
│
├── models/
│   └── __pycache__/
│
├── outputs/
│   └── logs/
│
├── services/
│   └── __pycache__/
│
├── tests/
│   └── __pycache__/
│
├── utils/
│   └── __pycache__/
│
└── __pycache__/
```

The service boundaries used in the implementation separate embedding, vector storage, retrieval, graph orchestration, API handling, and validation.

---

# Zepto Support Corpus

The application uses the required 8-document Zepto support corpus.

The documents cover:

| Document | Subject                 |
| -------- | ----------------------- |
| `doc_01` | Delivery Policy         |
| `doc_02` | Returns & Refunds       |
| `doc_03` | Membership              |
| `doc_04` | Order Tracking          |
| `doc_05` | Order Cancellation      |
| `doc_06` | Damaged / Missing Items |
| `doc_07` | Gift Cards              |
| `doc_08` | Customer Support Hours  |

The corpus is stored locally and does not require an external knowledge source at query time.

---

# RAG Architecture

The complete RAG pipeline implemented in Module 3 is:

```text
┌──────────────────────────┐
│  8 Zepto Corpus Documents│
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       INGESTION          │
│ Load + Chunk Documents   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       EMBEDDING          │
│ all-MiniLM-L6-v2         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        CHROMADB          │
│ support_assistant        │
│ Vector Collection        │
└────────────┬─────────────┘
             │
             │ User Query
             ▼
┌──────────────────────────┐
│     classify_intent      │
│ LangGraph Node           │
└────────────┬─────────────┘
             │
       Conditional Edge
       ┌─────┴──────┐
       │            │
       ▼            ▼
 policy_question  general_question
       │            │
       ▼            ▼
retrieve_and_answer direct_answer
       │
       ▼
 ChromaDB Top-3
       │
       ▼
 Answer Generation
       │
       └────────────┐
                    ▼
             Pydantic Validation
                    │
                    ▼
              FastAPI /ask
```

---

# RAG Pipeline Stage 1 - Ingestion

## Objective

Load the 8 Zepto support documents and prepare their contents for embedding.

The corpus documents are loaded from the local `support_assistant` corpus directory.

The ingestion process preserves the source document information so that the retrieved context can be traced back to the original corpus document.

The document content is converted into chunks before embedding.

For this module, the corpus documents are relatively small, so the implementation uses document-level/small chunk processing rather than a large-document processing strategy.

The resulting data flow is:

```text
Corpus File
    ↓
Document Text
    ↓
Chunk
    ↓
Embedding
```

---

## Implementation

The ingestion and preparation logic feeds the embedding service.

Each chunk remains associated with its source document.

This is important because the final Pydantic response exposes the retrieved source information through the `sources` field.

---

## Key Result

All 8 corpus documents are available to the embedding and vector-store pipeline.

---

# Task 1 - Embedding and ChromaDB Vector Store

## Objective

Embed the complete Zepto support corpus and store the vectors in ChromaDB so that the documents can be queried semantically.

---

## Embedding Model

The application uses:

```text
all-MiniLM-L6-v2
```

through the Sentence Transformers library.

The embedding service loads the model locally.

The runtime logs confirm the model loading process:

```text
Loading embedding model: all-MiniLM-L6-v2
Embedding model loaded successfully.
```

The model is used both for corpus embeddings and for generating the embedding of an incoming user query.

---

## Embedding Flow

```text
Document Chunk
      │
      ▼
EmbeddingService
      │
      ▼
all-MiniLM-L6-v2
      │
      ▼
Vector
      │
      ▼
ChromaDB
```

For a user query:

```text
User Question
      │
      ▼
EmbeddingService
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB Similarity Search
```

---

## ChromaDB Collection

The application uses the ChromaDB collection:

```text
support_assistant
```

The runtime logs confirm:

```text
Initializing ChromaDB.
Using collection: support_assistant
```

The collection stores the embedded support-document chunks and is queried using semantic similarity.

---

## Top-K Retrieval

The implementation retrieves:

```text
Top 3
```

most similar document chunks.

The runtime logs confirm:

```text
3 document chunks retrieved.
```

---

## Query Retrieval Flow

```text
Question
   │
   ▼
Generate Query Embedding
   │
   ▼
ChromaDB
   │
   ▼
Similarity Search
   │
   ▼
Top 3 Chunks
```

---

## Key Findings

* The embedding model runs locally.
* No LLM API is required for embedding.
* ChromaDB provides the semantic retrieval layer.
* The vector collection is named `support_assistant`.
* Retrieval returns three document chunks.
* Retrieval is performed independently of the LLM mock/real-generation toggle.

---

# Task 2 - Structured Prompt Engineering

## Objective

Create a structured prompt for the optional real-LLM generation path.

The prompt follows the required five-part skeleton:

1. Role
2. Context
3. Task
4. Format
5. Length

The implementation also includes:

* Explicit negative constraint
* Few-shot example

---

## Prompt Structure

The prompt follows this structure:

```text
Role
  ↓
Context
  ↓
Task
  ↓
Format
  ↓
Length
  ↓
Negative Constraint
  ↓
Few-Shot Example
```

---

## Role

The assistant is instructed to behave as a Zepto customer support assistant.

---

## Context

The retrieved ChromaDB chunks are supplied as the knowledge context.

The purpose of this section is to ground the generated answer in the retrieved corpus.

---

## Task

The LLM is instructed to answer the user's question using the supplied support context.

---

## Format

The prompt specifies the expected structured answer format so that the generated response can subsequently be validated.

---

## Length

The prompt instructs the model to produce a concise customer-support response.

---

## Negative Constraint

The prompt explicitly prevents unsupported information.

The core constraint is:

```text
Do not answer using information that is not present in the provided context.
```

This is particularly important for RAG because the generated answer should remain grounded in the retrieved support corpus.

---

## Few-Shot Example

The prompt also contains a concrete example showing:

```text
Example Question
        ↓
Example Context
        ↓
Example Answer
```

This gives the optional LLM generation path an explicit example of the expected answer behavior.

---

## MOCK_LLM Relationship

The structured prompt is used by the optional:

```text
MOCK_LLM=0
```

path.

It is not required for the default deterministic mock execution.

This keeps the graded baseline completely offline.

---

# Task 3 - LangGraph Workflow and Intent Routing

## Objective

Implement the support assistant workflow using LangGraph `StateGraph` and route questions according to their intent.

The graph contains three required named nodes:

```text
classify_intent
retrieve_and_answer
direct_answer
```

---

## Graph Architecture

```text
                         ┌────────────────────┐
                         │  classify_intent   │
                         └─────────┬──────────┘
                                   │
                          Conditional Edge
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                 policy_question       general_question
                         │                   │
                         ▼                   ▼
              retrieve_and_answer       direct_answer
```

The graph structure was explicitly tested.

The graph test confirms that the required graph nodes are present.

---

# Task 3.1 - `classify_intent`

## Objective

Determine whether the incoming question requires retrieval from the Zepto support corpus.

Two intents are supported:

```text
policy_question
general_question
```

---

## Mock Classification

With `MOCK_LLM` unset or set to:

```text
MOCK_LLM=1
```

the classifier uses a deterministic keyword heuristic.

The required policy keywords are:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

For example:

```text
How long does delivery take?
```

is classified as:

```text
policy_question
```

An unrelated question is classified as:

```text
general_question
```

The implementation logs the classification explicitly.

Example:

```text
Question classified as: policy_question
```

---

## No LLM Call in Mock Mode

The default classifier does not call an external LLM.

Therefore:

```text
MOCK_LLM = default
        │
        ▼
Keyword Heuristic
        │
        ▼
Intent
```

This makes the classification deterministic and suitable for automated grading.

---

## Optional Real-LLM Classification

When:

```text
MOCK_LLM=0
```

the optional implementation can use the configured LLM path for classification.

The routing mechanism itself remains unchanged.

Only the LLM-dependent generation/classification behavior changes.

---

# Task 3.2 - `retrieve_and_answer`

## Objective

Process a `policy_question` using genuine semantic retrieval and generate the response.

The node performs:

```text
Question
   ↓
Query Embedding
   ↓
ChromaDB Similarity Search
   ↓
Top 3 Chunks
   ↓
Answer Generation
```

---

## Retrieval Runs in Both Modes

An important design decision is that ChromaDB retrieval is **not mocked**.

It runs in both:

```text
MOCK_LLM default
MOCK_LLM=0
```

This ensures that the module remains a genuine RAG implementation even when LLM generation is disabled.

The runtime logs show the actual retrieval process:

```text
Question classified as: policy_question
Retrieving context.
Generating query embedding.
Performing similarity search.
3 document chunks retrieved.
```

---

## Mock Generation

With the default `MOCK_LLM` setting, no external LLM call is made.

Instead, the implementation generates a deterministic answer using the most relevant retrieved chunk.

The response follows the required pattern:

```text
Based on the retrieved context: ...
```

The snippet is derived from the top retrieved context.

For example, a delivery-policy query retrieves content beginning with the Delivery Policy document and generates:

```text
Based on the retrieved context: Delivery Policy: "Zepto delivers grocery and household essentials...
```

The runtime test output confirms this behavior.

---

## Optional Real-LLM Generation

With:

```text
MOCK_LLM=0
```

the retrieved context is supplied to the structured prompt and passed to the configured real LLM.

The flow becomes:

```text
Query
  ↓
ChromaDB Top-3
  ↓
Structured Prompt
  ↓
Real LLM
  ↓
Pydantic Validation
```

---

# Task 3.3 - `direct_answer`

## Objective

Handle `general_question` queries that do not require retrieval.

For example:

```text
What is the capital of France?
```

is classified as:

```text
general_question
```

and routed directly to:

```text
direct_answer
```

---

## Mock Mode

The default implementation returns a fixed canned response.

No:

* ChromaDB retrieval
* External LLM call

is required for this route.

The resulting flow is:

```text
General Question
      ↓
classify_intent
      ↓
general_question
      ↓
direct_answer
      ↓
Fixed Response
```

---

## Optional Real-LLM Mode

With:

```text
MOCK_LLM=0
```

the optional path can call the LLM directly.

Retrieval is not performed for this route.

---

# Conditional Routing

The conditional edge is attached to:

```text
classify_intent
```

and routes according to the returned intent.

```text
policy_question
      ↓
retrieve_and_answer

general_question
      ↓
direct_answer
```

The routing logic itself is independent of `MOCK_LLM`.

This is an important architectural distinction:

```text
Intent Routing
      │
      └── always follows classification

Generation
      │
      ├── MOCK_LLM default → deterministic mock
      │
      └── MOCK_LLM=0 → optional real LLM
```

---

# Task 4 - Pydantic Structured Response

## Objective

Enforce a deterministic JSON response contract using Pydantic.

The response schema contains:

```text
answer
sources
confidence
```

---

## Response Schema

Conceptually:

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "document/chunk identifier"
  ],
  "confidence": 1.0
}
```

---

## `answer`

Contains the final response returned to the API client.

For a policy question in mock mode, it is generated from the retrieved context.

For a general question, it contains the deterministic direct-answer response.

---

## `sources`

Contains the retrieved document/chunk identifiers for policy questions.

For a general question:

```text
sources = []
```

because no retrieval is performed.

---

## `confidence`

The mock-mode value is populated deterministically by application code.

This avoids depending on an LLM to produce a confidence score.

---

## Validation Flow

```text
Graph Output
     ↓
Pydantic Model
     ↓
Validation
     ↓
Validated Response
     ↓
FastAPI
```

This ensures that the API does not return an unvalidated model response.

---

## Optional Real-LLM Retry

The optional real-LLM path contains retry logic for malformed structured output.

The intended flow is:

```text
LLM Response
     ↓
Pydantic Validation
     │
     ├── Valid → Return
     │
     └── Invalid
            ↓
       Corrective Prompt
            ↓
          Retry
```

The implementation allows the optional real-LLM path to retry validation failures before returning an error response.

The mock path does not require this retry because its response is constructed deterministically.

---

# Task 5 - FastAPI REST API

## Objective

Expose the LangGraph support assistant through a REST API.

The primary endpoint is:

```http
POST /ask
```

---

## Request Schema

The endpoint accepts:

```json
{
  "query": "What is the delivery policy?"
}
```

The request is validated using a Pydantic request model.

---

## API Processing Flow

```text
HTTP POST /ask
       │
       ▼
Pydantic Request Validation
       │
       ▼
GraphService
       │
       ▼
LangGraph
       │
       ▼
classify_intent
       │
       ├──────── policy_question ────────┐
       │                                 │
       │                                 ▼
       │                       retrieve_and_answer
       │                                 │
       │                                 ▼
       │                             ChromaDB
       │                                 │
       │                                 ▼
       │                           Answer Generation
       │
       └──────── general_question ───────┐
                                         │
                                         ▼
                                   direct_answer
                                         │
                                         ▼
                                  Fixed / LLM Answer
                                         │
                                         ▼
                                  Pydantic Response
                                         │
                                         ▼
                                    JSON Response
```

---

# Local Execution

The application is designed to run locally using Uvicorn.

Example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The endpoint is then available at:

```text
http://localhost:8000/ask
```

---

# Example 1 - Policy Question

The following type of query exercises the RAG route:

```text
What is the delivery policy?
```

The observed graph execution is:

```text
Question classified as: policy_question
Retrieving context.
Generating query embedding.
Performing similarity search.
3 document chunks retrieved.
```

The retrieved context contains the Delivery Policy document, including the statement that Zepto delivers within 10 to 30 minutes depending on delivery zone and order volume.

The mock response follows:

```text
Based on the retrieved context: Delivery Policy: "Zepto delivers grocery and household essentials...
```

---

# Example 2 - General Question

A question unrelated to Zepto policy is routed to:

```text
general_question
```

and then:

```text
direct_answer
```

The runtime logs confirm the general-question path:

```text
Question classified as: general_question
Support Assistant graph completed.
```

No retrieval is performed for this path.

---

# Task 5 - Docker Containerization

## Objective

Containerize the FastAPI application so that it can be built and executed locally.

The required Docker baseline is:

```text
Dockerfile
    ↓
docker build
    ↓
Docker Image
    ↓
docker run
    ↓
FastAPI /ask
```

---

## Build

From the project root:

```bash
docker build -t support-assistant ./support_assistant
```

---

## Run

```bash
docker run --rm -p 8000:8000 support-assistant
```

The API can then be accessed through:

```text
http://localhost:8000/ask
```

Example:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What is the delivery policy?\"}"
```

The Dockerfile is the required graded containerization baseline.

---

# MOCK_LLM Design

The `MOCK_LLM` switch was intentionally designed to keep the required implementation independent of external LLM providers.

## Default Mode

```text
MOCK_LLM
```

unset, or:

```text
MOCK_LLM=1
```

The application uses:

```text
Keyword intent classification
        +
Real local embedding
        +
Real ChromaDB retrieval
        +
Deterministic answer generation
        +
Pydantic validation
```

No external LLM API call is required.

---

## Optional Real-LLM Mode

```text
MOCK_LLM=0
```

The application can use the configured LLM for:

* Intent classification
* RAG answer generation
* Direct answer generation

The embedding and retrieval stages remain local.

```text
                    MOCK_LLM
                       │
             ┌─────────┴─────────┐
             │                   │
          Default               0
             │                   │
             ▼                   ▼
       Mock generation      Real LLM generation
             │                   │
             └─────────┬─────────┘
                       │
                 Pydantic Validation
```

---

# End-to-End Architecture

The final implementation can be summarized as:

```text
                         ZEpto Corpus
                       8 Documents
                            │
                            ▼
                       Ingestion
                            │
                            ▼
                  all-MiniLM-L6-v2
                       Embeddings
                            │
                            ▼
                   ChromaDB Collection
                  "support_assistant"
                            │
                            │
                      User Question
                            │
                            ▼
                    FastAPI POST /ask
                            │
                            ▼
                    GraphService
                            │
                            ▼
                   LangGraph StateGraph
                            │
                            ▼
                    classify_intent
                       /          \
                      /            \
                     ▼              ▼
           policy_question    general_question
                  │                   │
                  ▼                   ▼
       retrieve_and_answer       direct_answer
                  │                   │
                  ▼                   │
             Query Embed             │
                  │                   │
                  ▼                   │
             ChromaDB                │
                  │                   │
               Top-3                 │
                  │                   │
                  ▼                   ▼
             Generation          Generation
                  │                   │
                  └─────────┬─────────┘
                            │
                            ▼
                     Pydantic Model
                            │
                            ▼
                    answer/sources/
                       confidence
                            │
                            ▼
                       JSON Response
```

---

# Generated / Runtime Components

The important Module 3 runtime components are:

| Component              | Responsibility                                        |
| ---------------------- | ----------------------------------------------------- |
| `embedding_service.py` | Loads `all-MiniLM-L6-v2` and generates embeddings     |
| `vector_store.py`      | Initializes and queries ChromaDB                      |
| `retrieval_service.py` | Generates query embeddings and retrieves top-3 chunks |
| `graph_service.py`     | Builds and executes the LangGraph workflow            |
| Prompt module          | Defines the structured real-LLM prompt                |
| Pydantic models        | Validate request and response structures              |
| `main.py`              | FastAPI application entry point                       |
| `Dockerfile`           | Containerizes the FastAPI application                 |
| `tests/`               | Validates graph behavior and routing                  |

---

# Acceptance Criteria Mapping

| Requirement                             | Implementation Status |
| --------------------------------------- | --------------------- |
| 8 corpus documents                      | Implemented           |
| Local `all-MiniLM-L6-v2` embeddings     | Implemented           |
| ChromaDB vector collection              | Implemented           |
| `support_assistant` collection          | Implemented           |
| Top-3 semantic retrieval                | Implemented           |
| Structured prompt                       | Implemented           |
| Role / Context / Task / Format / Length | Implemented           |
| Negative constraint                     | Implemented           |
| Few-shot example                        | Implemented           |
| `classify_intent` node                  | Implemented           |
| `retrieve_and_answer` node              | Implemented           |
| `direct_answer` node                    | Implemented           |
| LangGraph conditional routing           | Implemented           |
| Default keyword heuristic               | Implemented           |
| Real retrieval in mock mode             | Implemented           |
| Mock RAG response                       | Implemented           |
| Mock direct response                    | Implemented           |
| Pydantic response schema                | Implemented           |
| `answer` / `sources` / `confidence`     | Implemented           |
| Real-LLM retry logic                    | Implemented           |
| FastAPI `/ask`                          | Implemented           |
| Local Uvicorn execution                 | Implemented           |
| Dockerfile                              | Implemented           |
| Local Docker execution                  | Implemented           |
| Hugging Face Space                      | Not attempted         |

---

# Current Implementation Status

The required Module 3 baseline is designed around the offline/mock execution path.

```text
RAG Pipeline                 Implemented
ChromaDB                     Implemented
Local Embeddings              Implemented
LangGraph                     Implemented
Intent Routing                Implemented
Mock LLM Path                 Implemented
Pydantic Validation           Implemented
FastAPI                       Implemented
Dockerfile                    Implemented
Hugging Face Deployment       Not attempted
```

The Hugging Face deployment is intentionally not represented as completed because it has not yet been attempted.

---

# Learning Outcomes

This module demonstrates the complete lifecycle of a small production-oriented GenAI/RAG service, including:

* Document ingestion
* Text chunking
* Semantic embeddings
* Local embedding models
* Vector databases
* ChromaDB
* Semantic similarity search
* Top-K retrieval
* Retrieval-Augmented Generation
* Prompt engineering
* Negative constraints
* Few-shot prompting
* LangGraph `StateGraph`
* Typed graph state
* Intent classification
* Conditional graph routing
* Offline deterministic LLM mocking
* Optional real-LLM integration
* Structured output validation
* Pydantic models
* FastAPI REST APIs
* Uvicorn
* Docker containerization
* Automated testing
* Separation of retrieval and generation concerns

---

# Future Enhancements

The current implementation establishes the required local RAG and API foundation.

Potential future enhancements include:

* Enable and validate the optional `MOCK_LLM=0` real-LLM path.
* Test the structured prompt against a real LLM.
* Validate the Pydantic retry-on-failure path with intentionally malformed LLM output.
* Improve source/chunk metadata returned by the retrieval layer.
* Add more comprehensive API integration tests.
* Add health and readiness endpoints.
* Add request logging and observability.
* Deploy the existing Docker image to Hugging Face Spaces.
* Add a live demonstration URL after successful Hugging Face deployment.

Hugging Face deployment is intentionally listed as a future enhancement because it has not yet been attempted.

---

# Conclusion

Module 3 implements a complete GenAI Support Assistant using a local RAG pipeline and LangGraph orchestration.

The implementation starts with eight Zepto support documents, generates local embeddings using `all-MiniLM-L6-v2`, and stores them in the ChromaDB `support_assistant` collection. Incoming questions are classified by the LangGraph `classify_intent` node and conditionally routed either to the RAG retrieval path or the direct-answer path.

Policy questions use genuine semantic retrieval from ChromaDB and retrieve the top three relevant document chunks. In the default `MOCK_LLM` mode, answer generation remains deterministic and offline, while the optional `MOCK_LLM=0` path provides the foundation for real-LLM generation using the structured prompt.

The final response is validated through Pydantic and exposed through a FastAPI `/ask` endpoint. The application is also containerized using Docker, providing a locally runnable deployment baseline.

The architecture therefore demonstrates the complete GenAI application flow:

```text
Documents
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Semantic Retrieval
    ↓
LangGraph Routing
    ↓
Mock / Optional Real LLM
    ↓
Pydantic Validation
    ↓
FastAPI
    ↓
JSON Response
```
