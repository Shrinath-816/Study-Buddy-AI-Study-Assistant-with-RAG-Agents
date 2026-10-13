# 01 · Chat Models: Talking to the LLM

> **In one line:** a *chat model* is LangChain's remote control for an LLM. You press `invoke`, and the LLM answers.

📄 Code: [step01_chat_model.py](../step01_chat_model.py) · ⚙️ Setup: [config.py](../config.py)

---

## 🤔 The problem

Study Buddy needs to ask Gemini questions. Every AI company (Google, OpenAI, Anthropic...) has its **own** way of being called. Learning each one is painful, and switching later means rewriting the app.

## 💡 The idea

LangChain wraps every LLM in a class with the **same buttons**. It's like a universal TV remote: the TV brand doesn't matter, because the buttons are the same.

```
                 ┌───────────────────────────┐
                 │   Same buttons for all:   │
                 │  invoke · stream · batch  │
                 └─────────────┬─────────────┘
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
 ChatGoogleGenerativeAI     ChatOpenAI         ChatAnthropic
      (Gemini) ✅           (GPT)               (Claude)
   ← used in Study Buddy
```

---

## 🧩 Creating the model (in `config.py`)

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",   # which Gemini model to use
    temperature=0.3,            # 0 = focused & factual, 1 = creative
)
```

**Temperature** is like a creativity dial:

```
 0.0 ────────────── 0.3 ─────────────────────── 0.8 ──────── 1.0
 same answer        Study Buddy's normal         mnemonics   wild &
 every time         answers (factual)            (step 03)   random
```

---

## 🔘 The three buttons

### 1) `invoke` → ask once, wait for the full answer

```python
response = llm.invoke("What is an atom?")
print(response.text)
```

```
 "What is an atom?" ──► [ Gemini ] ··· thinking ··· ──► full answer arrives at once
```

### 2) `stream` → get the answer piece by piece

```python
for chunk in llm.stream("Give me 3 study tips"):
    print(chunk.text, end="")
```

```
 "Give me 3 study tips" ──► [ Gemini ] ──► "1." ──► " Take" ──► " short" ──► " breaks..."
                                          (each chunk is printed as soon as it arrives)
```

📍 **Study Buddy uses this** in option 2 (Summarize), so you see the summary appear as it's written, just like ChatGPT.

### 3) `batch` → ask many questions at once

```python
answers = llm.batch(["Capital of Japan?", "12 x 12?"])
```

```
 ["Capital of Japan?", "12 x 12?"] ──► [ Gemini ] ──► [AIMessage("Tokyo"), AIMessage("144")]
                                                      (same order as the questions)
```

---

## 📨 What comes back? An `AIMessage`, not a string

```
 response = llm.invoke("In one sentence, what is photosynthesis?")

 ┌────────────── AIMessage ───────────────────────────────────────┐
 │ .text            → "Photosynthesis is how plants make food..." │  ← what you usually want
 │ .usage_metadata  → {input_tokens: 9, output_tokens: 18, ...}   │  ← how much it "cost"
 │ .response_metadata → model name, finish reason...              │
 └────────────────────────────────────────────────────────────────┘
```

> 💡 **Tokens** are small pieces of words (about ¾ of a word each). API limits and prices are counted in tokens.

---

## ⚠️ Common beginner mistakes

| Mistake | Fix |
|---|---|
| `print(response)` shows a messy object | use `response.text` |
| "API key not found" error | create `.env` from `.env.example` and add `GOOGLE_API_KEY` |
| Answers change every run | that's normal; lower the `temperature` for more consistent answers |

## ✅ Remember

- A chat model = LangChain's wrapper around an LLM.
- `invoke` / `stream` / `batch` work the same on every model, and on every other LangChain block.
- The result is an `AIMessage`; read the text with `.text`.

⬅️ [00 · Big Picture](00_big_picture.md) · ➡️ **Next:** [02 · Messages](02_messages.md)
