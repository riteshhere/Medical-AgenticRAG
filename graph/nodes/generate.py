# graph/nodes/generate.py

from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState

def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    print(f"Question: {question}")
    documents = state.get("documents", [])
    print(f"Documents: {documents}")

    # Prepare the context by combining the documents into a single string
    context_pieces = []
    if isinstance(documents, list):
        for doc in documents:
            if isinstance(doc, str):
                context_pieces.append(doc)
            elif hasattr(doc, 'page_content'):
                context_pieces.append(doc.page_content)
            else:
                print("Unexpected document format in generate.py")
                print(f"Document: {doc}")
    else:
        context_pieces.append(documents)

    context = "\n\n".join(context_pieces)
    print(f"Context: {context}")

    # Retrieve the context source from state
    context_source = state.get("context_source", "Unknown Source")
    print(f"Context source in generate.py: {context_source}")

    # Invoke the generation chain with the combined context and question
    try:
        generation = generation_chain.invoke({"context": context, "question": question})
        print(f"Generation: {generation}")
    except Exception as e:
        print(f"Exception during generation: {e}")
        generation = None

    # Store the generated answer in the state
    state["generation"] = generation

    # Return the necessary outputs for the Streamlit app
    return {
        "generation": generation,
        "context": context,
        "context_source": context_source,
        "question": question,
        "documents": documents,  # Include documents in outputs
    }
