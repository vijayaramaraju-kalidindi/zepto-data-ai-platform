"""
Support Assistant.

Application entry point.

Tasks covered:
    Task 1: Document ingestion
    Task 2: Structured prompt generation
    Task 3: LangGraph workflow
    Task 4: Structured LLM response validation
"""

from __future__ import annotations

from config.logging_config import (
    get_logger,
)

from models.response_models import (
    FinalAnswer,
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
    Execute the Support Assistant workflow
    through Task 4.
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
        "Task 1: Document ingestion completed."
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
        "Task 2: Structured prompt created successfully."
    )

    logger.debug(
        "Generated prompt:\n%s",
        prompt,
    )

    # --------------------------------------------------
    # Task 3: LangGraph workflow
    # Task 4: Structured LLM response
    # --------------------------------------------------

    graph_service = GraphService()

    sample_query = (
        "What is the delivery policy?"
    )

    result = graph_service.run(
        sample_query,
    )

    logger.info(
        "Task 3: Graph execution completed."
    )

    logger.info(
        "Intent: %s",
        result.get("intent"),
    )

    retrieved_context = result.get(
        "retrieved_context",
        [],
    )

    logger.info(
        "Retrieved context chunks: %s",
        len(retrieved_context),
    )

    logger.info(
        "Answer:\n%s",
        result.get("answer", ""),
    )

    # --------------------------------------------------
    # Task 4: FinalAnswer validation
    # --------------------------------------------------

    response_data = result.get(
        "response",
    )

    if response_data:

        response = FinalAnswer(
            **response_data,
        )

        logger.info(
            "Task 4: Structured response validated successfully."
        )

        logger.info(
            "Final response:\n%s",
            response.model_dump(),
        )

        logger.info(
            "Sources: %s",
            response.sources,
        )

        logger.info(
            "Confidence: %.2f",
            response.confidence,
        )

    logger.info(
        "Support Assistant completed successfully."
    )


if __name__ == "__main__":
    main()