"""
Document Loader Service.

Loads policy documents from the
configured documents directory.
"""

from __future__ import annotations

from pathlib import Path

from config.logging_config import (
    get_logger,
)

from config.settings import (
    DOCUMENTS_DIRECTORY,
)

from utils.exceptions import (
    DocumentLoadingError,
)

logger = get_logger(__name__)


class DocumentLoaderService:
    """
    Service responsible for loading
    policy documents.
    """

    def __init__(
        self,
    ) -> None:

        self.documents_directory = (
            DOCUMENTS_DIRECTORY
        )

    def load_documents(
        self,
    ) -> list[dict]:
        """
        Load all text documents.

        Returns
        -------
        list[dict]
            Loaded documents.
        """

        logger.info(
            "Loading policy documents."
        )

        try:


            document_files = sorted(
                self.documents_directory.glob("*.txt")
            )

            if not document_files:

                raise DocumentLoadingError(
                    "No documents found."
                )

            logger.info(
                "Found %s documents.",
                len(document_files),
            )

            documents = []

            for file_path in document_files:

                documents.append(
                    self.load_document(
                        file_path,
                    )
                )

            logger.info(
                "%s documents loaded successfully.",
                len(documents),
            )

            return documents

        except Exception as error:

            logger.exception(
                "Document loading failed."
            )

            raise DocumentLoadingError(
                str(error)
            ) from error

    def load_document(
        self,
        file_path: Path,
    ) -> dict:
        """
        Load a single document.

        Parameters
        ----------
        file_path : Path
            Path to document.

        Returns
        -------
        dict
            Document metadata.
        """

        logger.info(
            "Loading %s",
            file_path.name,
        )

        text = file_path.read_text(
            encoding="utf-8",
        )

        return {
            "document_name": file_path.name,
            "content": text,
        }