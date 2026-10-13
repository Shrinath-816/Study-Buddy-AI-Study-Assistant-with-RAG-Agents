# 06 · Memory: Helping Study Buddy Remember You

> **In one line:** "memory" = **saving** every message, then **sending them all again** with each new question.

📄 Code: [step06_memory.py](../step06_memory.py)

---

## 🤔 The problem

From step 02: **LLMs forget everything between calls.**

```
 You: "Hi! I'm Arjun and I'm studying photosynthesis."
 Bot: "Hi Arjun! Great topic."
 You: "What's my name?"
 Bot: "I don't know your name."      😕  (without memory)
```

## 💡 The idea: a notebook

Study Buddy keeps a **notebook** of the conversation. Before answering, it reads the whole notebook.

```
        ┌──────────── 📓 History notebook ────────────┐
        │ Human: Hi! I'm Arjun, studying photosynth.  │
        │ AI:    Hi Arjun! Great topic.               │
        └──────────────────┬──────────────────────────┘
                           │ ① inserted into the prompt
                           ▼
  ┌──────────────── TUTOR_PROMPT ───────────────────┐
  │ system: You are Study Buddy...                  │
  │ [ MessagesPlaceholder("history") ] ◄── notebook │
  │ human: {question} = "What's my name?"           │
  └──────────────────┬──────────────────────────────┘
                     ▼
                  Gemini ──► "Your name is Arjun!" 😊
                     │
                     │ ② the new question AND answer are written into the notebook
                     ▼
              📓 notebook grows by 2 messages
```

Every turn follows the same cycle: **read the notebook → answer → write to the notebook**.

---

## A) The manual way: a Python list

```python
history = []                                  # 📓 the notebook

answer = chain.invoke({"history": history, "question": question})
history.append(HumanMessage(content=question))  # write the question
history.append(AIMessage(content=answer))       # write the answer
```

Simple, and it shows that memory is **just a list**.

## B) The LangChain way: `RunnableWithMessageHistory`

This wrapper does the reading and writing for you. It also keeps a **separate notebook for each user**, identified by a `session_id`.

```
                          ┌───────── session_store ─────────┐
 config session_id="riya" ├─► 📓 riya:  [I love chemistry..]│
 config session_id="sam"  ├─► 📓 sam:   [I love history...] │
                          └─────────────────────────────────┘

 Riya asks "Which subject do I love?"  → reads ONLY Riya's notebook → "Chemistry!"
 Sam  asks "Which subject do I love?"  → reads ONLY Sam's notebook  → "History!"
```

```python
tutor = RunnableWithMessageHistory(
    chain,
    get_session_history,                 # function: session_id → notebook
    input_messages_key="question",       # which input is the new message
    history_messages_key="history",      # which placeholder receives the notebook
)
tutor.invoke({"question": "Hi, I'm Riya"}, config={"configurable": {"session_id": "riya"}})
```

## C) Memory for agents: a "checkpointer" (step 13)

Agents use `InMemorySaver()` with a `thread_id`. It's the same idea: one notebook per conversation.

📍 **In the app:** option 4 (Chat) remembers what you said earlier in the session, thanks to the checkpointer.

---

## ⚠️ Things to know

| Point | Why it matters |
|---|---|
| The notebook grows every turn | more tokens are sent every call (slower, and uses more quota) |
| `InMemory...` means it's stored in RAM | the memory is lost when the program stops (real apps use a database) |
| Forgetting the `session_id` config | raises an error, because LangChain doesn't know which notebook to use |

## ✅ Remember

- Memory = save the messages, then re-send them every time.
- `MessagesPlaceholder("history")` is where the saved messages go in the prompt.
- `RunnableWithMessageHistory` automates this, with one history per `session_id`.

⬅️ [05 · Chains](05_chains_lcel.md) · ➡️ **Next:** [07 · Document Loaders](07_document_loaders.md)
