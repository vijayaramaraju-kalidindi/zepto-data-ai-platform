"""
LangGraph workflow for the Support Assistant.
"""

from __future__ import annotations

from typing import TypedDict

from config.logging_config import (
    get_logger,
)

from services.retrieval_service import (
    RetrievalService,
)

logger = get_logger(__name__)


class SupportAssistantState(TypedDict, total=False):
    """
    State passed between LangGraph nodes.
    """

    question: str
    intent: str
    retrieved_context: list[str]
    answer: str


class GraphService:
    """
    Build and execute the Support Assistant
    LangGraph workflow.
    """

    POLICY_KEYWORDS = [
            "delivery",
            "return",
            "refund",
            "membership",
            "tracking",
            "track",
            "cancel",
            "gift card",
            "support hours",
        ]

    def __init__(self) -> None:

        self.retrieval_service = (
            RetrievalService()
        )

        self.graph = self._build_graph()

    def classify_intent(
        self,
        state: SupportAssistantState,
    ) -> SupportAssistantState:
        """
        Classify the incoming question.

        MOCK_LLM baseline uses the required
        keyword heuristic.
        """

        question = state["question"]
        normalized_question = question.lower()

        is_policy_question = any(
            keyword in normalized_question
            for keyword in self.POLICY_KEYWORDS
        )

        if is_policy_question:
            intent = "policy_question"
        else:
            intent = "general_question"

        logger.info(
            "Question classified as: %s",
            intent,
        )

        return {
            **state,
            "intent": intent,
        }

    def retrieve_and_answer(
        self,
        state: SupportAssistantState,
    ) -> SupportAssistantState:
        """
        Retrieve the top-3 policy chunks and
        generate the required mock response.
        """

        question = state["question"]

        context = (
            self.retrieval_service
            .retrieve_context(
                question,
                top_k=3,
            )
        )

        if context:
            answer = (
                "Based on the retrieved context:\n\n"
                "Relevant Zepto policy information was retrieved."
            )
        else:
            answer = (
                "Based on the retrieved context:\n\n"
                "No relevant policy information was found."
            )
        return {
            **state,
            "retrieved_context": context,
            "answer": answer,
        }

    def direct_answer(
        self,
        state: SupportAssistantState,
    ) -> SupportAssistantState:
        """
        Handle general questions in mock mode.
        """

        answer = (
            "I can only answer questions about "
            "Zepto policies right now."
        )

        return {
            **state,
            "answer": answer,
        }

    def _route_after_classification(
        self,
        state: SupportAssistantState,
    ) -> str:
        """
        Route the workflow based on intent.
        """

        if state["intent"] == "policy_question":
            return "retrieve_and_answer"

        return "direct_answer"

    def _build_graph(self):
        """
        Build and compile the LangGraph StateGraph.
        """

        from langgraph.graph import (
            END,
            START,
            StateGraph,
        )

        workflow = StateGraph(
            SupportAssistantState,
        )

        workflow.add_node(
            "classify_intent",
            self.classify_intent,
        )

        workflow.add_node(
            "retrieve_and_answer",
            self.retrieve_and_answer,
        )

        workflow.add_node(
            "direct_answer",
            self.direct_answer,
        )

        workflow.add_edge(
            START,
            "classify_intent",
        )

        workflow.add_conditional_edges(
            "classify_intent",
            self._route_after_classification,
            {
                "retrieve_and_answer": "retrieve_and_answer",
                "direct_answer": "direct_answer",
            },
        )

        workflow.add_edge(
            "retrieve_and_answer",
            END,
        )

        workflow.add_edge(
            "direct_answer",
            END,
        )

        return workflow.compile()

    def run(
        self,
        question: str,
    ) -> SupportAssistantState:
        """
        Execute the Support Assistant graph.
        """

        if not question.strip():
            raise ValueError(
                "Question must not be empty."
            )

        logger.info(
            "Executing Support Assistant graph."
        )

        initial_state: SupportAssistantState = {
            "question": question,
        }

        result = self.graph.invoke(
            initial_state,
        )

        logger.info(
            "Support Assistant graph completed."
        )

        return result