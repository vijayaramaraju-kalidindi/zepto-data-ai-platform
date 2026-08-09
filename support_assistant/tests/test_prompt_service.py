"""
Tests for PromptService.
"""

from services.prompt_service import PromptService


def test_prompt_contains_required_structure() -> None:
    """Verify the required prompt skeleton is present."""

    service = PromptService()

    prompt = service.build_prompt(
        question="How much is priority delivery?",
        context=[
            "Priority delivery is available for an "
            "additional INR 15."
        ],
    )

    assert "ROLE" in prompt
    assert "CONTEXT" in prompt
    assert "TASK" in prompt
    assert "FORMAT" in prompt
    assert "LENGTH" in prompt


def test_prompt_contains_negative_constraint() -> None:
    """Verify the prompt prevents unsupported answers."""

    service = PromptService()

    prompt = service.build_prompt(
        question="How much is priority delivery?",
        context=[
            "Priority delivery costs an additional INR 15."
        ],
    )

    assert (
        "Do not answer using information that is not present"
        in prompt
    )


def test_prompt_contains_few_shot_example() -> None:
    """Verify that few-shot examples are embedded."""

    service = PromptService()

    prompt = service.build_prompt(
        question="Is delivery free?",
        context=[
            "Standard delivery is free on orders over INR 149."
        ],
    )

    assert "FEW-SHOT EXAMPLE" in prompt
    assert "Expected Answer:" in prompt


def test_prompt_contains_question_and_context() -> None:
    """Verify dynamic question and context are included."""

    service = PromptService()

    question = "Is priority delivery available?"

    context = [
        "Priority delivery is available for an additional INR 15."
    ]

    prompt = service.build_prompt(
        question=question,
        context=context,
    )

    assert question in prompt
    assert context[0] in prompt
