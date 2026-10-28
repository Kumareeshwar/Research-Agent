# Researcher agent: runs every search query and collects the results.
from tools.search import search_web


def researcher(state: dict) -> dict:
    results = []
    for query in state["queries"]:
        results.extend(search_web(query))
    return {"results": results}
