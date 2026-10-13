"""
STEP 03  -  Prompt Templates: reusable prompts with blanks to fill in
=====================================================================
📖 Read first: learning_notes/03_prompt_templates.md  (simple explanation with diagrams)

PROBLEM:
    In a real app you don't type the prompt by hand every time. The prompt has
    a fixed part ("You are a tutor... explain this topic...") and a changing
    part (the topic the user typed).

SOLUTION:
    A Prompt Template is a prompt with {placeholders}. You fill the
    placeholders with .invoke({...}) and get a ready-to-send prompt.

    PromptTemplate       -> builds ONE plain text string
    ChatPromptTemplate   -> builds a LIST OF MESSAGES (system/human/ai)  <- used most
    MessagesPlaceholder  -> a slot where a whole list of messages goes
                            (e.g. the chat history - used in step 06)

NOTE: A template does NOT call the LLM. It only prepares the input.
      Prompt templates are Runnables too, so they also have .invoke().

Run this file:   python step03_prompt_templates.py
"""

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from config import get_chat_model


# ------------------------------------------------------------------
# 1. PromptTemplate: a simple text prompt with blanks
# ------------------------------------------------------------------
def simple_prompt_template_demo():
    # {topic} and {level} are placeholders that we fill in later.
    template = PromptTemplate.from_template(
        "Explain {topic} to a {level} student in 3 short bullet points."
    )

    # Filling the blanks. The result is a "PromptValue" (a finished prompt).
    prompt_value = template.invoke({"topic": "gravity", "level": "beginner"})
    print("Finished prompt text:\n", prompt_value.to_string())

    # The same template can be reused with different values:
    print("\nReused:\n", template.invoke({"topic": "DNA", "level": "high school"}).to_string())


# ------------------------------------------------------------------
# 2. ChatPromptTemplate: a template that produces messages
# ------------------------------------------------------------------
# This is the template our Study Buddy uses to explain topics.
# We create it once, at the top level, so other files can import it.
EXPLAIN_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are Study Buddy, a patient tutor. Explain topics for a {level} student. "
     "Use simple words and one real-life example."),
    ("human", "Please explain: {topic}"),
])


def chat_prompt_template_demo():
    # Fill the blanks -> we get a list of messages, ready for a chat model.
    prompt_value = EXPLAIN_PROMPT.invoke({"level": "beginner", "topic": "electric current"})

    print("Messages produced by the template:")
    for message in prompt_value.to_messages():
        print(f"  [{message.type}] {message.content}")

    # Now send them to the model.
    llm = get_chat_model()
    response = llm.invoke(prompt_value)
    print("\nModel answer:\n", response.text)


# ------------------------------------------------------------------
# 3. Few-shot prompting: teach the model by showing examples
# ------------------------------------------------------------------
# "Few-shot" means: include a few example question/answer pairs in the prompt,
# so the model copies the STYLE of the examples.
MNEMONIC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You create short, catchy memory tricks (mnemonics) for students."),
    # --- example 1 ---
    ("human", "Order of the planets"),
    ("ai", "My Very Educated Mother Just Served Us Noodles (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune)"),
    # --- example 2 ---
    ("human", "Colours of the rainbow"),
    ("ai", "ROY G BIV (Red, Orange, Yellow, Green, Blue, Indigo, Violet)"),
    # --- the real question ---
    ("human", "{topic}"),
])


def few_shot_demo():
    llm = get_chat_model(temperature=0.8)  # a bit more creative for mnemonics
    prompt_value = MNEMONIC_PROMPT.invoke({"topic": "The first 5 noble gases"})
    print(llm.invoke(prompt_value).text)


# ------------------------------------------------------------------
# 4. MessagesPlaceholder: a slot for a list of messages
# ------------------------------------------------------------------
def messages_placeholder_demo():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are Study Buddy. Keep answers short."),
        # Everything inside "history" will be inserted here, in order.
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    prompt_value = prompt.invoke({
        "history": [
            HumanMessage(content="I'm learning about cells."),
            AIMessage(content="Great! Cells are the building blocks of life."),
        ],
        "question": "What did I say I was learning?",
    })

    for message in prompt_value.to_messages():
        print(f"  [{message.type}] {message.content}")


if __name__ == "__main__":
    print("=== 1. PromptTemplate ===")
    simple_prompt_template_demo()

    print("\n=== 2. ChatPromptTemplate ===")
    chat_prompt_template_demo()

    print("\n=== 3. Few-shot prompting ===")
    few_shot_demo()

    print("\n=== 4. MessagesPlaceholder ===")
    messages_placeholder_demo()
