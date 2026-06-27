# 🏥 Healthcare AI Assistant Using RAG and LLMs

A healthcare-focused AI assistant built using **Retrieval-Augmented Generation (RAG)** that answers user questions from a healthcare knowledge base instead of relying only on the language model.

The project was developed as part of the **AI Engineer Hackathon Assignment**. The objective was to build a working prototype that demonstrates practical knowledge of RAG pipelines, LLM integration, vector databases, API development, and a simple agent-based workflow.

---

## Features

* Answer healthcare-related questions using a RAG pipeline
* Uses **ChromaDB** as the vector database
* Generates embeddings using **sentence-transformers/all-MiniLM-L6-v2**
* Runs completely offline using **Ollama + Mistral**
* Returns source citations for every answer
* Handles appointment-related queries using a separate routing tool
* REST API built with FastAPI
* Simple Streamlit interface
* Docker support
* Logging and environment-based configuration

---

## Tech Stack

| Technology             | Purpose              |
| ---------------------- | -------------------- |
| Python                 | Programming Language |
| FastAPI                | Backend API          |
| Streamlit              | Frontend             |
| LangChain              | RAG Pipeline         |
| ChromaDB               | Vector Database      |
| Ollama (Mistral)       | Local LLM            |
| HuggingFace Embeddings | Text Embeddings      |
| Docker                 | Containerization     |

---

# How it Works

1. Healthcare documents are loaded from the **data** folder.
2. Documents are split into smaller chunks.
3. Each chunk is converted into embeddings.
4. Embeddings are stored in **ChromaDB**.
5. When a user asks a question, relevant chunks are retrieved.
6. The retrieved context is sent to the local Mistral model.
7. The assistant generates an answer using only the retrieved information and also returns the source documents.

---

## Agent Workflow

The application supports two different workflows.

### 1. RAG Workflow

Used for healthcare-related questions.

Example:

> Can a patient request a medication refill through telehealth?

↓

Retrieve relevant document chunks

↓

Generate grounded answer using Mistral

↓

Return answer with citations

---

### 2. Appointment Tool

If the question is related to appointment booking, it is routed to a simple mock scheduling tool.

Example:

> Can I book a cardiology appointment for Monday?

↓

Appointment Router

↓

Mock Appointment Tool

↓

Available Time Slots

---

# Project Structure

```text
healthcare-ai-assistant/

├── app/
│   ├── main.py
│   ├── rag.py
│   ├── llm.py
│   ├── embeddings.py
│   ├── config.py
│   ├── prompt.py
│   ├── agent.py
│   ├── tools.py
│   └── logger.py
│
├── data/
│
├── vector_store/
│
├── logs/
│
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Healthcare Dataset

The project uses a small synthetic healthcare knowledge base containing:

* Telehealth Consultation Guidelines
* Medication Refill Policy
* HIPAA Privacy Guidelines
* Insurance Eligibility FAQ
* Appointment Scheduling Policy
* Patient Discharge Instructions

No real patient information or PHI has been used.

---

# API Endpoints

## Health Check

```http
GET /health
```

Checks whether the API is running.

---

## Ingest Documents

```http
POST /ingest
```

Loads healthcare documents, creates embeddings, and stores them in ChromaDB.

---

## Ask Question

```http
POST /ask
```

Example Request

```json
{
    "question":"Can a patient request a medication refill through telehealth?"
}
```

Example Response

```json
{
    "answer":"Yes...",
    "sources":[
        {
            "document":"telehealth_policy.txt"
        }
    ],
    "confidence":"high"
}
```

---

# Sample Questions

### RAG

* Can a patient request a medication refill through telehealth?
* What information is considered PHI?
* How can a patient verify insurance eligibility?
* What should a patient do after discharge?
* When should a patient seek emergency care?

### Appointment Tool

* Can I book a cardiology appointment for Monday?
* Show dermatology appointment slots.
* Schedule a pediatrics appointment.

---

# Running the Project

Clone the repository

```bash
git clone <repository-url>
cd healthcare-ai-assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start Ollama

```bash
ollama run mistral
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

Run Streamlit

```bash
streamlit run streamlit_app.py
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

---

# Future Improvements

Some features I would like to add in future versions:

* PDF and DOCX document support
* User authentication
* Conversation memory
* Hybrid Search (BM25 + Vector Search)
* Real hospital appointment API
* Cloud deployment
* Multi-language support
* Better evaluation metrics

---

# Author

**Akash Jadhav**

This project was developed as part of the AI Engineer Hackathon Assignment to demonstrate practical implementation of Retrieval-Augmented Generation, local LLM integration, vector search, and agent-based workflows in a healthcare use case.
