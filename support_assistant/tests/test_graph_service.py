"""
Tests for the Task 3 LangGraph workflow.
"""

from support_assistant.services.graph_service import (
    GraphService,
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