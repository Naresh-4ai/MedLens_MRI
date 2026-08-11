import os

from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

load_dotenv()


COLLECTION_NAME = "medical_knowledge_base"

qdrant_client = QdrantClient(
    host=os.getenv("QDRANT_HOST", "localhost"),
    port=int(os.getenv("QDRANT_PORT", "6333"))
)


def create_collection():

    collections = qdrant_client.get_collections().collections

    names = [collection.name for collection in collections]

    if COLLECTION_NAME not in names:

        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )


def store_embedding(
    point_id: str,
    embedding: list,
    payload: dict
):

    point = PointStruct(
        id=point_id,
        vector=embedding,
        payload=payload
    )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )


def search_similar_documents(
    embedding: list,
    limit: int = 5
):

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit
    )

    return results.points


def delete_collection():

    if collection_exists():

        qdrant_client.delete_collection(
            collection_name=COLLECTION_NAME
        )


def collection_exists():

    collections = qdrant_client.get_collections().collections

    return COLLECTION_NAME in [c.name for c in collections]