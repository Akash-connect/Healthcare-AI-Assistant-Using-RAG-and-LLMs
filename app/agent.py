import os

from app.rag import RAGPipeline
from app.llm import GeminiLLM
from app.tools import check_available_slots, extract_department, extract_date


class HealthcareAgent:
    def __init__(self):
        self.rag = RAGPipeline()
        self.llm = GeminiLLM()

    def is_appointment_query(self, question: str) -> bool:
        keywords = [
            "appointment",
            "book",
            "slot",
            "schedule",
            "doctor available",
            "availability"
        ]

        question_lower = question.lower()
        return any(keyword in question_lower for keyword in keywords)

    def relevance_label(self, score: float) -> str:
        if score <= 0.8:
            return "High"
        elif score <= 1.2:
            return "Medium"
        return "Low"

    def confidence_from_scores(self, scores) -> str:
        if not scores:
            return "low"

        best_score = min(scores)

        if best_score <= 0.8:
            return "high"
        elif best_score <= 1.2:
            return "medium"
        return "low"

    def clean_document_name(self, path: str) -> str:
        return os.path.basename(path.replace("\\", "/"))

    def ask(self, question: str):
        if self.is_appointment_query(question):
            department = extract_department(question)
            date = extract_date(question)
            tool_result = check_available_slots(department, date)

            return {
                "answer": tool_result["message"],
                "sources": [
                    {
                        "document": "mock_appointment_tool",
                        "excerpt": "Appointment availability is generated using a mock tool for demo purposes.",
                        "relevance": "High"
                    }
                ],
                "confidence": "medium",
                "workflow": "appointment_tool",
                "tool_result": tool_result
            }

        retrieved_results = self.rag.retrieve_with_scores(question)

        if not retrieved_results:
            return {
                "answer": "I could not find this information in the provided documents.",
                "sources": [],
                "confidence": "low",
                "workflow": "rag"
            }

        docs = [item[0] for item in retrieved_results]
        scores = [item[1] for item in retrieved_results]

        confidence = self.confidence_from_scores(scores)

        if confidence == "low":
            return {
                "answer": "I could not find this information in the provided documents.",
                "sources": [],
                "confidence": "low",
                "workflow": "rag"
            }

        context = "\n\n".join([doc.page_content for doc in docs])
        answer = self.llm.generate_answer(question, context)

        sources = []

        for doc, score in retrieved_results:
            sources.append({
                "document": self.clean_document_name(doc.metadata.get("source", "unknown")),
                "excerpt": doc.page_content[:450],
                "relevance": self.relevance_label(score)
            })

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "workflow": "rag"
        }