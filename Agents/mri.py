from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

from Agents.embeddings import generate_embedding

from Database.qdrant import search_similar_documents
from Database.neo4j import get_patient_context

load_dotenv()

client = OpenAI()


def retrieve_context(question: str):

    embedding = generate_embedding(question)

    if not embedding:
        return "", ""

    results = search_similar_documents(
        embedding=embedding,
        limit=6
    )

    if not results:
        return "", ""

    patient_name = None
    retrieved_documents = []

    for result in results:

        payload = result.payload

        if patient_name is None:
            patient_name = payload.get("patient")

        retrieved_documents.append(
            f"""
Document Type:
{payload.get("document_type")}

Content:
{payload.get("content")}
"""
        )

    semantic_context = "\n\n---------------------------\n\n".join(
        retrieved_documents
    )

    graph_context = ""

    if patient_name:

        graph_context = get_patient_context(patient_name)

    return semantic_context, graph_context


def mri_agent(state: Dict[str, Any]) -> Dict[str, Any]:

    doctor_query = state.get("doctor_query", "").strip()

    if not doctor_query:

        state["mri_response"] = "Please enter a doctor's question."

        return state

    semantic_context, graph_context = retrieve_context(
        doctor_query
    )

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content": """
You are MedLens MRI (Medical Report Intelligence).

You assist healthcare professionals by understanding a patient's uploaded medical records.

You are NOT a doctor.

Your responsibilities:

- Summarize patient history.
- Explain diagnoses already documented.
- Explain medications already prescribed.
- Explain laboratory findings.
- Explain procedures.
- Explain hospital visits.
- Track disease progression.
- Answer questions ONLY from the uploaded records.

Rules:

- Never diagnose diseases.
- Never prescribe medication.
- Never recommend treatment.
- Never interpret MRI, CT, X-ray or Ultrasound images.
- Never make assumptions.
- If the answer is unavailable in the uploaded records, clearly say so.
- Always cite which document(s) the answer came from.
- Keep responses concise and professional.
"""
            },

            {
                "role": "user",
                "content": f"""
Doctor Question

{doctor_query}


Retrieved Medical Records

{semantic_context}


Patient Knowledge Graph

{graph_context}
"""
            }

        ]

    )

    state["mri_response"] = response.choices[0].message.content.strip()

    return state