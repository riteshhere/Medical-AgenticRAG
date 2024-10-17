# graph/state.py

from typing import List, TypedDict, Optional, Any

class GraphState(TypedDict, total=False):
    """
    Represents the state of our graph.

    Attributes:
        question: The input question.
        generation: The generated answer.
        web_search: Whether to add web search.
        documents: List of documents retrieved.
        context: Combined context from retrieval or web search.
        context_source: Source of the context (e.g., 'Vector Store', 'Web Search').
    """

    question: str
    generation: Optional[str]
    web_search: Optional[bool]
    documents: Optional[List[Any]] 
    context: Optional[str]
    context_source: Optional[str]
