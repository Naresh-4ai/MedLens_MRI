## 🩺 MedLens — Medical Report Intelligence

> *“See every patient's history through one intelligent lens.”*

**MedLens** is a prototype medical document intelligence and doctor-assistance system designed to bring a patient's scattered medical records together into one intelligent view.

Built with **Python, LangGraph, OpenAI, Qdrant, Neo4j, and Streamlit**, MedLens processes multiple medical documents, extracts clinically relevant information, builds a chronological view of the patient's history, and combines **semantic retrieval with a medical knowledge graph** to help doctors quickly understand the patient's records.

Instead of treating every report as an isolated PDF, MedLens connects information across **prescriptions, laboratory reports, discharge summaries, radiology reports, consultation notes, medical certificates, and other patient documents**. This allows the doctor to explore a patient's history through a conversational assistant rather than manually searching through every document.

### Prototype

MedLens is currently a **prototype / research-oriented project** focused on exploring how **Agentic AI, RAG, vector databases, and knowledge graphs** can work together to make longitudinal medical records easier to understand and retrieve.

The goal is not to replace existing clinical systems or medical professionals, but to demonstrate how an intelligent layer can sit on top of a patient's existing records and provide **context-aware access to medical history**.

> ⚠️ **Medical Disclaimer:** MedLens is an AI-assisted medical-record retrieval and summarization prototype. It is not a medical device or a substitute for professional clinical judgment. It does not diagnose diseases, prescribe medication, recommend treatment, or make independent clinical decisions.


------------------------------------------------------------------------

## ✨ Features

-   📄 Upload multiple medical records
-   🗂️ Classify medical documents
-   🔍 Extract text from medical documents
-   🧠 Extract structured medical information
-   📅 Generate a chronological medical timeline
-   🧬 Store patient relationships in Neo4j
-   🔎 Store semantic medical information in Qdrant
-   💬 Ask questions about the patient's medical records
-   🤖 Use GPT-4.1-mini for medical-record-based responses
-   📊 Display a patient dashboard in Streamlit
-   🔐 Keep the system based only on uploaded patient records

------------------------------------------------------------------------

## 🏗️ Architecture

MedLens uses two separate flows.

### 1. Medical Record Processing

This flow runs when the doctor uploads and analyzes medical records.

``` text
Medical Documents
       │
       ▼
Classification Agent
       │
       ▼
OCR / Document Reader
       │
       ▼
Medical Information Agent
       │
       ▼
Timeline Agent
       │
       ▼
Knowledge Base Agent
       │
       ├──────────────► Qdrant
       │                Semantic Medical Data
       │
       └──────────────► Neo4j
                        Patient Relationships
```

The processing graph is handled by LangGraph.

### 2. Doctor Chat

The doctor chat does **not** run the entire LangGraph again.

``` text
Doctor Question
       │
       ▼
MRI Agent
       │
       ├──────────────► Qdrant
       │                Relevant Medical Records
       │
       └──────────────► Neo4j
                        Patient Context
                │
                ▼
             GPT-4.1-mini
                │
                ▼
          Doctor's Answer
```

This separation keeps the chat considerably faster because document
processing and database storage happen once.

------------------------------------------------------------------------

## 🧰 Technologies Used

  Technology               Purpose
  ------------------------ ---------------------------------------------------------
  Python                   Main programming language
  Streamlit                Web interface
  LangGraph                Medical document processing workflow
  OpenAI API               Document understanding, extraction, embeddings and chat
  GPT-4.1-mini             Classification, extraction and doctor assistant
  text-embedding-3-small   Medical text embeddings
  Qdrant                   Vector database / semantic retrieval
  Neo4j                    Medical knowledge graph / relationships
  Docker                   Running Qdrant and Neo4j
  python-dotenv            Environment variable management

------------------------------------------------------------------------

# 🚀 Getting Started

## 1. Clone the repository

``` bash
git clone <your-repository-url>
cd MedLens_MRI
```

------------------------------------------------------------------------

## 2. Install Docker

MedLens requires Docker because **Qdrant and Neo4j run as services**.

Install Docker Desktop:

https://www.docker.com/products/docker-desktop/

