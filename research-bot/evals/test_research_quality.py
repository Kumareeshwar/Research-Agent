# DeepEval checks on real graph output. Calls live Groq + Tavily, so run it on purpose:
#   pytest evals            (or: deepeval test run evals/test_research_quality.py)
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from evals.judge import GroqJudge
from graph.workflow import graph

QUESTIONS = [
    "What was the outcome of the Israeli general election held on October 27, 2026, according to the exit polls?",
    "Which severe cyclonic storm made landfall along India's eastern coast in late October 2026, forcing evacuations in Odisha?",
    "What technical misconfigurations allowed OpenAI and Anthropic models to circumvent sandboxes during their recent cybersecurity evaluations?",
]

judge = GroqJudge()


@pytest.mark.parametrize("question", QUESTIONS)
def test_answer_quality(question):
    result = graph.invoke({"question": question})

    test_case = LLMTestCase(
        input=question,
        actual_output=result["answer"],
        retrieval_context=[r["content"] for r in result["results"]],
    )
    assert_test(
        test_case,
        [
            AnswerRelevancyMetric(threshold=0.7, model=judge, async_mode=False),
            FaithfulnessMetric(threshold=0.7, model=judge, async_mode=False),
        ],
    )
