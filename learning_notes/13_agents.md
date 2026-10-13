# 13 · Agents: Study Buddy Decides What To Do

> **In one line:** an agent is an LLM that **decides by itself** which tools to use, in a **loop**, until it can answer.

📄 Code: [step13_agent.py](../step13_agent.py)

---

## 🚂 Chain vs 🚕 Agent

```
 CHAIN = a train on fixed tracks               AGENT = a taxi driver
 You decide the route in advance.              You give a destination;
                                               the driver picks the route.

 prompt ──► llm ──► parser                     "Find Jupiter in my notes and save a flashcard"
 (always the same steps)                        → the driver decides: search notes → save flashcard → answer
```

| | Chain | Agent |
|---|---|---|
| Who decides the steps? | you (the programmer) | the LLM |
| Number of steps | fixed | changes with each question |
| Study Buddy example | Summarize, Ask notes, Quiz | **Chat (option 4)** |

---

## 🔁 The agent loop

```
                      ┌─────────────────────────────────┐
  your message ─────► │        🧠 MODEL (Gemini)        │
                      │  "Do I need a tool?"            │
                      └───────┬─────────────────┬───────┘
                       YES    │                 │   NO
                              ▼                 ▼
                      ┌──────────────┐    ✅ FINAL ANSWER ──► you
                      │ 🖐️ RUN TOOL  │
                      │ (our code)   │
                      └──────┬───────┘
                             │ result (ToolMessage)
                             └──────────► back to the MODEL ↺
```

It's the same cycle as step 12, but **repeated automatically** until the model is done.

## 🎬 A real example

**You:** *"Find the largest planet in my notes and save a flashcard about it."*

```
 Round 1  🧠 "First I'll search the notes."   ──► 🖐️ search_my_notes("largest planet")
                                               ◄── "[solar_system.md] Jupiter is the largest planet..."
 Round 2  🧠 "Now save the flashcard."        ──► 🖐️ save_flashcard("Largest planet?", "Jupiter...")
                                               ◄── "Flashcard saved."
 Round 3  🧠 "I have everything I need."      ──► ✅ "Jupiter is the largest planet (from
                                                     solar_system.md). I saved a flashcard for you!"
```

Nobody told it to use **two** tools **in that order**. It worked that out by itself. 🤯

---

## 🧩 Building it: `create_agent`

```python
agent = create_agent(
    model=get_chat_model(),          # 🧠 the brain
    tools=STUDY_TOOLS,               # 🖐️ the hands (step 12)
    system_prompt=AGENT_SYSTEM_PROMPT,  # 📜 the rules: when to use which tool
    checkpointer=InMemorySaver(),    # 📓 memory (see below)
)
```

Using it:

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Show my flashcards"}]},
    config={"configurable": {"thread_id": "student-1"}},
)
result["messages"][-1].text    # the last message = the final answer
```

## 📓 Agent memory: checkpointer + thread_id

```
 thread_id = "student-1"
 ┌───────────── InMemorySaver ──────────────┐
 │ "My exam is on Friday, I struggle with   │
 │  Python loops."                          │
 │ "Good luck! Loops are..."                │
 └──────────────────────────────────────────┘
 later: "What did I say I struggle with?" ──► "Python loops!" ✅
```

📍 In `main.py` the agent is created **once**, so it remembers the whole chat session.

> 🔧 Under the hood, `create_agent` runs on **LangGraph**, LangChain's engine for loops and multi-step workflows. You don't need to learn LangGraph to use it.

## 👀 Watching it think

`watch_agent_think()` in step 13 uses `agent.stream(..., stream_mode="updates")` to print every decision as it happens. **LangSmith (step 14)** shows the same thing visually, as a tree.

## ✅ Remember

- Agent = model + tools + a loop; the **model** chooses the steps.
- `create_agent(model, tools, system_prompt, checkpointer)`.
- Memory comes from the checkpointer, with one `thread_id` per conversation.

⬅️ [12 · Tools](12_tools.md) · ➡️ **Next:** [14 · LangSmith Tracing](14_langsmith_tracing.md)
