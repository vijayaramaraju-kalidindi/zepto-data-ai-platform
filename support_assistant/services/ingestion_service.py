"""
Document Ingestion Service.

Coordinates the complete document
ingestion pipeline.

Pipeline
--------
1. Load documents
2. Generate embeddings
3. Store embeddings in ChromaDB
"""

from __future__ import annotations

from config.logging_config import (
    get_logger,
)

from services.document_loader import (
    DocumentLoaderService,
)

from services.embedding_service import (
    EmbeddingService,
)

from services.vector_store import (
    VectorStoreService,
)

logger = get_logger(__name__)


class IngestionService:
    """
    Coordinate the complete
    document ingestion workflow.
    """

    def __init__(
        self,
    ) -> None:

        self.document_loader = (
            DocumentLoaderService()
        )

        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_store = (
            VectorStoreService()
        )

    def run(
        self,
    ) -> None:
        """
        Execute the complete
        ingestion pipeline.
        """


        self.vector_store.reset_collection()

        logger.info(
            "Starting document ingestion."
        )

        documents = (
            self.document_loader
            .load_documents()
        )

        embedded_chunks = (
            self.embedding_service
            .process_documents(
                documents,
            )
        )

        self.vector_store.store_embeddings(
            embedded_chunks,
        )
        

        logger.info(
            "Document ingestion completed successfully."
        )
