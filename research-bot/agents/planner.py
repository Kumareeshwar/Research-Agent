# Planner agent: turns the user's question into a few search queries.
from config import llm


def planner(state: dict) -> dict:
    prompt = (
        "You are a research planner. Write 3 short web search queries that "
        "would help answer the question below. Return one query per line, "
        "with no numbering and no extra text.\n\n"
        f"Question: {state['question']}"
    )
    reply = llm.invoke(prompt)
    queries = [line.strip() for line in reply.content.splitlines() if line.strip()]
    return {"queries": queries}
