# 10 · Vector Stores: A Searchable Library of Your Notes

> **In one line:** a vector store saves every chunk **together with its vector**, and quickly finds the chunks **closest in meaning** to a question.

📄 Code: [step10_vector_store.py](../step10_vector_store.py)

```
  LOAD ─► SPLIT ─► EMBED ─► [ STORE ] ─► RETRIEVE
                             ▲ you are here
```

---

## 💡 The idea: a filing cabinet sorted by meaning

```
 ┌──────────────────── 🗄️ Vector store ─────────────────────────────┐
 │  vector                        │  chunk (Document)                 │
 │ ───────────────────────────────┼──────────────────────────────────│
 │ [0.01, -0.04, 0.08, ...]       │ "Mars is called the Red Planet.." │ {source: solar_system.md}
 │ [0.07,  0.02, -0.01, ...]      │ "Photosynthesis is the process.." │ {source: photosynthesis.txt}
 │ [-0.03, 0.05, 0.02, ...]       │ "A list stores many items..."     │ {source: python_basics.md}
 │   ... one row per chunk ...    │                                   │
 └──────────────────────────────────────────────────────────────────┘
```

## 🔨 Two jobs

### Job 1: BUILD (done once, slow)

```
 notes/ ──► load ──► split ──► 12 chunks ──► embed each ──► 🗄️ store ──► 💾 data/notes_index.json
```

```python
vector_store = InMemoryVectorStore.from_documents(chunks, embedding=get_embeddings())
vector_store.dump("data/notes_index.json")   # save to disk
```

### Job 2: SEARCH (done for every question, fast)

```
 "What is the largest planet?"
          │ embed the question
          ▼
 [0.05, -0.01, 0.09, ...] ──► compare with EVERY stored vector ──► top k closest chunks
                                                                   1. "Jupiter is the largest planet..."
                                                                   2. "Saturn is famous for its rings..."
```

```python
vector_store.similarity_search("What is the largest planet?", k=2)              # → 2 Documents
vector_store.similarity_search_with_score("What is the largest planet?", k=3)   # → (Document, score) pairs
```

---

## 💾 Why save to disk?

Creating embeddings **calls the API** (it takes time and uses your free quota). So Study Buddy:

```
 load_vector_store():
      Is data/notes_index.json there?
          ├── YES ──► load it (fast, no API calls for the notes)  ✅
          └── NO  ──► build it, then save it
```

📍 **When you add new notes**, choose **option 5 ("Rebuild the notes index")** in the app. Otherwise, the old index won't know about them.

---

## 🏪 Which vector store?

We use **`InMemoryVectorStore`** because it's built into `langchain-core` (nothing to install) and is perfect for learning.

| Vector store | When it's used |
|---|---|
| `InMemoryVectorStore` ✅ | learning, small projects |
| FAISS / Chroma | bigger local projects |
| Pinecone / pgvector / Qdrant | production apps with millions of chunks |

They all share the **same methods** (`from_documents`, `similarity_search`, `as_retriever`), so switching later means changing about two lines.

## ✅ Remember

- A vector store keeps (vector + chunk + metadata) and searches by meaning.
- Build it once and save it; load it next time.
- Rebuild it when your notes change.

⬅️ [09 · Embeddings](09_embeddings.md) · ➡️ **Next:** [11 · Retrievers & RAG](11_retrievers_rag.md)
