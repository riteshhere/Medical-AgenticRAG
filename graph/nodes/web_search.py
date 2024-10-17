# graph/nodes/web_search.py

from typing import Any, Dict
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from graph.state import GraphState

web_search_tool = TavilySearchResults(k=3)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    print(f"Question: {question}")

    # Perform the web search
    docs = web_search_tool.invoke({"query": question})
    print(f"Web Search Results: {docs}")

    # Extract content from the search results
    web_results_content = [d["content"] for d in docs]

    # Create Document objects from the content
    web_documents = [Document(page_content=content) for content in web_results_content]

    # Append the web search results to the documents list
    if "documents" not in state or state["documents"] is None:
        state["documents"] = []

    state["documents"].extend(web_results_content)  # Store as strings for consistency

    # Combine the web search results into a single string for the context
    state["context"] = "\n\n".join(web_results_content)
    state["context_source"] = "Web Search"

    print(f"Context set in state: {state['context']}")
    print(f"Context source set in state: {state['context_source']}")

    # Return the updated state or necessary outputs
    return {
        "documents": state["documents"],
        "question": question,
        "context": state["context"],
        "context_source": state["context_source"],
    }
