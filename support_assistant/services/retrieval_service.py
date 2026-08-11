"""
Retrieval Service.

Retrieves the most relevant
document chunks for a user query.
"""

from __future__ import annotations

from config.logging_config import (
    get_logger,
)

from services.embedding_service import (
    EmbeddingService,
)

from services.vector_store import (
    VectorStoreService,
)

from utils.exceptions import (
    RetrievalError,
)

logger = get_logger(__name__)


class RetrievalService:
    """
    Retrieve relevant context from
    the vector database.
    """

    def __init__(
        self,
    ) -> None:

        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_store = (
            VectorStoreService()
        )

    def retrieve_context(
        self,
        question: str,
        top_k: int = 3,
    ) -> list[str]:
        """
        Retrieve relevant document
        chunks.

        Parameters
        ----------
        question : str

        top_k : int

        Returns
        -------
        list[str]
        """

        logger.info(
            "Retrieving context."
        )

        try:

            query_embedding = (
                self.embedding_service
                .generate_query_embedding(
                    question,
                )
            )

            results = (
                self.vector_store
                .similarity_search(
                    query_embedding,
                    top_k,
                )
            )

            documents = (
                results.get(
                    "documents",
                    [[]],
                )[0]
            )

            logger.info(
                "%s document chunks retrieved.",
                len(documents),
            )

            return documents

        except Exception as error:

            logger.exception(
                "Context retrieval failed."
            )

            raise RetrievalError(
                str(error),
            ) from error

    def retrieve_chunks(
        self,
        question: str,
        top_k: int = 3,
    ) -> list[dict]:
        """
        Retrieve relevant document chunks
        together with their IDs and metadata.

        Parameters
        ----------
        question : str
            User question.

        top_k : int
            Number of chunks to retrieve.

        Returns
        -------
        list[dict]
            Retrieved chunks containing:
            id, text, document_name and chunk_id.
        """

        logger.info(
            "Retrieving document chunks."
        )

        try:

            query_embedding = (
                self.embedding_service
                .generate_query_embedding(
                    question,
                )
            )

            results = (
                self.vector_store
                .similarity_search(
                    query_embedding,
                    top_k,
                )
            )

            documents = (
                results.get(
                    "documents",
                    [[]],
                )[0]
            )

            ids = (
                results.get(
                    "ids",
                    [[]],
                )[0]
            )

            metadatas = (
                results.get(
                    "metadatas",
                    [[]],
                )[0]
            )

            chunks = []

            for index, document in enumerate(
                documents
            ):

                metadata = (
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                )

                chunk_id = (
                    ids[index]
                    if index < len(ids)
                    else metadata.get(
                        "chunk_id",
                        index,
                    )
                )

                chunks.append(
                    {
                        "id": str(chunk_id),
                        "text": document,
                        "document_name": metadata.get(
                            "document_name",
                            "",
                        ),
                        "chunk_id": metadata.get(
                            "chunk_id",
                            index,
                        ),
                    }
                )

            logger.info(
                "%s document chunks retrieved.",
                len(chunks),
            )

            return chunks

        except Exception as error:

            logger.exception(
                "Document chunk retrieval failed."
            )

            raise RetrievalError(
                str(error),
            ) from error
