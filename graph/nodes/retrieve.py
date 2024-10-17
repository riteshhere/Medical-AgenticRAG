# graph/nodes/retrieve.py

from typing import Any, Dict
from langchain.schema import Document  # Make sure Document is imported
from graph.state import GraphState
from ingestion import retriever

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]
    print(f"Question: {question}")

    # Invoke the retriever to get documents (assuming retriever returns a list of Document objects)
    documents = retriever.invoke(question)
    print(f"Retrieved Documents: {documents}")

    # Extract the content from the Document objects
    if documents:
        context_pieces = [doc.page_content for doc in documents if isinstance(doc, Document)]
    else:
        context_pieces = []

    # Combine the document contents into a single string for the context
    context = "\n\n".join(context_pieces)
    state["context"] = context
    print(f"Context set in state: {state['context']}")

    # Indicate the context source
    state["context_source"] = "Vector Store"
    print(f"Context source set in state: {state['context_source']}")

    # Return the updated state or necessary outputs
    return {
        "question": question,
        "documents": documents,
        "context": context,
        "context_source": state["context_source"],
    }
