
from IPython.display import display, Image

from typing_extensions import TypedDict
from typing import Literal
import random

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str

def node1(state: State) -> State:
    print("--- node1 ---")
    return {"graph_state": state['graph_state'] + " Ich bin"}

def node2(state: State) -> State:
    print("--- node2 ---")
    return {"graph_state": state['graph_state'] + " fröhlich!"}

def node3(state: State) -> State:
    print("--- node3 ---")
    return {"graph_state": state['graph_state'] + " traurig!"}

def set_mood(state: State) -> Literal["NODE2", "NODE3"]:
    print("--- set_mood ---")
    if random.random() > 0.5:
        return "NODE2"

    return "NODE3"

builder = StateGraph(State, "graph_state")
builder.add_node("NODE1", node1)
builder.add_node("NODE2", node2)
builder.add_node("NODE3", node3)

builder.add_edge(START, "NODE1")
builder.add_conditional_edges("NODE1", set_mood)
builder.add_edge("NODE2", END)
builder.add_edge("NODE3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

