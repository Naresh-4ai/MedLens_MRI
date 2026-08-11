from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from Agents.classification import classification_agent
from Agents.ocr import ocr_agent
from Agents.medical_info import medical_info_agent
from Agents.timeline import timeline_agent
from Agents.knowledge_base import knowledge_base_agent



class State(TypedDict, total=False):

    uploaded_files: list

    documents: list

    ocr_results: list

    medical_information: list

    medical_timeline: str

    knowledge_base_status: dict

    doctor_query: str

    mri_response: str


graph_builder = StateGraph(State)

graph_builder.add_node("classification", classification_agent)
graph_builder.add_node("ocr", ocr_agent)
graph_builder.add_node("medical_info", medical_info_agent)
graph_builder.add_node("timeline", timeline_agent)
graph_builder.add_node("knowledge_base", knowledge_base_agent)

graph_builder.add_edge(START, "classification")
graph_builder.add_edge("classification", "ocr")
graph_builder.add_edge("ocr", "medical_info")
graph_builder.add_edge("medical_info", "timeline")
graph_builder.add_edge("timeline", "knowledge_base")
graph_builder.add_edge("knowledge_base", END)

graph = graph_builder.compile()