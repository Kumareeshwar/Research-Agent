# The web search tool. Takes a query, returns a list of results.
import os
from langsmith import traceable
from tavily import TavilyClient


@traceable(run_type="tool", name="search_web")
def search_web(query: str) -> list[dict]:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query, max_results=3)
    return response["results"]  # each result has: title, url, content
