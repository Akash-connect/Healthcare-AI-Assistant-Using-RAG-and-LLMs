import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.rag import RAGPipeline
from app.agent import HealthcareAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Healthcare AI Assistant",
    description="Healthcare-focused RAG AI Assistant using FastAPI, ChromaDB, and LLMs",
    version="1.0.0"
)


rag_pipeline = RAGPipeline()
agent = HealthcareAgent()


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {
        "status": "running",
        "message": "Healthcare AI Assistant API is healthy"
    }


@app.post("/ingest")
def ingest_documents():
    try:
        start_time = time.time()

        document_count, chunk_count = rag_pipeline.ingest_documents()

        processing_time = round(time.time() - start_time, 2)

        logging.info(
            f"Ingestion completed. Documents: {document_count}, Chunks: {chunk_count}"
        )

        return {
            "message": "Documents ingested successfully",
            "documents": document_count,
            "chunks": chunk_count,
            "processing_time_seconds": processing_time
        }

    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        start_time = time.time()

        result = agent.ask(request.question)

        processing_time = round(time.time() - start_time, 2)

        logging.info(f"Question answered using workflow: {result.get('workflow')}")

        result["processing_time_seconds"] = processing_time

        return result

    except HTTPException:
        raise

    except Exception as e:
        logging.error(f"Question answering failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))