"""
Vector Store Service.

Stores and retrieves document
embeddings using ChromaDB.
"""

from __future__ import annotations

import chromadb

from config.logging_config import (
    get_logger,
)

from config.settings import (
    CHROMA_COLLECTION,
    CHROMA_DIRECTORY,
)

from utils.exceptions import (
    VectorStoreError,
)

logger = get_logger(__name__)


class VectorStoreService:
    """
    Manage the Chroma vector
    database.
    """

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Initializing ChromaDB."
        )

        self.client = (
            chromadb.PersistentClient(
                path=str(
                    CHROMA_DIRECTORY,
                ),
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=CHROMA_COLLECTION,
            )
        )

        logger.info(
            "Using collection: %s",
            CHROMA_COLLECTION,
        )

    def reset_collection(
        self,
    ) -> None:
        """
        Reset the ChromaDB collection.
        """

        logger.info(
            "Resetting ChromaDB collection."
        )

        try:

            self.client.delete_collection(
                name=CHROMA_COLLECTION,
            )

            logger.info(
                "Existing collection deleted."
            )

        except Exception:

            logger.info(
                "No existing collection found."
            )

        self.collection = (
            self.client.get_or_create_collection(
                name=CHROMA_COLLECTION,
            )
        )

        logger.info(
            "Fresh collection created."
        )

    def store_embeddings(
        self,
        embedded_chunks: list[dict],
    ) -> None:
        """
        Store embeddings in ChromaDB.

        Parameters
        ----------
        embedded_chunks : list[dict]
        """

        logger.info(
            "Storing embeddings."
        )

        try:

            for chunk in embedded_chunks:

                self.collection.add(
                    ids=[
                        (
                            f"{chunk['document_name']}"
                            f"_{chunk['chunk_id']}"
                        )
                    ],
                    documents=[
                        chunk["text"]
                    ],
                    embeddings=[
                        chunk[
                            "embedding"
                        ].tolist()
                    ],
                    metadatas=[
                        {
                            "document_name":
                                chunk[
                                    "document_name"
                                ],
                            "chunk_id":
                                chunk[
                                    "chunk_id"
                                ],
                        }
                    ],
                )

            logger.info(
                "%s chunks stored successfully.",
                len(embedded_chunks),
            )

        except Exception as error:

            logger.exception(
                "Failed to store embeddings."
            )

            raise VectorStoreError(
                str(error),
            ) from error

    def similarity_search(
        self,
        query_embedding,
        top_k: int = 3,
    ) -> dict:
        """
        Retrieve similar document
        chunks.

        Parameters
        ----------
        query_embedding

        top_k : int

        Returns
        -------
        dict
        """

        logger.info(
            "Performing similarity search."
        )

        try:

            return self.collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=top_k,
            )

        except Exception as error:

            logger.exception(
                "Similarity search failed."
            )

            raise VectorStoreError(
                str(error),
            ) from error

