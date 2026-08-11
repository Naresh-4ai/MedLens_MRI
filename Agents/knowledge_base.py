import json
import uuid
from typing import Dict, Any

from Agents.embeddings import generate_embedding

from Database.qdrant import (
    create_collection,
    store_embedding
)

from Database.neo4j import (
    create_constraints,
    create_patient,
    create_document,
    create_hospital,
    create_doctor,
    create_diagnosis,
    create_medications,
    create_lab_tests
)


CHUNK_SIZE = 1200


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE):

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        chunks.append(
            text[start:start + chunk_size]
        )

        start += chunk_size

    return chunks


def knowledge_base_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds the MedLens Knowledge Base.

    Neo4j
    -------
    Stores structured patient relationships.

    Qdrant
    -------
    Stores raw OCR chunks for semantic retrieval.
    """

    create_constraints()
    create_collection()

    medical_information = state.get("medical_information", [])
    ocr_results = state.get("ocr_results", [])

    stored_embeddings = 0

    # Build Neo4j Graph

    for record in medical_information:

        medical_info = json.loads(record["medical_info"])

        patient = medical_info.get("patient_name") or "Unknown Patient"

        create_patient(patient)

        create_document(
            patient,
            record["document_type"]
        )

        create_hospital(
            patient,
            medical_info.get("hospital")
        )

        create_doctor(
            patient,
            medical_info.get("doctor")
        )

        create_diagnosis(
            patient,
            medical_info.get("diagnoses", [])
        )

        create_medications(
            patient,
            medical_info.get("medications", [])
        )

        create_lab_tests(
            patient,
            medical_info.get("lab_results", [])
        )

    # Build Qdrant Semantic Memory

    for document in ocr_results:

        text = document.get("text", "")

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            embedding = generate_embedding(chunk)

            if not embedding:
                continue

            store_embedding(

                point_id=str(uuid.uuid4()),

                embedding=embedding,

                payload={

                    "file": document.get("file"),

                    "document_type": document.get("document_type"),

                    "document_format": document.get("document_format"),

                    "chunk_id": index,

                    "content": chunk

                }
            )

            stored_embeddings += 1

    state["knowledge_base_status"] = {

        "status": "success",

        "stored_documents": len(medical_information),

        "stored_embeddings": stored_embeddings

    }

    return state