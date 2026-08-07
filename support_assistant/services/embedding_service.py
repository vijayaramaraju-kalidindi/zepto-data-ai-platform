"""
Embedding Service.

Chunks documents and generates
embeddings using Sentence
Transformers.
"""

from __future__ import annotations

from sentence_transformers import (
    SentenceTransformer,
)

from config.logging_config import (
    get_logger,
)

from config.settings import (
    EMBEDDING_MODEL,
)

from utils.exceptions import (
    EmbeddingGenerationError,
)

logger = get_logger(__name__)


class EmbeddingService:
    """
    Generate embeddings for
    document chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:

        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap

        logger.info(
            "Loading embedding model: %s",
            EMBEDDING_MODEL,
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL,
        )

        logger.info(
            "Embedding model loaded successfully."
        )

    def process_documents(
        self,
        documents: list[dict],
    ) -> list[dict]:
        """
        Chunk documents and generate
        embeddings.

        Parameters
        ----------
        documents : list[dict]

        Returns
        -------
        list[dict]
        """

        logger.info(
            "Generating embeddings."
        )

        try:

            embedded_chunks = []

            for document in documents:

                chunks = self.chunk_text(
                    document["content"],
                )

                logger.info(
                    "%s split into %s chunks.",
                    document["document_name"],
                    len(chunks),
                )

                for index, chunk in enumerate(
                    chunks,
                    start=1,
                ):

                    embedding = (
                        self.model.encode(
                            chunk,
                            convert_to_numpy=True,
                        )
                    )

                    embedded_chunks.append(
                        {
                            "document_name":
                                document["document_name"],
                            "chunk_id":
                                index,
                            "text":
                                chunk,
                            "embedding":
                                embedding,
                        }
                    )

            logger.info(
                "%s chunks embedded successfully.",
                len(embedded_chunks),
            )

            return embedded_chunks

        except Exception as error:

            logger.exception(
                "Embedding generation failed."
            )

            raise EmbeddingGenerationError(
                str(error),
            ) from error

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into overlapping
        chunks.

        Parameters
        ----------
        text : str

        Returns
        -------
        list[str]
        """

        chunks = []

        start = 0

        while start < len(text):

            end = (
                start
                + self.chunk_size
            )

            chunks.append(
                text[start:end]
            )

            start += (
                self.chunk_size
                - self.chunk_overlap
            )

        return chunks

def generate_query_embedding(
    self,
    query: str,
):
    """
    Generate an embedding for a
    user query.

    Parameters
    ----------
    query : str

    Returns
    -------
    numpy.ndarray
    """

    logger.info(
        "Generating query embedding."
    )

    return self.model.encode(
        query,
        convert_to_numpy=True,
    )