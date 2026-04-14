from langgraph.graph import StateGraph, END
from pipeline import AgentState
from pipeline.extractor import extractor_agent
from pipeline.comparator import comparator_agent
from pipeline.scorer import feedback_agent
def should_retry(state: AgentState) -> str:
    return "proceed"
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("extractor", extractor_agent)
    graph.add_node("comparator", comparator_agent)
    graph.add_node("feedback", feedback_agent)

    graph.set_entry_point("extractor")
    graph.add_edge("extractor", "comparator")
    graph.add_conditional_edges(
        "comparator",
        should_retry,
        {
            "retry": "extractor",
            "proceed": "feedback"
        }
    )
    graph.add_edge("feedback", END)

    return graph.compile()