# 07 · Document Loaders: Reading Your Notes

> **In one line:** a document loader reads files (or websites, databases...) and turns them into LangChain **`Document`** objects.

📄 Code: [step07_document_loaders.py](../step07_document_loaders.py)

---

## 🚀 Starting the RAG journey (steps 07 → 11)

Gemini has **never seen your notes**. To answer *"Why is Venus hotter than Mercury?"* from **your** notes, Study Buddy needs to build a searchable library first. That takes 5 steps:

```
  ┌──────┐    ┌───────┐    ┌───────┐    ┌───────┐    ┌──────────┐
  │ LOAD │ ─► │ SPLIT │ ─► │ EMBED │ ─► │ STORE │ ─► │ RETRIEVE │ ─► answer with Gemini
  └──────┘    └───────┘    └───────┘    └───────┘    └──────────┘
   step 07     step 08      step 09      step 10      step 11
   ▲ you are here
```

Think of it as setting up a **school library**:

| Library | Study Buddy |
|---|---|
| bring the books in | **Load** your notes files |
| cut them into index cards | **Split** them into chunks |
| give every card a "topic code" | **Embed** each chunk as a vector |
| file the cards in a cabinet | **Store** them in a vector store |
| the librarian finds the right cards | **Retrieve** the chunks for a question |

---

## 📄 What is a `Document`?

A `Document` is an envelope: **the text** inside, and **a label** on the outside.

```
 ┌──────────────────── Document ──────────────────────┐
 │ metadata:  {"source": "solar_system.md"}           │  ← the label: where it came from
 │ ─────────────────────────────────────────────────  │
 │ page_content:                                      │  ← the actual text
 │   "# The Solar System                              │
 │    The Solar System formed about 4.6 billion..."   │
 └────────────────────────────────────────────────────┘
```

> 💡 **Why metadata matters:** it's how Study Buddy can say *"Source: solar_system.md"* under an answer.

---

## 🧩 Our loader: `StudyNotesLoader`

LangChain has hundreds of ready-made loaders (PDF, websites, YouTube, Notion...). We wrote a small one ourselves so you can see that **there is no magic**:

```
 notes/
 ├── photosynthesis.txt  ──► 1 Document  {source: photosynthesis.txt}
 ├── python_basics.md    ──► 1 Document  {source: python_basics.md}
 ├── solar_system.md     ──► 1 Document  {source: solar_system.md}
 └── my_book.pdf (3 pg)  ──► 3 Documents {source: my_book.pdf, page: 1}
                                         {source: my_book.pdf, page: 2}
                                         {source: my_book.pdf, page: 3}
```

```python
class StudyNotesLoader(BaseLoader):           # extend LangChain's base class
    def lazy_load(self):                      # we only write this method
        for file_path in folder:
            if .txt or .md:  yield Document(page_content=text, metadata={"source": name})
            if .pdf:         yield one Document per page (with "page" in metadata)

docs = StudyNotesLoader("notes").load()      # .load() comes free from BaseLoader
```

> `yield` hands back **one Document at a time** ("lazy" loading), which saves memory with big folders.

---

## ✅ Remember

- A `Document` = `page_content` (text) + `metadata` (label).
- Loaders turn files into Documents, and every loader has `.load()`.
- Metadata travels with the text all the way to the answer, which is how Study Buddy shows sources.

⬅️ [06 · Memory](06_memory.md) · ➡️ **Next:** [08 · Text Splitters](08_text_splitters.md)
