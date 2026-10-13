"""
STEP 09  -  Embeddings: turning text into numbers that capture MEANING
======================================================================
📖 Read first: learning_notes/09_embeddings.md  (simple explanation with diagrams)

WHAT IS AN EMBEDDING?
    An embedding model converts text into a long list of numbers called a "vector"
    (Gemini's embedding model gives ~3000 numbers per text).

    The magic: texts with SIMILAR MEANING get SIMILAR vectors, even when they
    use different words. For example:
        "How do plants make food?"   and   "photosynthesis in leaves"
    share almost no words, but their vectors are close together.

    This is how our app finds the right part of your notes for a question:
    it compares the question's vector with the vector of every chunk.

TWO METHODS (every LangChain embedding model has both):
    .embed_query(text)        -> ONE vector, for a search question
    .embed_documents([texts]) -> a LIST of vectors, for the texts being searched

Run this file:   python step09_embeddings.py
"""

import math

from config import get_embeddings


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """
    Measures how similar two vectors are:  1.0 = same meaning, ~0 = unrelated.
    (You don't need to memorise this formula - vector stores do it for you.
     It is here only so you can see that "similarity" is just simple maths.)
    """
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    length_a = math.sqrt(sum(a * a for a in vector_a))
    length_b = math.sqrt(sum(b * b for b in vector_b))
    return dot_product / (length_a * length_b)


if __name__ == "__main__":
    embeddings = get_embeddings()

    print("=== 1. What does a vector look like? ===")
    vector = embeddings.embed_query("Plants use sunlight to make food.")
    print("Number of values:", len(vector))
    print("First 5 values  :", [round(v, 4) for v in vector[:5]])

    print("\n=== 2. Similar meaning -> similar vectors ===")
    question = "How do plants make their food?"
    sentences = [
        "Photosynthesis happens in the leaves using sunlight, water and carbon dioxide.",
        "Jupiter is the largest planet in the solar system.",
        "A for loop repeats a block of code several times.",
    ]

    question_vector = embeddings.embed_query(question)
    sentence_vectors = embeddings.embed_documents(sentences)

    print(f"Question: '{question}'\n")
    for sentence, sentence_vector in zip(sentences, sentence_vectors):
        score = cosine_similarity(question_vector, sentence_vector)
        print(f"  similarity {score:.3f}  <-  {sentence}")
    print("\nThe photosynthesis sentence scores highest, even though it uses different words!")
