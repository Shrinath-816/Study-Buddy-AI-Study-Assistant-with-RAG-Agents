"""
config.py  -  Shared settings for the whole project
=====================================================

Every other file imports its LLM and embedding model from HERE.
That way, if you want to switch models, you only change ONE file.

LangChain idea to notice:
    LangChain gives every chat model the SAME interface (.invoke, .stream, .batch).
    So if one day you switch from Gemini to OpenAI or Claude, you would only change
    the two functions below - the rest of the project keeps working untouched.
"""

import os
from dotenv import load_dotenv

# Gemini's chat model class and embedding model class.
# They live in the "langchain-google-genai" integration package.
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


# ------------------------------------------------------------------
# 1. Load the API key from the .env file
# ------------------------------------------------------------------
# load_dotenv() reads the .env file and puts GOOGLE_API_KEY into os.environ.
# The Gemini classes automatically look for GOOGLE_API_KEY, so we never
# have to pass the key around by hand.
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("WARNING: GOOGLE_API_KEY was not found. Copy .env.example to .env and add your key.")


# ------------------------------------------------------------------
# 1b. LangSmith tracing (see step14_langsmith_tracing.py)
# ------------------------------------------------------------------
# There is NO tracing code to write! LangChain checks these environment variables
# (loaded from .env above) and, if LANGSMITH_TRACING is "true", automatically sends
# a record ("trace") of every model call, chain, retriever and tool to LangSmith:
#     LANGSMITH_TRACING=true
#     LANGSMITH_API_KEY=...
#     LANGSMITH_PROJECT=study-buddy     (the folder your traces are grouped in)
if os.getenv("LANGSMITH_TRACING", "").lower() == "true" and not os.getenv("LANGSMITH_API_KEY"):
    print("WARNING: LANGSMITH_TRACING is on but LANGSMITH_API_KEY is missing. "
          "Add the key to .env or set LANGSMITH_TRACING=false.")


def print_tracing_status():
    """Tell the user whether LangSmith tracing is on, and where to look."""
    if os.getenv("LANGSMITH_TRACING", "").lower() == "true":
        project = os.getenv("LANGSMITH_PROJECT", "default")
        print(f"[LangSmith] Tracing is ON  -> see your traces at https://smith.langchain.com (project: '{project}')")
    else:
        print("[LangSmith] Tracing is OFF (set LANGSMITH_TRACING=true in .env to turn it on)")


# ------------------------------------------------------------------
# 2. Project settings (change these freely)
# ------------------------------------------------------------------
CHAT_MODEL_NAME = "gemini-3.5-flash"         # the LLM that writes answers
EMBEDDING_MODEL_NAME = "gemini-embedding-001"  # the model that turns text into numbers (vectors)

NOTES_FOLDER = "notes"                       # put your study notes (.txt / .md / .pdf) here
VECTOR_STORE_PATH = "data/notes_index.json"  # where the searchable index of your notes is saved
FLASHCARDS_FILE = "data/flashcards.txt"      # where the agent saves flashcards for you


# ------------------------------------------------------------------
# 3. Helper functions that create the models
# ------------------------------------------------------------------
def get_chat_model(temperature: float = 0.3):
    """
    Create and return the chat model (the "LLM").

    temperature controls creativity:
        0.0  -> very focused, gives almost the same answer every time
        1.0  -> more creative / random
    For a study assistant we want mostly factual answers, so we keep it low.
    """
    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL_NAME,
        temperature=temperature,
    )


def get_embeddings():
    """
    Create and return the embedding model.

    An embedding model does NOT chat. It converts a piece of text into a list
    of numbers (a "vector") that represents its MEANING. Texts with similar
    meanings get similar vectors. We use this later to search our notes.
    """
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME)
