# 03 · Prompt Templates: Prompts With Blanks

> **In one line:** a prompt template is a **fill-in-the-blanks form** for prompts. Write it once, then reuse it with different values.

📄 Code: [step03_prompt_templates.py](../step03_prompt_templates.py)

---

## 🤔 The problem

Study Buddy explains **any** topic for **any** level. We don't want to write a new prompt every time. Most of the prompt stays the same, and only a few words change:

```
 "You are Study Buddy... Explain for a ________ student.  Please explain: ________"
                                       ▲  level                           ▲  topic
```

## 💡 The idea: a form with blanks

```
       TEMPLATE (written once)                         VALUES (change every time)
 ┌─────────────────────────────────────────┐        ┌──────────────────────────┐
 │ system: You are Study Buddy... Explain  │        │ level = "beginner"       │
 │         topics for a {level} student.   │   +    │ topic = "electric        │
 │ human:  Please explain: {topic}         │        │          current"        │
 └─────────────────────────────────────────┘        └──────────────────────────┘
                      │  .invoke({...})
                      ▼
 ┌──────────────────────────────────────────────────────────┐
 │ [system] You are Study Buddy... for a beginner student.  │   ready-to-send
 │ [human]  Please explain: electric current                │   messages
 └──────────────────────────────────────────────────────────┘
                      │
                      ▼
                  Gemini 🤖
```

> ⚠️ A template **does not call the LLM**. It only **prepares** the input.

---

## 🧩 The four kinds you'll meet

### 1) `PromptTemplate`: produces a single text string

```python
template = PromptTemplate.from_template("Explain {topic} to a {level} student in 3 bullet points.")
template.invoke({"topic": "gravity", "level": "beginner"})
# → "Explain gravity to a beginner student in 3 bullet points."
```

### 2) `ChatPromptTemplate`: produces a list of messages ⭐ (used most)

```python
EXPLAIN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Study Buddy, a patient tutor. Explain topics for a {level} student."),
    ("human", "Please explain: {topic}"),
])
```

📍 Study Buddy has a template for **every feature**:

| Template | File | Blanks |
|---|---|---|
| `EXPLAIN_PROMPT` | step 03 | `{level}`, `{topic}` |
| `SUMMARY_PROMPT` | step 05 | `{notes}` |
| `QUIZ_PROMPT` | step 05 | `{num_questions}`, `{material}`, `{topic}` |
| `RAG_PROMPT` | step 11 | `{context}`, `{question}` |
| `TUTOR_PROMPT` | step 06 | `{history}`, `{question}` |

### 3) Few-shot: teach by example

Instead of describing the style you want, **show** a couple of examples. The model copies the pattern.

```
 [system] You create short memory tricks.
 [human]  Order of the planets            ┐
 [ai]     My Very Educated Mother...      │  example 1
 [human]  Colours of the rainbow          │
 [ai]     ROY G BIV                       ┘  example 2
 [human]  {topic}                         ←  the real question
                │
                ▼
 Gemini answers in the SAME style ✨
```

### 4) `MessagesPlaceholder`: a slot for a whole list of messages

Some blanks hold a **list of messages** rather than a single word. The chat history (step 06) is the main example:

```
 ┌───────────────────────────────────────┐
 │ system: You are Study Buddy...        │
 │ ┌───────────────────────────────────┐ │
 │ │ MessagesPlaceholder("history")    │ │ ◄── [Human: "I'm learning cells",
 │ │  (any number of messages go here) │ │      AI: "Great! Cells are..."]
 │ └───────────────────────────────────┘ │
 │ human: {question}                     │
 └───────────────────────────────────────┘
```

---

## ⚠️ Common beginner mistakes

| Mistake | Fix |
|---|---|
| `KeyError: missing variable 'level'` | pass **every** blank: `.invoke({"topic": ..., "level": ...})` |
| You need a literal `{` in the prompt (e.g. for JSON) | write `{{` and `}}` (see step 04) |
| Writing prompts with f-strings everywhere | use templates, so they're reusable and visible in LangSmith |

## ✅ Remember

- A template = a prompt with `{blanks}`; `.invoke({...})` fills them.
- `ChatPromptTemplate` builds the **messages** (system, human, ai).
- Few-shot examples show the model the style you want.
- `MessagesPlaceholder` is a slot for a list of messages, such as the chat history.

⬅️ [02 · Messages](02_messages.md) · ➡️ **Next:** [04 · Output Parsers](04_output_parsers.md)
