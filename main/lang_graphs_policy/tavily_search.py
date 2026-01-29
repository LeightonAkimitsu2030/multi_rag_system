from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

@tool
def web_search(query: str):
    """
    Search the web for real-time information, current events, or general knowledge 
    not found in the local databases.
    """
    # Initialize the tool with specific parameters like result limits
    search = TavilySearchResults(max_results=5)
    
    # Execute the search and return the results as a string for the model
    results = search.invoke({"query": query})
    
    # Formatting the output for better LLM ingestion
    formatted_results = [
        f"Source: {res['url']}\nContent: {res['content']}" 
        for res in results
    ]
    return "\n\n---\n\n".join(formatted_results)