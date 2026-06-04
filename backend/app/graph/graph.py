import sqlite3
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.sqlite import SqliteSaver
from app.graph.state import RehearsalState
from app.graph.nodes import generate_response, process_feedback

conn = sqlite3.connect("./rehearsal.db", check_same_thread=False)
memory = SqliteSaver(conn)

def create_graph():
    graph = StateGraph(RehearsalState)
    
    graph.add_node("generate_response", generate_response)
    graph.add_node("process_feedback", process_feedback)
    
    graph.add_conditional_edges(
        START,
        lambda state: state["next_node"],
        {
            "generate_response": "generate_response",
            "process_feedback": "process_feedback"
        }
    )
    
    graph.add_edge("generate_response", END)
    graph.add_edge("process_feedback", END)
    
    return graph.compile(checkpointer=memory)

rehearsal_graph = create_graph()