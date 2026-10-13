# 08 · Text Splitters: Cutting Notes Into Chunks

> **In one line:** a text splitter cuts long documents into **small, overlapping pieces** called *chunks*.

📄 Code: [step08_text_splitters.py](../step08_text_splitters.py)

```
  LOAD ─► [ SPLIT ] ─► EMBED ─► STORE ─► RETRIEVE
           ▲ you are here
```

---

## 🤔 Why split at all?

Say you ask: *"How tall is Olympus Mons?"*

```
 ❌ Without splitting                         ✅ With splitting
 ┌─────────────────────────────┐            ┌──────────┐ ┌──────────┐ ┌──────────┐
 │ the WHOLE solar_system.md   │            │ Overview │ │ Mars,    │ │ Jupiter, │
 │ (Sun, Mercury, Venus, Earth,│            │ & Sun    │ │ Olympus  │ │ Saturn   │
 │  Mars, Jupiter, Saturn...)  │            │          │ │ Mons ✔   │ │          │
 └─────────────────────────────┘            └──────────┘ └──────────┘ └──────────┘
 sent to Gemini every time:                 only the Mars chunk is sent:
 slow, costly, answer gets "lost"           fast, cheap, focused
```

1. **Focus:** only the relevant part of your notes reaches Gemini.
2. **Cost and speed:** fewer tokens per call.
3. **Better search:** a small chunk about one idea is easier to match than a whole file.

---

## ✂️ `RecursiveCharacterTextSplitter`, the most popular splitter

It tries to cut at **natural boundaries**, in this order:

```
 1st try: between paragraphs   "\n\n"
 2nd try: between lines        "\n"
 3rd try: between words        " "
 last:    between characters   ""      (only if nothing else fits)
```

So chunks usually end at the end of a paragraph or sentence, not in the middle of a word.

## 🎚️ Two settings

```python
RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
```

- `chunk_size`: the **maximum** number of characters per chunk.
- `chunk_overlap`: how many characters **repeat** between neighbouring chunks.

**Why overlap?** So an idea that falls on a border isn't cut in half and lost:

```
 Original: "Mitochondria are the powerhouse of the cell. They produce energy. Chloroplasts..."

 Chunk 1: [Mitochondria are the powerhouse of the cell. They produce]
 Chunk 2:                                            [They produce energy. Chloroplasts are...]
                                                      └── overlap ──┘
                                                      (appears in both chunks)
```

---

## 📍 In Study Buddy

```
 3 Documents (3 notes files) ──► split_documents() ──► ~12 chunks
```

Each chunk is **still a `Document`**, and it **keeps its parent's metadata** (plus a `start_index` showing where it began):

```
 { "source": "solar_system.md", "start_index": 1450 }
 "Mars is called the Red Planet because of iron oxide (rust)..."
```

---

## 🎛️ Choosing the numbers

| chunk_size | Effect |
|---|---|
| too small (e.g. 100) | chunks lose context ("It is 22 km high." What is?) |
| too big (e.g. 5000) | search gets fuzzy, and many tokens are wasted |
| **~500–1000** ✅ | a good starting point for notes |

Overlap is usually **10–20%** of `chunk_size`.

## ✅ Remember

- Splitting = cutting documents into small chunks for focused search and fewer tokens.
- `RecursiveCharacterTextSplitter` cuts at paragraphs, then lines, then words.
- Overlap keeps ideas on a border from being lost; metadata is kept on every chunk.

⬅️ [07 · Document Loaders](07_document_loaders.md) · ➡️ **Next:** [09 · Embeddings](09_embeddings.md)
