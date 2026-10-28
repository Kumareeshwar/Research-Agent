# Writer agent: summarizes the search results into the final answer.
from config import llm


def writer(state: dict) -> dict:
    sources = ""
    for r in state["results"]:
        sources += f"- {r['title']} ({r['url']})\n{r['content']}\n\n"

    prompt = (
        "Answer the question using only the sources below. "
        "Keep it short and clear, then list the source URLs you used.\n\n"
        f"Question: {state['question']}\n\nSources:\n{sources}"
    )
    reply = llm.invoke(prompt)
    return {"answer": reply.content}
