from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embedding(text: str) -> List[float]:
    """
    Generate an embedding for a single text.
    """

    text = text.strip()

    if not text:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    """

    texts = [text.strip() for text in texts if text.strip()]

    if not texts:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]