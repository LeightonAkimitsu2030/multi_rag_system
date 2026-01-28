from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from .tavily_search import web_search

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def build_graph():
    # Initialize Gemini Model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    
    # Bind tools to the LLM
    tools = [web_search]
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the node that processes messages through the LLM
    def agent_node(state: AgentState) -> AgentState:
        """Process messages through the Gemini LLM"""
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        
        # Add the assistant's response to the message history
        return {"messages": [response]}
    
    # Build the workflow
    workflow = StateGraph(AgentState)
    
    # Add the agent node
    workflow.add_node("agent", agent_node)
    
    # Connect START to agent node
    workflow.add_edge(START, "agent")
    
    # Connect agent node to END
    workflow.add_edge("agent", END)
    
    # Compile and return the graph
    return workflow.compile()