Make sure Docker Desktop is running before starting MedLens.

------------------------------------------------------------------------

## 3. Start Qdrant

Run:

``` bash
docker run -d \
  --name medlens-qdrant \
  -p 6333:6333 \
  qdrant/qdrant
```

Qdrant will be available at:

``` text
http://localhost:6333
```

------------------------------------------------------------------------

## 4. Start Neo4j

Run:

``` bash
docker run -d \
  --name medlens-neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j
```

Neo4j Browser will be available at:

``` text
http://localhost:7474
```

Neo4j Bolt connection:

``` text
bolt://localhost:7687
```

Credentials:

``` text
Username: neo4j
Password: password
```

------------------------------------------------------------------------

# 🐍 5. Create a Python Virtual Environment

It is recommended to run MedLens inside a virtual environment.

### Windows

``` bash
python -m venv venv
```

Activate it:

``` bash
venv\Scripts\activate
```

You should see something similar to:

``` text
(venv)
```

before your terminal prompt.

### Linux / macOS

``` bash
python3 -m venv venv
```

Activate it:

``` bash
source venv/bin/activate
```

------------------------------------------------------------------------

# 📦 6. Install Dependencies

With the virtual environment activated:

``` bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt` yet, install the required
packages according to the project's dependency configuration.

------------------------------------------------------------------------

# 🔑 7. Create the `.env` File

Create a file named:

``` text
.env
```

in the root directory of the project.

Add:

``` env
OPENAI_API_KEY=your_openai_api_key

QDRANT_HOST=localhost
QDRANT_PORT=6333

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

Replace:

``` text
your_openai_api_key
```

with your actual OpenAI API key.

### ⚠️ Do not commit `.env`

Make sure `.env` is included in `.gitignore`.

Example:

``` gitignore
.env
venv/
__pycache__/
uploads/
```

------------------------------------------------------------------------

# ▶️ 8. Run MedLens

Make sure:

-   Docker Desktop is running
-   Qdrant container is running
-   Neo4j container is running
-   Virtual environment is activated
-   `.env` is configured

Then run:

``` bash
streamlit run app.py
```

Streamlit will provide a local address, normally:

``` text
http://localhost:8501
```

Open it in your browser.

------------------------------------------------------------------------

# 🩺 Using MedLens

## Step 1 --- Upload Medical Records

Upload one or multiple:

``` text
PDF
PNG
JPG
JPEG
```

medical records.

Examples:

-   Prescriptions
-   Lab reports
-   Discharge summaries
-   Radiology reports
-   Clinical notes
-   Medical certificates
-   Insurance documents

------------------------------------------------------------------------

## Step 2 --- Analyze Records

Click:

``` text
Analyze Records
```

MedLens processes the uploaded records through the LangGraph pipeline.

The extracted information is then stored in:

### Qdrant

For semantic retrieval.

### Neo4j

For relationships between:

``` text
Patient
│
├── Diagnosis
├── Medication
├── Medical Test
├── Doctor
├── Hospital
└── Document
```

------------------------------------------------------------------------

## Step 3 --- View Patient Dashboard

The dashboard displays information extracted from the patient's records,
including:

-   Patient name
-   Age
-   Gender
-   Hospital
-   Doctor
-   Medical history
-   Allergies
-   Diagnoses
-   Medications
-   Laboratory results
-   Medical timeline
-   Uploaded medical documents

------------------------------------------------------------------------

## Step 4 --- Ask the Doctor Assistant

After the records have been processed, use:

``` text
Doctor Assistant
```

to ask questions such as:

``` text
What diagnoses does this patient have?

What medications is the patient currently taking?

What was the patient's previous medical history?

Show me the patient's laboratory findings.

When was hypertension first documented?

What happened during the patient's previous hospital admission?

What medications were prescribed for diabetes?
```

The MRI agent retrieves relevant information from Qdrant and Neo4j
before sending the context to GPT-4.1-mini.

------------------------------------------------------------------------

# 🗃️ Project Structure

``` text
MedLens_MRI/
│
├── Agents/
│   ├── classification.py
│   ├── embeddings.py
│   ├── ocr.py
│   ├── medical_info.py
│   ├── timeline.py
│   ├── knowledge_base.py
│   └── mri.py
│
├── Database/
│   ├── qdrant.py
│   └── neo4j.py
│
├── Langgraph/
│   └── orchestrator.py
│
├── uploads/
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

