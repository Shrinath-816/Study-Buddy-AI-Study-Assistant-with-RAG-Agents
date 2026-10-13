"""
STEP 13  -  Agents: an LLM that decides which tools to use, by itself
=====================================================================
📖 Read first: learning_notes/13_agents.md  (simple explanation with diagrams)

CHAIN vs AGENT
    Chain -> YOU decide the steps in advance:   prompt | llm | parser
    Agent -> the LLM decides the steps while running. It works in a LOOP:

        +--> model thinks: "do I need a tool?"
        |        | yes                         | no
        |   run the tool(s)              write the final answer -> DONE
        +--- feed the result back

    This is exactly the manual cycle from step 12, but repeated automatically
    until the model has everything it needs. For example, for
    "Look up Jupiter in my notes and save a flashcard about it" the agent will
    first call search_my_notes, THEN save_flashcard, THEN answer.

create_agent()
    LangChain's function to build an agent from: a model + tools + a system prompt.
    (Agents in LangChain run on "LangGraph", LangChain's engine for loops and steps.
     You don't need to learn LangGraph to use create_agent.)

MEMORY FOR AGENTS: a "checkpointer"
    InMemorySaver saves the agent's conversation after every step.
    Each conversation has a "thread_id" (like session_id in step 06).

Run this file:   python step13_agent.py
"""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from config import get_chat_model
from step12_tools import STUDY_TOOLS


AGENT_SYSTEM_PROMPT = """You are Study Buddy, a friendly AI study assistant for a student.

You have these tools:
- search_my_notes: ALWAYS use this first when the question could be about the student's notes.
- calculate: use for any arithmetic instead of doing maths in your head.
- save_flashcard: use when the student asks you to save or remember something for revision.
- show_flashcards: use when the student wants to see their saved flashcards.

Base factual answers on the notes when possible and say which file they came from.
Keep answers short and encouraging."""


def build_study_agent():
    """Create the Study Buddy agent with tools and conversation memory."""
    return create_agent(
        model=get_chat_model(),
        tools=STUDY_TOOLS,
        system_prompt=AGENT_SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),  # gives the agent memory between messages
    )


def ask_agent(agent, question: str, thread_id: str = "student-1") -> str:
    """Send one message to the agent and return its final reply."""
    result = agent.invoke(
        # Agents take a dict with a list of "messages" as input.
        {"messages": [{"role": "user", "content": question}]},
        # The thread_id tells the checkpointer which conversation this belongs to.
        config={
            "configurable": {"thread_id": thread_id},
            # run_name and tags only affect how this run looks in LangSmith (step 14)
            "run_name": "Study Buddy Agent",
            "tags": ["study-buddy", "agent"],
        },
    )
    # result["messages"] holds the WHOLE conversation, including tool calls.
    # The last message is the agent's final answer.
    return result["messages"][-1].text


def watch_agent_think(agent, question: str, thread_id: str = "demo-steps"):
    """
    Stream the agent's work step by step, so you can SEE its decisions.
    stream_mode="updates" yields one update every time a step finishes.
    """
    for update in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        stream_mode="updates",
    ):
        # Each update looks like {"model": {...}} or {"tools": {...}}
        for step_name, data in update.items():
            for message in data["messages"]:
                if message.type == "ai" and message.tool_calls:
                    for call in message.tool_calls:
                        print(f"  [{step_name}] decided to call -> {call['name']}({call['args']})")
                elif message.type == "tool":
                    print(f"  [{step_name}] {message.name} returned -> {str(message.content)[:80]!r}")
                elif message.type == "ai":
                    print(f"  [{step_name}] final answer -> {message.text}")


if __name__ == "__main__":
    agent = build_study_agent()

    print("=== 1. Watch the agent decide which tools to use ===")
    watch_agent_think(agent, "Find the largest planet in my notes and save a flashcard about it.")

    print("\n=== 2. A maths question (should use the calculate tool) ===")
    print(ask_agent(agent, "If Jupiter is 11.2 times wider than Earth, and Earth is 12742 km wide, how wide is Jupiter?"))

    print("\n=== 3. Memory: the agent remembers the conversation ===")
    print(ask_agent(agent, "My exam is on Friday and I struggle with Python loops."))
    print(ask_agent(agent, "What did I say I struggle with?"))
