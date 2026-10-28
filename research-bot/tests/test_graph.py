# Checks that the graph is wired up with all three agents.
from graph.workflow import graph


def test_graph_has_all_agents():
    nodes = graph.get_graph().nodes
    for name in ("planner", "researcher", "writer"):
        assert name in nodes
