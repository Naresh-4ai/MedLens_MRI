import json
import base64
import mimetypes
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


DOCUMENT_TYPES = [
    "Prescription",
    "Lab Report",
    "Discharge Summary",
    "Radiology Report",
    "Clinical Note",
    "Medical Certificate",
    "Insurance Document",
    "Unknown"
]


def classification_agent(state: Dict[str, Any]) -> Dict[str, Any]:

    uploaded_files = state.get("uploaded_files", [])

    documents = []

    for file_path in uploaded_files:

        extension = file_path.lower().split(".")[-1]
        # PDF
        if extension == "pdf":

            with open(file_path, "rb") as file:

                uploaded_file = client.files.create(
                    file=file,
                    purpose="user_data"
                )

            content = [
                {
                    "type": "file",
                    "file": {
                        "file_id": uploaded_file.id
                    }
                },
                {
                    "type": "text",
                    "text": "Classify this medical document."
                }
            ]

            file_id = uploaded_file.id

        # Images


        elif extension in ["png", "jpg", "jpeg"]:

            mime_type = mimetypes.guess_type(file_path)[0]

            if not mime_type:
                mime_type = "image/jpeg"

            with open(file_path, "rb") as file:

                image_data = base64.b64encode(
                    file.read()
                ).decode("utf-8")

            image_url = (
                f"data:{mime_type};base64,{image_data}"
            )

            content = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                },
                {
                    "type": "text",
                    "text": "Classify this medical document."
                }
            ]

            file_id = None

        else:

            continue

        # Classification

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content": f"""
You are the Classification Agent of MedLens.

Your job is to identify the uploaded medical document.

Choose ONLY one document type from:

{", ".join(DOCUMENT_TYPES)}

Also determine whether the document is:

- Digital PDF
- Scanned Document
- Handwritten Note

Return ONLY valid JSON.

Example:

{{
    "document_type": "Prescription",
    "document_format": "Scanned Document",
    "requires_ocr": true
}}

Rules:

- Digital PDFs -> requires_ocr = false
- Scanned Documents -> requires_ocr = true
- Handwritten Notes -> requires_ocr = true
- Never explain your answer.
"""
                },

                {
                    "role": "user",
                    "content": content
                }

            ]
        )

        classification = json.loads(
            response.choices[0].message.content
        )

        documents.append(
            {
                "file": file_path,
                "file_id": file_id,
                "document_type": classification.get(
                    "document_type",
                    "Unknown"
                ),
                "document_format": classification.get(
                    "document_format",
                    "Unknown"
                ),
                "requires_ocr": classification.get(
                    "requires_ocr",
                    True
                )
            }
        )

    state["documents"] = documents

    return state