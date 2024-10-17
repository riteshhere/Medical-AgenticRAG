from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document  # Import Document to wrap text properly
import os
from PyPDF2 import PdfReader  # Import PyPDF2 for reading PDFs

load_dotenv()

# Directory where the vector store will be persisted
persist_directory = "./vectordb"  # Changed to 'vectordb'

# Function to load and extract text from PDF files using PyPDF2
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()  # Extract text from each page
    return text

# Check if the vector store already exists
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    print("Vector store already exists. Loading existing vector store...")

    # Load the existing vector store and initialize the retriever
    retriever = Chroma(
        collection_name="rag-chroma",
        persist_directory=persist_directory,
        embedding_function=OpenAIEmbeddings(),
    ).as_retriever()

else:
    print("Vector store does not exist. Ingesting PDF documents and creating a new vector store...")

    # Directory where your PDFs are stored
    pdf_dir = "./knowledge"

    # Load all PDFs from the directory and extract text using PyPDF2
    docs_list = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, file)
            print(f"Loading and extracting document: {file_path}")
            text = load_pdf(file_path)  # Load and extract text from PDF
            # Wrap the extracted text in a Document object
            doc = Document(page_content=text, metadata={"source": file_path})
            docs_list.append(doc)

    # Initialize the text splitter to chunk large documents
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Create the Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_directory,  # Store the vector store in './vectordb'
    )

    # Initialize the retriever for querying
    retriever = Chroma(
        collection_name="rag-chroma",
        persist_directory=persist_directory,
        embedding_function=OpenAIEmbeddings(),
    ).as_retriever()

    print("PDF documents ingested and vector store created successfully.")
