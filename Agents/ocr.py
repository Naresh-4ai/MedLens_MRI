import base64
import mimetypes
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def ocr_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Document Reader Agent

    Reads uploaded medical documents and extracts
    all available text without interpretation.
    """

    documents = state.get("documents", [])

    ocr_results = []

    for document in documents:

        file_path = document["file"]
        file_id = document.get("file_id")

        extension = file_path.lower().split(".")[-1]

        # PDF

        if extension == "pdf":

            content = [
                {
                    "type": "file",
                    "file": {
                        "file_id": file_id
                    }
                },
                {
                    "type": "text",
                    "text": "Extract all text from this medical document."
                }
            ]

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
                    "text": "Extract all text from this medical document."
                }
            ]

        else:

            continue

        # OCR / Document Reading

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content": """
You are the Document Reader Agent of MedLens.

Your job is to faithfully read the uploaded medical document.

The document may be:

- Digital PDF
- Scanned PDF
- Handwritten Medical Note
- Prescription
- Lab Report
- Discharge Summary
- Clinical Note
- Radiology Report
- Medical Certificate

Instructions:

- Extract every readable character.
- Preserve headings.
- Preserve paragraphs.
- Preserve dates exactly.
- Preserve medicine names exactly.
- Preserve dosages exactly.
- Preserve laboratory values exactly.
- Preserve units.
- Preserve tables whenever possible.
- If handwriting cannot be read, write [Unreadable].
- Never guess missing words.
- Never summarize.
- Never interpret.
- Return ONLY the extracted text.
"""
                },

                {
                    "role": "user",
                    "content": content
                }

            ]
        )

        extracted_text = (
            response.choices[0]
            .message.content
            .strip()
        )

        ocr_results.append(
            {
                "file": document.get("file"),
                "file_id": document.get("file_id"),
                "document_type": document.get("document_type"),
                "document_format": document.get("document_format"),
                "requires_ocr": document.get("requires_ocr"),
                "text": extracted_text
            }
        )

    state["ocr_results"] = ocr_results

    return state