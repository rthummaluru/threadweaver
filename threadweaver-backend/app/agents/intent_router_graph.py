"""
Intent Router Graph for Agentic Workflow    
"""

import logging

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, List, Dict, Any, Optional
from app.prompts.intent_classification_prompt import intent_classification_prompt
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage

class InputRouterState(TypedDict):
    """ Input state for the agentic workflow """

    # Inputs
    session_id: str
    user_id: str
    message: List[BaseMessage]
    user_query: str

    # Routing Decisions
    is_doc_relevant: Optional[bool]
    intent: Optional[Literal["retreive", "action", "hybrid", "conversational"]]
    confidence_score: Optional[float]

    # Retreived Context 
    rag_results: Optional[List[dict]]
    notion_tools: Optional[List[dict]]

    # Response
    assistant_message: Optional[str]
    tool_calls_made: Optional[List[dict]]
    sources_used: Optional[List[str]]


    