# main.py

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from graph.graph import app

def main():
    st.title("🩺MedMitra")
    st.write("Ask any healthcare question.")

    # Input widget for the user to enter a question
    question = st.text_input("Please explain the symptoms in detail:", "")

    if question:
        inputs = {"question": question}

        with st.spinner("Processing your question..."):
            try:
                # Initialize the state
                state = {}
                # Run the workflow using app.stream and collect outputs
                for output in app.stream(inputs, config={"configurable": {"thread_id": "2"}}):
                    # Update the state with the outputs
                    state.update(output)
                    print(f"Output from node: {output}")
                    print(f"Updated state: {state}")
                # Debug: print the final state
                print(f"Final state: {state}")
            except Exception as e:
                st.error(f"An error occurred while processing your question: {e}")
                return

        if state:
            # Create two columns under the input field
            col1, col2 = st.columns(2)

            # Access the 'generate' node's outputs
            generate_output = state.get('generate', {})
            retrieve_output = state.get('retrieve', {})

            # Display the answer in the left column
            with col1:
                st.subheader("Answer:")
                generation = generate_output.get('generation')
                if generation:
                    st.write(generation)
                else:
                    st.warning("No generation output available.")

            # Display the context in the right column
            with col2:
                # Try to get context and source from 'generate' output first, then 'retrieve'
                context = generate_output.get('context') or retrieve_output.get('context')
                source = generate_output.get('context_source') or retrieve_output.get('context_source', "Unknown Source")
                st.subheader(f"Context (Source: {source})")
                if context:
                    # Optionally, use an expander for long contexts
                    with st.expander("Show Context"):
                        st.write(context)
                else:
                    st.warning("No context available.")
        else:
            st.warning("No output available from the processing.")

if __name__ == "__main__":
    main()
