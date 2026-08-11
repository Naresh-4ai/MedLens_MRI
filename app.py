import os
import json
import streamlit as st

from Langgraph.orchestrator import graph
from Agents.mri import mri_agent

st.set_page_config(
    page_title="MedLens",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 MedLens")
st.caption("Medical Report Intelligence")

st.divider()

uploaded_files = st.file_uploader(
    "Upload Patient Medical Records",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs("uploads", exist_ok=True)

    saved_files = []

    for file in uploaded_files:

        path = os.path.join("uploads", file.name)

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        saved_files.append(path)

    if st.button("Analyze Records"):

        with st.spinner("Analyzing medical records..."):

            state = {
                "uploaded_files": saved_files
            }

            result = graph.invoke(state)

            st.session_state["patient_data"] = result

            # Clear previous chat whenever a new patient is uploaded
            st.session_state["chat_history"] = []

        st.success("Analysis Complete")


if "patient_data" in st.session_state:

    state = st.session_state["patient_data"]

    st.divider()

    st.header("👤 Patient Summary")

    info = {}

    if state.get("medical_information"):

        info = json.loads(
            state["medical_information"][0]["medical_info"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Patient Name**")
            st.write(info.get("patient_name", "Not Available"))

            st.write("**Age**")
            st.write(info.get("age", "Not Available"))

            st.write("**Gender**")
            st.write(info.get("gender", "Not Available"))

            st.write("**Hospital**")
            st.write(info.get("hospital", "Not Available"))

        with col2:

            st.write("**Doctor**")
            st.write(info.get("doctor", "Not Available"))

            st.write("**Medical History**")

            history = info.get("medical_history", [])

            if history:
                st.write(history)
            else:
                st.write("Not Available")

            st.write("**Allergies**")

            allergies = info.get("allergies", [])

            if allergies:
                st.write(allergies)
            else:
                st.write("None Reported")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🩺 Diagnoses")

        diagnoses = info.get("diagnoses", [])

        if diagnoses:

            for diagnosis in diagnoses:
                st.success(diagnosis)

        else:

            st.info("No diagnoses found.")

    with col2:

        st.subheader("💊 Medications")

        medications = info.get("medications", [])

        if medications:

            for medicine in medications:

                st.info(
                    f"""
{medicine.get("name","")}

Dosage : {medicine.get("dosage","")}

Frequency : {medicine.get("frequency","")}
"""
                )

        else:

            st.info("No medications found.")

    st.divider()

    st.subheader("🧪 Laboratory Results")

    labs = info.get("lab_results", [])

    if labs:

        for lab in labs:

            st.write(
                f"""
**{lab.get("test","")}**

Result : {lab.get("result","")}

Unit : {lab.get("unit","")}
"""
            )

    else:

        st.info("No laboratory results found.")

    st.divider()

    st.subheader("📅 Medical Timeline")

    st.write(
        state.get(
            "medical_timeline",
            "Timeline unavailable."
        )
    )

    st.divider()

    st.subheader("📂 Uploaded Medical Documents")

    for document in state.get("medical_information", []):

        with st.expander(document["file"]):

            st.json(
                json.loads(
                    document["medical_info"]
                )
            )

    st.divider()

    st.subheader("💬 Doctor Assistant")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Show previous chat
    for message in st.session_state["chat_history"]:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask anything about this patient's medical records..."
    )

    if question:

        st.session_state["chat_history"].append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        # Reuse existing processed patient data
        state = st.session_state["patient_data"]

        state["doctor_query"] = question

        with st.spinner("Searching patient records..."):

            # Only MRI runs here
            state = mri_agent(state)

        st.session_state["patient_data"] = state

        answer = state["mri_response"]

        st.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)