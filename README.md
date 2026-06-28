#  Healthcare AI Assistant Using RAG and LLMs

## Overview

This project is a healthcare-focused AI assistant built as part of the **AI Engineer Hackathon Assignment**.

The goal of this project is to answer healthcare-related questions using a **Retrieval-Augmented Generation (RAG)** pipeline instead of relying only on the language model. The assistant retrieves relevant information from a healthcare knowledge base, generates a grounded response, and provides the document(s) used to answer the question.

To demonstrate a simple agentic workflow, appointment-related queries are routed to a mock appointment scheduling tool, while all document-related questions are handled using the RAG pipeline.

The project uses a **local Mistral model through Ollama**, allowing it to run completely offline without depending on external LLM APIs.

---

# Features

* Retrieval-Augmented Generation (RAG)
* Healthcare knowledge base using synthetic documents
* Local LLM with Ollama (Mistral)
* ChromaDB for vector storage
* HuggingFace embeddings
* Source citations with every answer
* Mock appointment booking tool
* FastAPI REST API
* Streamlit web interface
* Docker support
* Logging and environment-based configuration

---

# Tech Stack

| Component       | Technology                             |
| --------------- | -------------------------------------- |
| Backend         | FastAPI                                |
| Frontend        | Streamlit                              |
| LLM             | Ollama + Mistral                       |
| Embeddings      | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB                               |
| Framework       | LangChain                              |
| Language        | Python                                 |
| Deployment      | Docker                                 |

---

# Project Workflow

The application follows a simple RAG pipeline.

1. Healthcare documents are loaded from the **data** folder.
2. Documents are split into smaller chunks.
3. Each chunk is converted into vector embeddings.
4. Embeddings are stored in ChromaDB.
5. When a user asks a question, relevant chunks are retrieved.
6. The retrieved context is passed to the local Mistral model.
7. The assistant generates a grounded answer and returns the supporting document references.

For appointment-related questions, the request is routed directly to a mock appointment scheduling tool instead of the RAG pipeline.

---

# Project Structure

```text
healthcare-ai-assistant/

├── app/
│   ├── main.py
│   ├── rag.py
│   ├── llm.py
│   ├── embeddings.py
│   ├── agent.py
│   ├── tools.py
│   ├── config.py
│   ├── prompt.py
│   └── logger.py
│
├── data/
├── tests/
├── logs/
├── vector_store/
│
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .env.example
```

---

# Dataset

The knowledge base consists of six synthetic healthcare documents covering:

* Telehealth Consultation Guidelines
* Medication Refill Policy
* HIPAA Privacy Guidelines
* Appointment Scheduling Policy
* Insurance Eligibility FAQ
* Patient Discharge Instructions

No real patient information or PHI has been used in this project.

---

# API Endpoints

### Health Check

```http
GET /health
```

Returns the application status.

---

### Document Ingestion

```http
POST /ingest
```

Reads healthcare documents, creates embeddings, and stores them in ChromaDB.

---

### Ask a Question

```http
POST /ask
```

Example request

```json
{
    "question":"Can a patient request a medication refill through telehealth?"
}
```

Example response

```json
{
    "answer":"Yes, patients can request medication refills through telehealth if the medication was previously prescribed.",
    "confidence":"high",
    "workflow":"rag",
    "sources":[
        {
            "document":"telehealth_policy.txt"
        }
    ]
}
```

---

# Sample Questions

### RAG Questions

* Can a patient request a medication refill through telehealth?
* What information is considered protected health information?
* When should a patient seek emergency medical care?
* What documents are required for insurance eligibility?

### Agent Tool Questions

* Can I book a cardiology appointment for Monday?
* Show available dermatology slots.
* Schedule a pediatrics appointment.

---

# Running the Project

Clone the repository

```bash
git clone <repository-url>
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

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

Run the backend

```bash
uvicorn app.main:app --reload
```

Open Swagger

```
http://127.0.0.1:8000/docs
```

Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

---




---

# Author

**Akash Jadhav**

