# 12 · Tools: Giving Study Buddy Hands

> **In one line:** a tool is a **Python function the LLM can ask your program to run**.

📄 Code: [step12_tools.py](../step12_tools.py)

---

## 🤔 The problem

An LLM can only **write text**. It can't:

- 🔍 search your notes folder
- 🧮 do exact maths (LLMs often make arithmetic mistakes!)
- 💾 save a flashcard to a file

## 💡 The idea: the brain and the hands

```
   🧠 Gemini (the brain)                    🖐️ Your Python code (the hands)
   "I need to multiply 17.5 × 4.2.     ──►   runs calculate(17.5, 4.2, "multiply")
    Please run the calculate tool."    ◄──   "73.5"
   "The answer is 73.5."
```

> ⚠️ **Key point:** the model **never runs the tool itself**. It only *asks*. Your code runs it and sends back the result.

---

## 🧰 Study Buddy's four tools

| Tool | What it does | Example request |
|---|---|---|
| `search_my_notes(query)` | searches your notes (the retriever from step 11) | "What do my notes say about Mars?" |
| `calculate(a, b, operation)` | exact maths | "What's 11.2 × 12742?" |
| `save_flashcard(question, answer)` | saves a flashcard to `data/flashcards.txt` | "Save a flashcard about photosynthesis" |
| `show_flashcards()` | shows saved flashcards | "Show my flashcards" |

## 🏷️ The `@tool` decorator

```python
@tool
def calculate(a: float, b: float, operation: str) -> float:
    """Do exact maths on two numbers.
    operation must be one of: 'add', 'subtract', 'multiply', 'divide', 'power'."""
    ...
```

LangChain reads three things from your function and sends them to Gemini:

```
 def calculate(a: float, b: float, operation: str)
     ────┬────  ─────────────┬──────────────────
         │                   └──► ARGUMENTS:   a (number), b (number), operation (text)
         └──────────────────────► NAME:        "calculate"
 """Do exact maths on two numbers..."""
 ──────────────┬────────────────────────
               └────────────────► DESCRIPTION: Gemini reads this to decide WHEN to use the tool!
```

> 💡 **The docstring is the most important part.** A vague description means Gemini won't know when to use the tool.

---

## 🔄 The tool-calling cycle (done by hand in step 12)

```
 ① llm.bind_tools(STUDY_TOOLS)          → "Gemini, these 4 tools exist."

 ② You: "What is 17.5 multiplied by 4.2?"
           │
           ▼
 ③ Gemini replies with a TOOL CALL (not an answer!):
    AIMessage(tool_calls=[{"name": "calculate",
                           "args": {"a": 17.5, "b": 4.2, "operation": "multiply"},
                           "id": "call_1"}])
           │
           ▼
 ④ YOUR CODE runs it:  calculate.invoke(tool_call)  →  ToolMessage("73.5", tool_call_id="call_1")
           │
           ▼
 ⑤ Send ALL the messages back:  [Human, AIMessage(tool call), ToolMessage]
           │
           ▼
 ⑥ Gemini: "17.5 multiplied by 4.2 is 73.5."   ✅ final answer
```

The message list grows like this:

```
 [ HumanMessage  "What is 17.5 × 4.2?" ]
 [ AIMessage     tool_calls: calculate(...) ]     ← the model asks
 [ ToolMessage   "73.5" ]                         ← your code answers
 [ AIMessage     "The answer is 73.5." ]          ← the final reply
```

Doing this cycle by hand gets tedious, especially when the model needs **several** tools one after another. That's exactly what an **agent** automates (next step).

## ✅ Remember

- `@tool` turns a function into a tool; the **docstring** tells the model when to use it.
- `bind_tools()` tells the model which tools exist.
- The model **asks** (a tool call), your code **runs** it, and the result goes back as a `ToolMessage`.

⬅️ [11 · Retrievers & RAG](11_retrievers_rag.md) · ➡️ **Next:** [13 · Agents](13_agents.md)