------------------------------------------------------------------------

# 🧠 Why Qdrant + Neo4j?

MedLens uses two different types of medical memory.

## Qdrant --- Semantic Memory

Qdrant stores vector embeddings of relevant medical information.

For example:

``` text
Patient's prescription:
Metformin 500 mg twice daily
```

A doctor can ask:

``` text
What medication is the patient taking for diabetes?
```

The wording does not need to exactly match the stored text.

Qdrant retrieves semantically relevant information.

------------------------------------------------------------------------

## Neo4j --- Relationship Memory

Neo4j stores relationships between medical entities.

Example:

``` text
Patient
   │
   ├── HAS_DIAGNOSIS ──► Diabetes
   │
   ├── TAKES ──────────► Metformin
   │
   ├── UNDERWENT ──────► Blood Test
   │
   └── HAS_DOCUMENT ───► Prescription
```

This provides relationship and patient context that a basic vector
database alone cannot represent as naturally.

------------------------------------------------------------------------

# ⚡ Performance Design

MedLens intentionally separates **document ingestion** from **doctor
chat**.

### Document processing

Expensive operations such as:

``` text
Classification
OCR
Medical Information Extraction
Timeline Generation
Database Storage
```

run when the doctor analyzes the records.

### Doctor chat

After processing, the chat does not run those agents again.

Instead:

``` text
Question
   ↓
MRI Agent
   ↓
Qdrant + Neo4j
   ↓
GPT
   ↓
Answer
```

This avoids unnecessarily reprocessing the patient's documents for every
question.

------------------------------------------------------------------------

# 🔒 Medical Safety

MedLens is designed as a medical-record intelligence assistant.

It should:

-   Use information from uploaded records
-   Clearly state when information is unavailable
-   Avoid inventing patient information
-   Avoid diagnosing diseases
-   Avoid prescribing medications
-   Avoid recommending treatments
-   Avoid making unsupported assumptions

MedLens is **not a replacement for a qualified medical professional**.

------------------------------------------------------------------------

# 🛠️ Troubleshooting

## Qdrant connection error

Check that Docker is running:

``` bash
docker ps
```

You should see the Qdrant container.

If it is stopped:

``` bash
docker start medlens-qdrant
```

------------------------------------------------------------------------

## Neo4j connection error

Check:

``` bash
docker ps
```

Start the container if necessary:

``` bash
docker start medlens-neo4j
```

Neo4j should be available on:

``` text
bolt://localhost:7687
```

------------------------------------------------------------------------

## Python package error

Make sure the virtual environment is activated:

### Windows

``` bash
venv\Scripts\activate
```

Then:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## OpenAI API error

Check that `.env` contains:

``` env
OPENAI_API_KEY=your_openai_api_key
```

Restart Streamlit after changing `.env`.

------------------------------------------------------------------------

# 🚧 Future Improvements

Potential future versions may include:

-   Pydantic Structured Outputs
-   More granular medical embeddings
-   Better retrieval filtering
-   Patient-specific Qdrant collections
-   Advanced Neo4j medical relationships
-   Persistent doctor accounts
-   Authentication and authorization
-   PostgreSQL for application data
-   Persistent chat history
-   Audit logs
-   Multi-hospital support
-   Better OCR for handwritten documents
-   Evaluation and retrieval benchmarks

------------------------------------------------------------------------

# 👨‍💻 Author

**Jujare Naresh**

Built as an AI/GenAI project focused on medical document intelligence,
RAG, knowledge graphs, and conversational AI.

------------------------------------------------------------------------

## ⚠️ Disclaimer

This project is intended for educational, research, and demonstration
purposes.

Do not use MedLens as the sole basis for clinical decisions, diagnosis,
medication changes, or treatment decisions.


Do not use MedLens as the sole basis for clinical decisions, diagnosis,
medication changes, or treatment decisions.
#   M e d d L e n s _ M R I 
 
 
