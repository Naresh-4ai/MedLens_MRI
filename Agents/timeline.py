from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def timeline_agent(state: Dict[str, Any]) -> Dict[str, Any]:

    patient_records = state.get("medical_information", [])

    if not patient_records:
        state["medical_timeline"] = ""
        return state

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are the Timeline Agent of MedLens.

Your job is to organize the patient's medical history
into a chronological timeline.

Include:

- Hospital visits
- Diagnoses
- Medications started or changed
- Lab tests
- Procedures
- Follow-up visits
- Major clinical events

Rules:

- Arrange events from oldest to newest.
- Never invent dates.
- If a date is missing, place the event under "Date Unknown".
- Use only the provided records.
- Keep each event short and clear.
"""
            },
            {
                "role": "user",
                "content": str(patient_records)
            }
        ]
    )

    state["medical_timeline"] = response.choices[0].message.content.strip()

    return state