"""
STEP 01  -  Chat Models: talking to an LLM through LangChain
=============================================================
📖 Read first: learning_notes/01_chat_models.md  (simple explanation with diagrams)

WHAT IS A CHAT MODEL?
    A "chat model" is LangChain's wrapper around an LLM (Gemini, GPT, Claude...).
    You give it some text (or a list of messages), and it gives you back a reply.

WHY USE LANGCHAIN INSTEAD OF CALLING GEMINI DIRECTLY?
    Every chat model in LangChain has the SAME three methods:
        .invoke(input)    -> send ONE input, wait, get ONE full answer
        .stream(input)    -> send ONE input, get the answer piece by piece (like ChatGPT typing)
        .batch([inputs])  -> send MANY inputs at once, get a list of answers
    Learn these once, and they work for every model AND (as you'll see in step 05)
    for prompts, parsers and chains too. In LangChain, anything with these methods
    is called a "Runnable".

Run this file:   python step01_chat_model.py
"""

from config import get_chat_model


def ask_simple_question(question: str) -> str:
    """Send a plain string to the model and return the answer text."""
    llm = get_chat_model()

    # .invoke() sends the question and WAITS for the complete answer.
    response = llm.invoke(question)

    # The response is NOT a plain string. It is an "AIMessage" object.
    # .text gives us just the written answer.
    return response.text


def show_response_object():
    """Look inside the AIMessage object the model returns."""
    llm = get_chat_model()
    response = llm.invoke("In one sentence, what is photosynthesis?")

    print("Type of response   :", type(response).__name__)  # -> AIMessage
    print("Answer text        :", response.text)
    # usage_metadata tells you how many tokens (pieces of words) were used.
    # Tokens matter because API usage is measured (and billed) in tokens.
    print("Token usage        :", response.usage_metadata)


def stream_answer(question: str):
    """Print the answer word by word as it is being generated."""
    llm = get_chat_model()

    # .stream() returns the answer in small "chunks" as soon as they are ready.
    # This makes apps feel much faster, because the user sees text immediately.
    for chunk in llm.stream(question):
        print(chunk.text, end="", flush=True)
    print()  # final new line


def ask_many_questions(questions: list[str]) -> list[str]:
    """Send several questions in one go using .batch()."""
    llm = get_chat_model()

    # .batch() runs all the inputs (in parallel where possible)
    # and returns a list of AIMessages in the SAME order.
    responses = llm.batch(questions)
    return [response.text for response in responses]


# ------------------------------------------------------------------
# Demo: only runs when you execute this file directly
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 1. invoke() ===")
    print(ask_simple_question("Explain what an atom is to a 10 year old in 2 sentences."))

    print("\n=== 2. What does the response object contain? ===")
    show_response_object()

    print("\n=== 3. stream() ===")
    stream_answer("Give me 3 quick tips to remember things better while studying.")

    print("\n=== 4. batch() ===")
    answers = ask_many_questions([
        "What is the capital of Japan? Answer in one word.",
        "What is 12 x 12? Answer with just the number.",
    ])
    for answer in answers:
        print("-", answer)
