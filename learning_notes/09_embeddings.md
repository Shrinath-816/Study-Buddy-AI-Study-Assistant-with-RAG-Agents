# 09 · Embeddings: Turning Meaning Into Numbers

> **In one line:** an embedding model turns text into a list of numbers (a **vector**), so that texts with **similar meaning** get **similar numbers**.

📄 Code: [step09_embeddings.py](../step09_embeddings.py)

```
  LOAD ─► SPLIT ─► [ EMBED ] ─► STORE ─► RETRIEVE
                    ▲ you are here
```

---

## 🤔 The problem: keyword search isn't enough

A student asks: **"How do plants make their food?"**

The right chunk in `photosynthesis.txt` says: *"Photosynthesis is the process by which green plants... make their own food using light energy..."*

A word-matching search compares only the words. But a student might ask *"how do leaves turn sunlight into energy?"*, which shares almost **no words** with the notes. We need a search that understands **meaning**.

## 💡 The idea: a map of meanings

Imagine every sentence placed as a **dot on a map**, where sentences with similar meanings sit **close together**:

```
          ▲
          │  🌱 "Photosynthesis happens in leaves"
          │     🌱 "How do plants make their food?"      ← close together = similar meaning
          │
          │                                   🪐 "Jupiter is the largest planet"
          │                                      🪐 "Which planet is biggest?"
          │
          │     🐍 "A for loop repeats code"
          └──────────────────────────────────────────────►
```

An embedding is a sentence's **position** on that map. Real embeddings have ~3000 directions instead of 2, but the idea is the same.

```
 "Plants use sunlight to make food."
                │
                ▼  embedding model (gemini-embedding-001)
 [0.0123, -0.0456, 0.0871, 0.0032, -0.0219, ... about 3000 numbers]
```

---

## 🧩 Two methods

```python
embeddings = get_embeddings()

embeddings.embed_query("How do plants make their food?")        # ONE vector (for the question)
embeddings.embed_documents(["chunk 1 text", "chunk 2 text"])    # MANY vectors (for the notes)
```

## 📏 Measuring "closeness": cosine similarity

```
 Question: "How do plants make their food?"

   similarity 0.82  ◄── "Photosynthesis happens in the leaves using sunlight..."   🥇
   similarity 0.41  ◄── "Jupiter is the largest planet in the solar system."
   similarity 0.38  ◄── "A for loop repeats a block of code several times."

 1.0 = same meaning      ~0 = unrelated
```

(The numbers above are only an example; yours will be a little different.)

The photosynthesis sentence wins, **even though it uses different words**. 🎉

> 💡 You don't have to calculate this yourself. The vector store (step 10) does it for you.

---

## ⚠️ Important rule

Use the **same embedding model** for your notes **and** your questions. Different models create different "maps", and their positions can't be compared.

## ✅ Remember

- Embedding = text turned into a vector of numbers that captures its **meaning**.
- Similar meaning → nearby vectors → high similarity score.
- `embed_query` for questions, `embed_documents` for the chunks.

⬅️ [08 · Text Splitters](08_text_splitters.md) · ➡️ **Next:** [10 · Vector Stores](10_vector_store.md)
