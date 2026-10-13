"""
STEP 06  -  Memory: making the chatbot remember the conversation
================================================================
📖 Read first: learning_notes/06_memory.md  (simple explanation with diagrams)

Remember from step 02: LLMs have NO memory. Every call is brand new.
"Memory" in LangChain simply means:
    1. SAVE every message (human + AI) somewhere, and
    2. SEND those saved messages along with every new question.

We show two ways:

  A) The manual way - we keep a Python list of messages ourselves.
     Great for understanding what memory REALLY is.

  B) The LangChain way - RunnableWithMessageHistory.
     It wraps a chain and automatically loads/saves the history for us.
     Each conversation gets a "session_id", so many users can chat at once
     without mixing up their histories.

(Agents use a third way, a "checkpointer" - you'll see it in step 13.)

Run this file:   python step06_memory.py
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import get_chat_model


# The prompt has a MessagesPlaceholder called "history" where the past
# conversation gets inserted (see step 03).
TUTOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are Study Buddy, a friendly tutor. Keep answers short (under 60 words)."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])


# ------------------------------------------------------------------
# A) Manual memory with a Python list
# ------------------------------------------------------------------
def manual_memory_demo():
    chain = TUTOR_PROMPT | get_chat_model() | StrOutputParser()
    history = []  # this list IS the memory

    for question in ["Hi! I'm Arjun and I'm studying photosynthesis.",
                     "What gas do plants take in for it?",
                     "What's my name and what am I studying?"]:
        answer = chain.invoke({"history": history, "question": question})
        print(f"You : {question}\nBot : {answer}\n")

        # Save both sides of the exchange so the NEXT call can see them.
        history.append(HumanMessage(content=question))
        history.append(AIMessage(content=answer))


# ------------------------------------------------------------------
# B) Automatic memory with RunnableWithMessageHistory
# ------------------------------------------------------------------
# A simple dictionary that maps session_id -> that session's history.
# (In a real app this could be a database, e.g. Redis or SQL.)
session_store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Return the history for this session, creating an empty one if new."""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]


def build_tutor_with_memory():
    """A chat chain that remembers each session's conversation automatically."""
    chain = TUTOR_PROMPT | get_chat_model() | StrOutputParser()

    return RunnableWithMessageHistory(
        chain,
        get_session_history,                 # how to find a session's history
        input_messages_key="question",       # which input key is the new user message
        history_messages_key="history",      # which prompt placeholder gets the history
    )


def automatic_memory_demo():
    tutor = build_tutor_with_memory()

    # The session_id is passed through "config", not through the input.
    riya = {"configurable": {"session_id": "riya"}}
    sam = {"configurable": {"session_id": "sam"}}

    print("Riya:", tutor.invoke({"question": "Hi, I'm Riya. I love chemistry."}, config=riya))
    print("Sam :", tutor.invoke({"question": "Hi, I'm Sam. I love history."}, config=sam))
    # Each session only remembers its OWN conversation:
    print("Riya:", tutor.invoke({"question": "Which subject do I love?"}, config=riya))
    print("Sam :", tutor.invoke({"question": "Which subject do I love?"}, config=sam))

    print("\nWhat is stored for Riya:")
    for message in session_store["riya"].messages:
        print(f"  [{message.type}] {message.content[:60]}")


if __name__ == "__main__":
    print("=== A) Manual memory ===")
    manual_memory_demo()

    print("=== B) RunnableWithMessageHistory ===")
    automatic_memory_demo()
