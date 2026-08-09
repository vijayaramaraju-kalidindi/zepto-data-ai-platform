"""
Support Assistant.

Application entry point.
"""

from __future__ import annotations

from config.logging_config import (
    get_logger,
)

from services.ingestion_service import (
    IngestionService,
)

from services.prompt_service import (
    PromptService,
)

from services.graph_service import (
    GraphService,
)


logger = get_logger(__name__)


def main() -> None:
    """
    Execute the Support Assistant
    ingestion and prompt-template validation.
    """

    logger.info(
        "Support Assistant initialized."
    )

    # --------------------------------------------------
    # Task 1: Document ingestion
    # --------------------------------------------------

    ingestion_service = (
        IngestionService()
    )

    ingestion_service.run()

    logger.info(
        "Document ingestion completed."
    )

    # --------------------------------------------------
    # Task 2: Structured prompt template
    # --------------------------------------------------

    prompt_service = (
        PromptService()
    )

    sample_question = (
        "How much does priority delivery cost?"
    )

    sample_context = [
        (
            "Priority delivery is available at checkout "
            "for an additional INR 15."
        )
    ]

    prompt = prompt_service.build_prompt(
        question=sample_question,
        context=sample_context,
    )

    logger.info(
        "Task 2 structured prompt created successfully."
    )

    logger.debug(
        "Generated prompt:\n%s",
        prompt,
    )

    graph_service = GraphService()

    result = graph_service.run(
        "What is the delivery policy?"
    )

    logger.info(
        "Task 3 graph execution completed."
    )

    logger.info(
        "Task 3 intent: %s",
        result.get("intent"),
    )

    retrieved_context = result.get(
        "retrieved_context",
        [],
    )

    logger.info(
        "Task 3 retrieved context chunks: %s",
        len(retrieved_context),
    )

    # for index, chunk in enumerate(
    #     retrieved_context,
    #     start=1,
    # ):

    #     logger.info(
    #         "Task 3 retrieved chunk %s:\n%s",
    #         index,
    #         chunk,
    #     )

    logger.info(
        "Task 3 answer:\n%s",
        result.get("answer", ""),
    )

    logger.info(
        "Support Assistant completed successfully."
    )


if __name__ == "__main__":
    main()
