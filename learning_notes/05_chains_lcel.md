# 05 · Chains with LCEL: Snapping Blocks Together

> **In one line:** a **chain** connects blocks with the `|` pipe, so the output of one block becomes the input of the next.

📄 Code: [step05_chains_lcel.py](../step05_chains_lcel.py)

---

## 🤔 The problem

In step 04 we called each block by hand:

```python
prompt_value = EXPLAIN_PROMPT.invoke({"topic": "vaccines", "level": "beginner"})
ai_message   = llm.invoke(prompt_value)
text         = StrOutputParser().invoke(ai_message)
```

Three lines and two temporary variables, every single time. It gets messy fast.

## 💡 The idea: an assembly line

**LCEL** (LangChain Expression Language) lets you write the same thing as:

```python
chain = EXPLAIN_PROMPT | llm | StrOutputParser()
text  = chain.invoke({"topic": "vaccines", "level": "beginner"})
```

Read `|` as **"then send it to"**:

```
  {"topic": "vaccines",          ┌────────┐  messages  ┌────────┐ AIMessage ┌────────┐
   "level": "beginner"}  ──────► │ PROMPT │ ─────────► │ GEMINI │ ────────► │ PARSER │ ──► "Vaccines teach
                                 └────────┘            └────────┘           └────────┘     your body..."
     dict  ─────────────────────────────────────────────────────────────────────────────►  str
```

> ✨ **The magic:** the chain itself is a Runnable too, so it gets `.invoke()`, `.stream()` and `.batch()` for free.

---

## 📍 The chains inside Study Buddy

| Chain | Pipeline | Used for |
|---|---|---|
| Explain | `EXPLAIN_PROMPT \| llm \| StrOutputParser()` | step demos |
| Summary | `SUMMARY_PROMPT \| llm \| StrOutputParser()` | **app option 2** |
| Quiz | `QUIZ_PROMPT \| llm.with_structured_output(Quiz)` | **app option 3** |
| RAG | `retriever → prompt \| llm \| parser` (step 11) | **app option 1** |

---

## 🧰 Three more helpful blocks

### `RunnableLambda`: put your own function in the chain

```python
def count_words(text):                      # an ordinary Python function
    return f"{text}\n\n(Word count: {len(text.split())})"

chain = EXPLAIN_PROMPT | llm | StrOutputParser() | RunnableLambda(count_words)
```

```
 dict ─► PROMPT ─► GEMINI ─► PARSER ─► count_words() ─► "...explanation...\n(Word count: 74)"
                                       └ your code ┘
```

### `RunnableParallel`: do two things at the same time

A "study pack" contains an explanation **and** a mnemonic. Each part is independent, so both are made **at the same time**:

```
                              ┌──► explain chain  ──► "Vaccines teach your body..." ─┐
 {"topic": "vaccines", ...} ──┤                                                      ├──► {"explanation": "...",
                              └──► mnemonic chain ──► "VAX = Very Able eXercise"   ──┘     "mnemonic": "..."}
```

```python
RunnableParallel(explanation=explain_chain, mnemonic=mnemonic_chain)
```

### `RunnablePassthrough`: pass the input along unchanged

This is useful when a later block needs the **original** input. You'll use it in the RAG chain (step 11).

---

## 🔗 Chains feeding chains

The output of one chain can be the input of another. For example, *explain a topic, then quiz me on that explanation*:

```
 {"topic": "vaccines"} ──► [ explain chain ] ──► explanation text
                                                      │  reshape: {"material": explanation, ...}
                                                      ▼
                                              [ quiz chain ] ──► Quiz object
```

---

## ⚠️ Common beginner mistakes

| Mistake | Fix |
|---|---|
| The next block gets the wrong shape (e.g. a string where a dict is expected) | check each block's input and output, and add a `RunnableLambda` to reshape |
| Forgetting the parser, so you get an `AIMessage` instead of a `str` | end text chains with `StrOutputParser()` |
| Debugging long chains with `print()` | turn on LangSmith (step 14) to see every step's input and output |

## ✅ Remember

- `a | b | c` = run a, give its output to b, then to c.
- A chain is a Runnable, so `.invoke`, `.stream` and `.batch` all work.
- `RunnableLambda` = your own function · `RunnableParallel` = several at once · `RunnablePassthrough` = keep the input.

⬅️ [04 · Output Parsers](04_output_parsers.md) · ➡️ **Next:** [06 · Memory](06_memory.md)
