# 🩺 MedLens — Medical Report Intelligence

> **“See every patient's history through one intelligent lens.”**

**MedLens** is a prototype medical document intelligence and doctor-assistance system designed to bring a patient's scattered medical records together into one intelligent view.

Built with **Python, LangGraph, OpenAI, Qdrant, Neo4j, and Streamlit**, MedLens processes multiple medical documents, extracts relevant medical information, builds a chronological view of the patient's history, and combines **semantic retrieval with a medical knowledge graph** to help doctors understand patient records more efficiently.

Instead of treating every report as an isolated document, MedLens connects information across **prescriptions, laboratory reports, discharge summaries, radiology reports, consultation notes, medical certificates, and other patient records**. Doctors can then explore the patient's history through a conversational assistant rather than manually searching through every document.

## ✨ Features

- 📄 Upload multiple patient medical records
- 🗂️ Classify different medical document types
- 🔍 Extract text from PDFs and medical images
- 🧠 Extract structured medical information
- 📅 Generate a chronological medical timeline
- 🔎 Store and retrieve medical information using Qdrant
- 🧬 Represent patient relationships using Neo4j
- 💬 Ask questions about uploaded patient records
- 🤖 Use GPT-4.1-mini for medical-record-based responses
- 📊 Display extracted information through a Streamlit dashboard
- ⚡ Keep document processing separate from doctor chat for faster queries

## 🧪 Prototype

MedLens is currently a **prototype / research-oriented project** exploring how **Agentic AI, RAG, vector databases, and knowledge graphs** can work together to make longitudinal medical records easier to understand and retrieve.

The prototype focuses on building an intelligent layer over existing patient records. It is not intended to replace hospital information systems, electronic health record platforms, or medical professionals.

The current architecture separates **document ingestion** from **doctor conversation**. Medical records are processed and stored once; subsequent doctor questions retrieve relevant information from the existing knowledge base instead of re-running the complete document-processing pipeline.

## 🏗️ Architecture

### 1. Medical Record Processing

When records are uploaded and analyzed, MedLens processes them through a LangGraph workflow:

```text
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
       │                Semantic Medical Memory
       │
       └──────────────► Neo4j
                        Patient Relationships
```

### 2. Doctor Assistant

After the records have been processed, the doctor chat uses only the retrieval and reasoning path:

```text
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

This prevents every doctor question from triggering classification, OCR, medical information extraction, timeline generation, and database ingestion again.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface and dashboard |
| LangGraph | Agent workflow orchestration |
| OpenAI API | Document understanding, extraction, embeddings and chat |
| GPT-4.1-mini | Classification, extraction and doctor assistant |
| text-embedding-3-small | Medical text embeddings |
| Qdrant | Vector database and semantic retrieval |
| Neo4j | Medical knowledge graph and relationships |
| Docker | Running Qdrant and Neo4j |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
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
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Before running MedLens, install:

- Python 3.11+
- Docker Desktop
- Git
- An OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/Naresh-4ai/MedLens_MRI.git
cd MedLens_MRI
```

### 2. Start Docker

MedLens uses Docker to run **Qdrant** and **Neo4j**.

Make sure Docker Desktop is installed and running.

Start both services:

```bash
docker compose up -d
```

Check that they are running:

```bash
docker ps
```

You should see containers for:

```text
medlens_qdrant
medlens_neo4j
```

### 3. Qdrant

Qdrant is exposed on:

```text
http://localhost:6333
```

Default configuration:

```text
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

### 4. Neo4j

Neo4j Browser:

```text
http://localhost:7474
```

Bolt connection:

```text
bolt://localhost:7687
```

Default credentials:

```text
Username: neo4j
Password: password
```

### 5. Create a Python virtual environment

#### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 6. Install dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

### 7. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

QDRANT_HOST=localhost
QDRANT_PORT=6333

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

Replace `your_openai_api_key` with your actual OpenAI API key.

**Never commit your `.env` file or expose your API key publicly.**

### 8. Run MedLens

Make sure:

- Docker Desktop is running
- Qdrant is running
- Neo4j is running
- The Python virtual environment is activated
- `.env` is configured

Then run:

```bash
streamlit run app.py
```

Open the Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

## 🩺 Using MedLens

### Step 1 — Upload Records

Upload one or multiple medical records.

Supported formats:

```text
PDF
PNG
JPG
JPEG
```

Examples include:

- Prescriptions
- Lab reports
- Discharge summaries
- Radiology reports
- Clinical notes
- Medical certificates
- Insurance documents

### Step 2 — Analyze Records

Click:

```text
Analyze Records
```

MedLens processes the uploaded documents through the LangGraph pipeline.

The extracted information is then stored in the knowledge base.

### Step 3 — Patient Dashboard

The dashboard presents information extracted from the records, including:

- Patient name
- Age
- Gender
- Hospital
- Doctor
- Medical history
- Allergies
- Diagnoses
- Medications
- Laboratory results
- Medical timeline
- Uploaded medical documents

### Step 4 — Doctor Assistant

After processing, use the **Doctor Assistant** to ask questions about the patient's records.

Examples:

```text
What diagnoses does this patient have?

