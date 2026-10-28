# The graph: planner -> researcher -> writer.
# Each agent reads the shared state and returns the keys it wants to update.
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.planner import planner
from agents.researcher import researcher
from agents.writer import writer


class State(TypedDict, total=False):
    question: str   # the user's question
    queries: list   # set by planner
    results: list   # set by researcher
    answer: str     # set by writer


builder = StateGraph(State)
builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)

builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", END)

graph = builder.compile()
