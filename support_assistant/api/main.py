"""
FastAPI application for the Zepto Support Assistant.
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from models.response_models import FinalAnswer
from services.graph_service import GraphService


app = FastAPI(
    title="Zepto Support Assistant",
    description="Task 5 API for the Zepto Support Assistant.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    """
    Request model for the /ask endpoint.
    """

    query: str


graph_service = GraphService()


@app.post(
    "/ask",
    response_model=FinalAnswer,
)
def ask(
    request: AskRequest,
) -> FinalAnswer:
    """
    Answer a user question using the Support Assistant graph.
    """

    result = graph_service.run(
        request.query,
    )

    return FinalAnswer(
        **result["response"],
    )