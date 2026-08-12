"""
Tests for the Task 5 FastAPI application.
"""

from fastapi.testclient import TestClient

from support_assistant.api.main import app


client = TestClient(app)


def test_ask_policy_question_returns_valid_response():
    """
    Policy questions should execute the retrieval path.
    """

    response = client.post(
        "/ask",
        json={
            "query": "What is the delivery policy?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data

    assert isinstance(data["answer"], str)
    assert isinstance(data["sources"], list)
    assert isinstance(data["confidence"], float)

    assert data["sources"]


def test_ask_general_question_returns_valid_response():
    """
    General questions should execute the direct-answer path.
    """

    response = client.post(
        "/ask",
        json={
            "query": "Who is the CEO of Microsoft?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data

    assert isinstance(data["answer"], str)
    assert isinstance(data["sources"], list)
    assert isinstance(data["confidence"], float)

    assert data["sources"] == []


def test_ask_requires_query():
    """
    The /ask endpoint should reject requests without query.
    """

    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


def test_ask_rejects_invalid_request_body():
    """
    The /ask endpoint should reject a non-string query.
    """

    response = client.post(
        "/ask",
        json={
            "query": 123,
        },
    )

    assert response.status_code == 422