"""
STEP 02  -  Messages: the "language" chat models understand
============================================================
📖 Read first: learning_notes/02_messages.md  (simple explanation with diagrams)

In step 01 we sent a plain string. Behind the scenes, LangChain turned that
string into a message. Chat models really work with a LIST of messages,
where every message has a ROLE:

    SystemMessage  -> instructions for the AI: its personality, its rules.
                      The user usually never sees this.
    HumanMessage   -> what the user says.
    AIMessage      -> what the AI said earlier (used to give the model context).

WHY DOES THIS MATTER?
    LLMs have NO memory. Each call starts fresh. If you want the model to
    "remember" a conversation, you must send the whole conversation again as a
    list of messages. (Step 06 automates this.)

Run this file:   python step02_messages.py
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from config import get_chat_model


def ask_with_system_message(question: str) -> str:
    """Give the model a personality with a SystemMessage."""
    llm = get_chat_model()

    messages = [
        # The system message sets the rules for the whole conversation.
        SystemMessage(content=(
            "You are Study Buddy, a friendly tutor for students. "
            "Explain things simply, use a small example, and keep answers under 80 words."
        )),
        # The human message is the actual question.
        HumanMessage(content=question),
    ]

    response = llm.invoke(messages)  # response is an AIMessage
    return response.text


def conversation_with_context() -> str:
    """
    Show how we "fake" memory by sending the earlier conversation again.
    The model answers the LAST message, but it can read all the earlier ones.
    """
    llm = get_chat_model()

    messages = [
        SystemMessage(content="You are Study Buddy, a helpful tutor. Keep answers short."),
        HumanMessage(content="My name is Riya and I am studying the solar system."),
        AIMessage(content="Nice to meet you, Riya! The solar system is a great topic. What would you like to know?"),
        # Because the two messages above are included, the model knows the
        # name AND the topic, even though this question doesn't mention them.
        HumanMessage(content="What is my name, and which planet should I start with?"),
    ]

    response = llm.invoke(messages)
    return response.text


def messages_as_tuples() -> str:
    """
    Shortcut: instead of message classes you can write (role, text) tuples.
    LangChain converts them into proper message objects for you.
    """
    llm = get_chat_model()
    response = llm.invoke([
        ("system", "You answer in exactly one sentence."),
        ("human", "Why is the sky blue?"),
    ])
    return response.text


if __name__ == "__main__":
    print("=== 1. SystemMessage + HumanMessage ===")
    print(ask_with_system_message("What is a variable in programming?"))

    print("\n=== 2. Giving the model the earlier conversation ===")
    print(conversation_with_context())

    print("\n=== 3. The tuple shortcut ===")
    print(messages_as_tuples())
