"""
STEP 10  -  Vector Stores: a searchable database of your notes
==============================================================
📖 Read first: learning_notes/10_vector_store.md  (simple explanation with diagrams)

WHAT IS A VECTOR STORE?
    A database that stores each chunk TOGETHER with its embedding vector, and
    can quickly answer: "which chunks are most similar to this question?"

    Building it:   chunks --(embedding model)--> vectors --> stored
    Searching it:  question --(embedding model)--> vector --> compare --> top matches

WHICH ONE?
    We use InMemoryVectorStore, which is built into langchain-core (nothing extra to
    install) and can save itself to a JSON file.
    Popular "real" options are FAISS, Chroma, Pinecone, pgvector... The good news:
    they all share the same LangChain methods (from_documents, similarity_search,
    as_retriever), so switching later only changes a couple of lines.

WHY SAVE TO DISK?
    Creating embeddings calls the API (costs time and quota). We build the index
    ONCE, save it, and simply load it next time. Rebuild only when your notes change.

Run this file:   python step10_vector_store.py
"""

import os

from langchain_core.vectorstores import InMemoryVectorStore

from config import get_embeddings, VECTOR_STORE_PATH
from step07_document_loaders import load_notes
from step08_text_splitters import split_documents


def build_vector_store() -> InMemoryVectorStore:
    """Load notes -> split -> embed -> store, then save to disk."""
    documents = load_notes()
    chunks = split_documents(documents)
    print(f"Building index: {len(documents)} documents -> {len(chunks)} chunks. Creating embeddings...")

    # from_documents() embeds every chunk with the embedding model and stores it.
    vector_store = InMemoryVectorStore.from_documents(chunks, embedding=get_embeddings())

    # Save it so we don't have to rebuild every time.
    os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
    vector_store.dump(VECTOR_STORE_PATH)
    print(f"Index saved to {VECTOR_STORE_PATH}")
    return vector_store


def load_vector_store() -> InMemoryVectorStore:
    """
    Load the saved index if it exists, otherwise build it.
    Note: we must pass the SAME embedding model that built it, because new
    questions need to be turned into vectors the same way.
    """
    if os.path.exists(VECTOR_STORE_PATH):
        return InMemoryVectorStore.load(VECTOR_STORE_PATH, embedding=get_embeddings())
    return build_vector_store()


if __name__ == "__main__":
    vector_store = build_vector_store()

    question = "What is the largest planet?"

    print(f"\n=== 1. similarity_search('{question}') ===")
    # Returns the k most similar chunks as Documents.
    results = vector_store.similarity_search(question, k=2)
    for doc in results:
        print(f"[{doc.metadata['source']}] {doc.page_content[:150]} ...\n")

    print(f"=== 2. similarity_search_with_score (higher score = more similar) ===")
    for doc, score in vector_store.similarity_search_with_score(question, k=3):
        print(f"  score {score:.3f}  [{doc.metadata['source']}]  {doc.page_content[:70]!r}")
