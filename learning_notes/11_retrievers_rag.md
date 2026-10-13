# 11 · Retrievers & RAG: Answering From YOUR Notes

> **In one line:** RAG = **find** the relevant chunks of your notes, **paste** them into the prompt, and let Gemini **answer** from them.

📄 Code: [step11_rag.py](../step11_rag.py)

```
  LOAD ─► SPLIT ─► EMBED ─► STORE ─► [ RETRIEVE + GENERATE ]
                                      ▲ you are here
```

---

## 📚 RAG = an open-book exam

```
 Closed-book exam (plain LLM)            Open-book exam (RAG) ✅
 ┌──────────────────────────┐            ┌──────────────────────────────────┐
 │ Answer only from memory  │            │ 1. Look up the right pages       │  ← Retrieval
 │ → might guess or invent  │            │ 2. Put them on the desk          │  ← Augmented
 │   facts ("hallucinate")  │            │ 3. Write the answer from them    │  ← Generation
 └──────────────────────────┘            └──────────────────────────────────┘
```

**R**etrieval **A**ugmented **G**eneration.

---

## 🔎 What is a retriever?

A retriever is a block that takes **a question (string)** and returns **a list of relevant Documents**.

```python
retriever = vector_store.as_retriever(search_kwargs={"k": 4})   # get the top 4 chunks
docs = retriever.invoke("What is a Python list?")
```

Because a retriever is a **Runnable**, it can sit inside an LCEL chain with `|`. That's what makes RAG easy to build.

---

## 🔁 The full RAG flow in Study Buddy (app option 1)

```
 "Why is Venus hotter than Mercury?"
        │
        ├──────────────────────────────┐
        ▼                              ▼
 ┌─────────────┐                 (passed through
 │  RETRIEVER  │                  unchanged)
 └──────┬──────┘                       │
        ▼ 4 Documents                  │
 ┌─────────────┐                       │
 │ format_docs │                       │
 └──────┬──────┘                       │
        ▼ context text                 ▼ question
 ┌───────────────────────── RAG_PROMPT ──────────────────────────┐
 │ system: Answer using ONLY the notes below. If it's not there, │
 │         say "I couldn't find that in your notes."             │
 │         NOTES:                                                │
 │         [Source: solar_system.md]                             │
 │         Venus is the hottest planet... thick CO2 atmosphere...│
 │ human:  Why is Venus hotter than Mercury?                     │
 └──────────────────────────────┬────────────────────────────────┘
                                ▼
                          ┌──────────┐      ┌────────┐
                          │  GEMINI  │ ───► │ PARSER │ ───► "Venus's thick CO2 atmosphere traps
                          └──────────┘      └────────┘       heat (greenhouse effect)...
                                                              Source: solar_system.md"
```

The simple version in code:

```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)
rag_chain.invoke("Why is Venus hotter than Mercury?")
```

> The `{...}` dict at the start runs **both** branches on the same question: one finds the notes (`context`), and the other passes the question along unchanged (`question`).

## 📎 The version with sources (what the app really uses)

`build_rag_chain_with_sources()` **grows a dictionary** step by step with `RunnablePassthrough.assign()`:

```
 "question"
   ──► {docs, question}
   ──► {docs, question, context}           (+ context)
   ──► {docs, question, context, answer}   (+ answer)
```

The app prints `answer` and lists the `source` of each doc.

---

## 🛡️ Why "ONLY use the notes" matters

```
 Q: "Who won the 2010 football World Cup?"   (not in the notes)
 A: "I couldn't find that in your notes."    ✅ honest, and nothing made up
```

## 🎯 Quiz from notes = RAG + structured output (app option 3)

```
 {"topic": "planets"} ──► retriever finds 6 chunks about planets ──► "material"
                                                                         │
                          QUIZ_PROMPT | gemini.with_structured_output(Quiz) ◄┘
                                                                         │
                                                                    Quiz object 🎲
```

## ✅ Remember

- Retriever: question → relevant Documents (it's a Runnable).
- RAG: retrieve → put the chunks into the prompt → generate the answer.
- Tell the model to use **only** the notes, which reduces made-up answers.

⬅️ [10 · Vector Stores](10_vector_store.md) · ➡️ **Next:** [12 · Tools](12_tools.md)
