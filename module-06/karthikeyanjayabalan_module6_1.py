#py -m pip install langchain langchain-community langchain-chroma langchain-ollama pypdf docx2txt requests
#py -m pip install sentence-transformers langchain-huggingface


import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 🆕 Updated to use the modern, standalone integration package
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DOCUMENT_PATH = "sample.txt"

def run_local_rag_pipeline(query: str):
    if not os.path.exists(DOCUMENT_PATH):
        print(f"Error: Please create a '{DOCUMENT_PATH}' file in this directory first.")
        return

    print("--- Phase 1: Loading Document Source ---")
    loader = TextLoader(DOCUMENT_PATH)
    documents = loader.load()

    print("--- Phase 2: Chunking Document Text Content ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(documents)
    print(f"Generated {len(text_chunks)} unique text chunks from the document file.")

    print("--- Phase 3: Generating Vector Embeddings Locally (HuggingFace) ---")
    # Using the clean, up-to-date modern class mapping
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("--- Phase 4: Storing Embeddings inside Chroma Vector DB ---")
    vector_db = Chroma.from_documents(text_chunks, embeddings)

    print("--- Phase 5: Retrieving Relevant Context Fragments ---")
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    retrieved_docs = retriever.invoke(query)

    print(f"\n=======================================================")
    print(f" TOP 3 SEARCH CHOICES RETRIEVED FOR: '{query}'")
    print(f"=======================================================")
    for index, doc in enumerate(retrieved_docs, start=1):
        print(f"Choice #{index}:")
        print(f"Content: {doc.page_content.strip()}")
        print("-" * 55)

if __name__ == "__main__":
    # run_local_rag_pipeline("What are the office hours?")
    # run_local_rag_pipeline("what is the id for user02?")
    run_local_rag_pipeline("explain the task details?")
