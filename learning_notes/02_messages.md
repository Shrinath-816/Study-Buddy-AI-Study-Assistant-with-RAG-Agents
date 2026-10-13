# 02 · Messages: The Language of Chat Models

> **In one line:** a chat model doesn't really receive "a question". It receives a **list of messages**, and each message has a **role**.

📄 Code: [step02_messages.py](../step02_messages.py)

---

## 🎭 The three roles

Think of a **theatre play script**:

```
 ┌──────────────────────────────────────────────────────────────────┐
 │ DIRECTOR'S NOTE (SystemMessage)                                  │
 │   "You are Study Buddy, a friendly tutor. Keep answers short."   │  ← rules for the AI
 ├──────────────────────────────────────────────────────────────────┤
 │ STUDENT (HumanMessage):  "My name is Riya. I study planets."     │  ← the user
 │ STUDY BUDDY (AIMessage): "Nice to meet you, Riya!"               │  ← the AI's earlier reply
 │ STUDENT (HumanMessage):  "What is my name?"                      │  ← the new question
 └──────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼  the whole script is sent to Gemini
                       "Your name is Riya!" (a new AIMessage)
```

| Role | Class | Who "says" it | Study Buddy example |
|---|---|---|---|
| system | `SystemMessage` | the developer (you!) | "You are Study Buddy, a patient tutor..." |
| human | `HumanMessage` | the student | "Explain photosynthesis" |
| ai | `AIMessage` | the model | "Photosynthesis is..." |
| tool | `ToolMessage` | a tool's result (step 12) | "Flashcard saved." |

---

## 🧠 The most important fact: LLMs have NO memory

Every call to the LLM starts **completely fresh**. It's like phoning someone who forgets everything the moment you hang up.

```
 Call 1:  [Human: "My name is Riya"]          ──► "Hi Riya!"
 Call 2:  [Human: "What is my name?"]         ──► "I don't know your name." 😕
```

The trick is to **send the earlier conversation again** with every call:

```
 Call 2:  [Human: "My name is Riya",
           AI:    "Hi Riya!",
           Human: "What is my name?"]         ──► "Your name is Riya!" 😊
```

That's all "memory" really is. Step 06 shows how LangChain does this automatically.

---

## 🧩 In code

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="You are Study Buddy, a friendly tutor."),
    HumanMessage(content="My name is Riya and I study the solar system."),
    AIMessage(content="Nice to meet you, Riya!"),
    HumanMessage(content="What is my name?"),
]
response = llm.invoke(messages)   # → "Your name is Riya!"
```

**Shortcut:** tuples work too, and LangChain converts them for you:

```python
llm.invoke([("system", "Answer in one sentence."), ("human", "Why is the sky blue?")])
```

---

## 📍 Where Study Buddy uses messages

- **Every prompt template** (step 03) produces a list of messages behind the scenes.
- **Memory** (step 06) is a growing list of Human and AI messages.
- **The agent** (step 13) works through a list of messages that also includes tool calls and tool results.

## ✅ Remember

- Chat models take a **list of messages** with roles: system, human, ai (and tool).
- The **system message** sets Study Buddy's personality and rules.
- LLMs forget everything between calls, so memory means **re-sending old messages**.

⬅️ [01 · Chat Models](01_chat_models.md) · ➡️ **Next:** [03 · Prompt Templates](03_prompt_templates.md)
