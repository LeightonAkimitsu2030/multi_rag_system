from lang_graphs_policy.workflow_graphs import build_graph
from langchain_core.messages import HumanMessage

class ChatbotManager:
    def __init__(self):
        # Build the LangGraph agent once during initialization
        self.app = build_graph()

    def get_response(self, user_input: str, history=None):
        """
        Processes the user input through the agent graph and returns the final answer.
        """
        # Prepare the state for the graph
        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }
        
        # Invoke the graph. The agent will decide whether to use 
        # RAG tools or Tavily web search
        final_state = self.app.invoke(initial_state)
        
        # Retrieve the last message from the AI in the conversation
        return final_state["messages"][-1].content