from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def medical_info_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Medical Information Agent

    Extracts structured medical information from OCR text.

    Input:
        state["ocr_results"]

    Output:
        state["medical_information"]
    """

    documents = state.get("ocr_results", [])

    medical_information = []

    for document in documents:

        extracted_text = document.get("text", "").strip()

        if not extracted_text:
            continue

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": """
You are the Medical Information Agent of MedLens.

Extract ONLY the information explicitly available in the medical document.

Return ONLY valid JSON using this schema:

{
    "patient_name": "",
    "age": "",
    "gender": "",
    "hospital": "",
    "doctor": "",

    "diagnoses": [],
    "symptoms": [],
    "medical_history": [],
    "allergies": [],

    "medications": [
        {
            "name": "",
            "dosage": "",
            "frequency": ""
        }
    ],

    "lab_results": [
        {
            "test": "",
            "result": "",
            "unit": ""
        }
    ],

    "procedures": [],
    "hospital_visits": [],
    "follow_up": "",
    "important_dates": [],
    "summary": ""
}

Rules:

- Extract only information explicitly present.
- Do not infer or diagnose.
- Do not recommend treatments.
- Leave unavailable fields empty.
- Return ONLY valid JSON.
"""
                },
                {
                    "role": "user",
                    "content": extracted_text
                }
            ]
        )

        medical_information.append(
            {
                "file": document.get("file"),
                "file_id": document.get("file_id"),
                "document_type": document.get("document_type"),
                "medical_info": response.choices[0].message.content
            }
        )

    state["medical_information"] = medical_information

    return state