What medications is the patient taking?

What is the patient's previous medical history?

Show me the patient's laboratory findings.

When was hypertension first documented?

What happened during the previous hospital admission?

What medications were documented for diabetes?
```

The MRI agent retrieves relevant information from Qdrant and patient context from Neo4j before sending the available evidence to GPT-4.1-mini.

## 🧠 Why Qdrant + Neo4j?

MedLens uses two complementary forms of medical memory.

### Qdrant — Semantic Memory

Qdrant stores vector embeddings of medical text for semantic retrieval.

For example:

```text
Patient's prescription:
Metformin 500 mg twice daily
```

A doctor could ask:

```text
What medication is the patient taking for diabetes?
```

The wording does not need to exactly match the original document. Semantic retrieval can identify relevant information based on meaning.

### Neo4j — Relationship Memory

Neo4j represents relationships between medical entities.

For example:

```text
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

This allows MedLens to maintain relationships between patients, diagnoses, medications, tests, doctors, hospitals, and documents.

## ⚡ Performance Design

MedLens intentionally separates **document processing** from **doctor chat**.

### Document Processing

```text
Classification
     ↓
OCR / Document Reading
     ↓
Medical Information Extraction
     ↓
Timeline Generation
     ↓
Knowledge Base Storage
```

### Doctor Chat

```text
Doctor Question
      ↓
MRI Agent
      ↓
Qdrant + Neo4j
      ↓
GPT-4.1-mini
      ↓
Answer
```

The document-processing agents are therefore not unnecessarily executed for every question.

## 🔒 Medical Safety

MedLens is an AI-assisted medical-record retrieval and summarization prototype.

The system is designed to:

- Use information from uploaded records
- Clearly state when information is unavailable
- Avoid inventing patient information
- Avoid diagnosing diseases
- Avoid prescribing medication
- Avoid recommending treatment
- Avoid making unsupported assumptions

> **Medical Disclaimer:** MedLens is a prototype for educational, research, and demonstration purposes. It is not a medical device and is not a substitute for qualified clinical judgment. Do not use MedLens as the sole basis for diagnosis, medication changes, treatment decisions, or other clinical decisions.

## 🛠️ Troubleshooting

### Qdrant Connection Error

Check Docker:

```bash
docker ps
```

If the container is stopped:

```bash
docker start medlens_qdrant
```

Or start the complete stack:

```bash
docker compose up -d
```

Qdrant should be available at:

```text
http://localhost:6333
```

### Neo4j Connection Error

Check:

```bash
docker ps
```

If the container is stopped:

```bash
docker start medlens_neo4j
```

Neo4j should be available at:

```text
bolt://localhost:7687
```

If Neo4j has just been started, wait several seconds for the database to finish initializing.

### Python Package Error

Make sure the virtual environment is activated.

Windows:

```powershell
venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

### OpenAI API Error

Check that `.env` contains:

```env
OPENAI_API_KEY=your_openai_api_key
```

Restart Streamlit after changing the environment variables.

## 🚧 Future Improvements

Possible future versions of MedLens may include:

- Pydantic Structured Outputs
- More granular medical embeddings
- Improved retrieval filtering
- Patient-specific vector collections
- More advanced Neo4j medical relationships
- Better OCR for handwritten documents
- Persistent doctor accounts
- Authentication and authorization
- Persistent chat history
- Audit logs
- Multi-hospital support
- Retrieval evaluation and benchmarking
- Improved medical document processing

## 👨‍💻 Author

**Jujare Naresh**

MedLens is an AI/GenAI project exploring medical document intelligence, RAG, vector databases, knowledge graphs, and conversational AI.

---

> **MedLens — See every patient's history through one intelligent lens.**
