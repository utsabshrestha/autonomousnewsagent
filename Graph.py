from langgraph.graph import StateGraph, START, END
import GraphStates as states
import Node as node

builder = StateGraph(states.AgentState)
builder.add_node("planner", node.PlannerNode)
builder.add_node("SearchNode", node.SearchNode)
builder.add_node("deduplicate", node.RemoveDuplicateSearchResults)
builder.add_node("gather_results", lambda state : state)
builder.add_node("SearchResultsEvaluation", node.SearchResultsEvaluationNode)
builder.add_node("ScrapeDispatch", lambda state: state)
builder.add_node("ScrapeNode", node.ScrapeNode)
builder.add_node("ReporterNode", node.ReporterNode)

builder.add_edge(START, "planner")
builder.add_conditional_edges("planner", node.Route_to_SearchNode, ["SearchNode"])
builder.add_edge("SearchNode", "gather_results")
builder.add_edge("gather_results", "deduplicate")
builder.add_edge("deduplicate", "SearchResultsEvaluation")
builder.add_conditional_edges("SearchResultsEvaluation", 
                              node.Check_Sufficient_Urls, 
                              {
                                  "planner": "planner",
                                  "ScrapeNode": "ScrapeDispatch"
                              })

builder.add_conditional_edges("ScrapeDispatch", node.Route_to_ScrapeNode, ["ScrapeNode"])
builder.add_edge("ScrapeNode", "ReporterNode") # Wait, this needs to gather!
builder.add_edge("ReporterNode", END)

graph = builder.compile()


