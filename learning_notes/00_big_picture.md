# 00 · The Big Picture: What is LangChain?

> **In one line:** LangChain is a toolbox of ready-made building blocks for making apps that use an LLM, like our **Study Buddy**.

---

## 🤔 First, what is an LLM?

An **LLM** (Large Language Model) is an AI that has read a huge amount of text and can **read text and write text**. Google **Gemini**, used in this project, is an LLM.

```
   "Explain photosynthesis simply"          "Plants use sunlight to turn water
   ───────────────────────────────►  LLM  ─────────────────────────────────►
            (text in)                       and air into food..."  (text out)
```

That's all an LLM can do on its own. It **cannot**:

| ❌ An LLM alone cannot... | ✅ So in Study Buddy, LangChain helps us... |
|---|---|
| remember your last message | add **memory** (step 06) |
| read *your* notes folder | **load, split, search** your notes (steps 07–11) |
| reliably return a quiz as clean data | get **structured output** (step 04) |
| do exact maths or save a file | give it **tools** (step 12) |
| decide on its own to "search, then save a flashcard" | build an **agent** (step 13) |
| show you why it gave a wrong answer | **trace** every step with LangSmith (step 14) |

---

## 🧱 LangChain = LEGO blocks for AI apps

Think of LangChain like a box of **LEGO blocks**. Each block does one job, and every block has the **same connector shape**, so any block can snap onto any other.

```
 ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
 │  Prompt  │──►│  Model   │──►│  Parser  │──►│  Answer  │
 │ Template │   │ (Gemini) │   │          │   │          │
 └──────────┘   └──────────┘   └──────────┘   └──────────┘
   fill the       the LLM        clean up
   blanks         thinks         the output
```

In LangChain, that shared "connector shape" is called a **Runnable**. Every Runnable has the same three methods:

| Method | Meaning | Study Buddy example |
|---|---|---|
| `.invoke(x)` | run once, wait for the full result | answer one question |
| `.stream(x)` | run once, get the result piece by piece | show the summary word by word |
| `.batch([x, y])` | run many at once | explain 5 topics together |

You'll see these three methods on **every** block in this project.

---

## 🗺️ The map of Study Buddy

Here's every concept in the project, and where it sits in the app:

```
                         ┌───────────────────────────┐
                         │      YOU (the student)    │
                         └─────────────┬─────────────┘
                                       │ question / command
                                       ▼
 ┌─────────────────────────────────── main.py ───────────────────────────────────┐
 │                                                                               │
 │   1. Ask notes      2. Summarize       3. Quiz me        4. Chat (agent)      │
 │      (RAG)             (chain)            (RAG+struct)      (agent+tools)     │
 └──────┬──────────────────┬──────────────────┬─────────────────────┬────────────┘
        │                  │                  │                     │
        ▼                  ▼                  ▼                     ▼
 ┌─────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐
 │ Retriever   │   │ Prompt       │   │ Retriever    │   │ Agent loop           │
 │ (step 11)   │   │ Template(03) │   │ + Quiz chain │   │ (step 13)            │
 │     │       │   │     │        │   │ (04, 05, 11) │   │  ├─ search_my_notes  │
 │     ▼       │   │     ▼        │   └──────────────┘   │  ├─ calculate        │
 │ Vector store│   │ Chat model   │                      │  ├─ save_flashcard   │
 │ (step 10)   │   │ (01, 02)     │                      │  └─ show_flashcards  │
 └─────┬───────┘   │     │        │                      │     (tools, step 12) │
       │           │     ▼        │                      └──────────────────────┘
       │           │ Output parser│
       │           │ (step 04)    │
       │           └──────────────┘
       ▼
 ┌────────────────────────────────────────────────┐
 │ notes/ ─► Loader ─► Splitter ─► Embeddings     │   ← built once, then saved
 │           (07)       (08)        (09)          │
 └────────────────────────────────────────────────┘

   Everything above is recorded in LangSmith (step 14) so you can inspect it.
```

---

## 📦 The packages we use

| Package | What's inside |
|---|---|
| `langchain-core` | the basic blocks: messages, prompts, parsers, Runnables, vector store |
| `langchain` | higher-level features, such as `create_agent` |
| `langchain-google-genai` | the "plug" that connects LangChain to **Gemini** |
| `langchain-text-splitters` | tools to cut long text into chunks |
| `langsmith` | sends traces of your app to the LangSmith website |

> 💡 **Why the "plug" package matters:** to switch from Gemini to OpenAI, you'd swap `langchain-google-genai` for `langchain-openai` and change **only `config.py`**. Every other file stays the same.

---

## 🚶 How to study this project

For each step, do these three things:

```
  ① Read the note           ② Read the code            ③ Run it
  learning_notes/NN_*.md ─► stepNN_*.py comments ─► python stepNN_*.py
                                                          │
                     ④ (optional) look at the trace in LangSmith ◄┘
```

➡️ **Next:** [01 · Chat Models](01_chat_models.md)
