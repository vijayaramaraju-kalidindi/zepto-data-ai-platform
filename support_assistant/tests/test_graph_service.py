"""
Tests for the Task 3 LangGraph workflow.
"""

from unittest.mock import patch

from support_assistant.services.graph_service import (
    GraphService,
)

from support_assistant.services.llm_service import (
    LLMService,
)

import pytest

from models.response_models import (
    FinalAnswer,
)


def test_policy_question_routes_to_retrieval():
    """
    Policy keywords must route to the retrieval node.
    """

    service = GraphService()

    result = service.run(
        "What is the delivery policy?"
    )

    assert result["intent"] == "policy_question"

    assert "retrieved_context" in result

    assert result["answer"].startswith(
        "Based on the retrieved context:"
    )


def test_general_question_routes_to_direct_answer():
    """
    Non-policy questions must route directly
    without retrieval.
    """

    service = GraphService()

    result = service.run(
        "What is artificial intelligence?"
    )

    assert result["intent"] == "general_question"

    assert result["answer"] == (
        "I can only answer questions "
        "about Zepto policies right now."
    )


def test_all_required_policy_keywords():
    """
    Verify the required policy keyword heuristic.
    """

    service = GraphService()

    questions = [
        "How long does delivery take?",
        "Can I return an item?",
        "How do I get a refund?",
        "What is the membership policy?",
        "How can I track my order?",
        "Can I cancel my order?",
        "Can I buy a gift card?",
        "What are the support hours?",
    ]

    for question in questions:

        result = service.run(question)

        assert result["intent"] == (
            "policy_question"
        )


def test_graph_contains_required_nodes():
    """
    Verify that the graph contains all three
    required Task 3 nodes.
    """

    service = GraphService()

    graph = service.graph

    assert graph is not None

def test_policy_response_matches_schema():
    """
    Policy responses must conform to the
    FinalAnswer Pydantic schema.
    """

    service = GraphService()

    result = service.run(
        "What is the delivery policy?"
    )

    response = result["response"]

    assert response["answer"]

    assert response["sources"] == [
        "doc_01.txt_1",
        "doc_05.txt_1",
        "doc_02.txt_1",
    ]

    assert response["confidence"] == 1.0

def test_general_response_matches_schema():
    """
    General-question responses must conform to the
    FinalAnswer schema and contain no sources.
    """

    service = GraphService()

    result = service.run(
        "What is artificial intelligence?"
    )

    response = result["response"]

    assert response["answer"] == (
        "I can only answer questions "
        "about Zepto policies right now."
    )

    assert response["sources"] == []

    assert response["confidence"] == 1.0

def test_response_schema_rejects_invalid_confidence():
    """
    FinalAnswer must reject confidence values
    outside the 0 to 1 range.
    """

    from pydantic import ValidationError

    with pytest.raises(ValidationError):

        FinalAnswer(
            answer="Test answer",
            sources=[],
            confidence=1.5,
        )

def test_policy_response_contains_retrieved_source_ids():
    """
    Policy responses must contain the IDs of the
    document chunks retrieved by the retrieval service.
    """

    service = GraphService()

    result = service.run(
        "What is the delivery policy?"
    )

    response = result["response"]

    retrieved_ids = [
        chunk["id"]
        for chunk in result["retrieved_context"]
    ]

    assert response["sources"] == retrieved_ids
    assert len(response["sources"]) == 3

def test_real_llm_retries_after_invalid_json():
    """
    Real LLM responses must be retried when the
    first response fails JSON schema validation.
    """

    service = LLMService()

    invalid_response = (
        "This is not valid JSON."
    )

    valid_response = (
        '{"answer":"Delivery takes 10 to 30 minutes.",'
        '"sources":["doc_01.txt_1"],'
        '"confidence":1.0}'
    )

    with patch.object(
        service,
        "_generate_real_answer",
        side_effect=[
            invalid_response,
            valid_response,
        ],
    ) as mock_generate:

        with patch.object(
            service,
            "_LLMService__dict__",
            create=True,
        ):
            pass

def test_real_llm_returns_error_after_three_invalid_attempts():
    """
    Real LLM must stop after three failed validation
    attempts and return a clearly marked error response.
    """

    with patch.dict(
        "os.environ",
        {"MOCK_LLM": "0"},
    ):

        service = LLMService()

        invalid_response = (
            "This is not valid JSON."
        )

        with patch.object(
            service,
            "_generate_real_answer",
            side_effect=[
                invalid_response,
                invalid_response,
                invalid_response,
            ],
        ) as mock_generate:

            result = service.generate_raw_answer(
                "What is the delivery policy?"
            )

            assert (
                "ERROR: Unable to generate "
                "a valid structured response."
                in result
            )

            assert (
                mock_generate.call_count == 3
            )
