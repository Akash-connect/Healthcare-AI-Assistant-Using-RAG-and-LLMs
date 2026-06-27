import os
import time
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


def get_file_name(path: str) -> str:
    return os.path.basename(path.replace("\\", "/"))


st.set_page_config(
    page_title="Healthcare AI Assistant",
    page_icon="",
    layout="wide"
)

st.title(" Healthcare AI Assistant")
st.caption("RAG-based Healthcare Question Answering System")

with st.sidebar:
    st.header("System Status")

    try:
        health_response = requests.get(f"{API_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("Backend Connected")
        else:
            st.error("Backend Error")
    except Exception:
        st.error("Backend Not Running")

    st.divider()

    st.header("Technology Stack")
    st.write("FastAPI")
    st.write("LangChain")
    st.write("ChromaDB")
    st.write("Ollama Mistral")
    st.write("Streamlit")

    st.divider()

    st.header("Knowledge Base")

    if st.button("Ingest Documents", use_container_width=True):
        with st.spinner("Ingesting documents..."):
            response = requests.post(f"{API_URL}/ingest")

        if response.status_code == 200:
            data = response.json()
            st.success("Documents ingested")
            st.write(f"Documents: {data.get('documents')}")
            st.write(f"Chunks: {data.get('chunks')}")
        else:
            st.error("Ingestion failed")
            st.text(response.text)

st.subheader("Ask a Healthcare Question")

question = st.text_area(
    "Question",
    placeholder="Example: Can a patient request a medication refill through telehealth?",
    height=120,
    label_visibility="collapsed"
)

ask_button = st.button("Ask Assistant", type="primary")

if ask_button:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving context and generating answer..."):
            start_time = time.time()
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question},
                timeout=180
            )
            total_time = round(time.time() - start_time, 2)

        if response.status_code != 200:
            st.error("API error")
            st.text(response.text)
        else:
            result = response.json()

            st.divider()
            st.subheader("Answer")
            st.write(result.get("answer", ""))

            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Confidence", result.get("confidence", "N/A"))
            col2.metric("Workflow", result.get("workflow", "N/A"))
            col3.metric("Response Time", f"{total_time} sec")

            if result.get("workflow") == "appointment_tool" and "tool_result" in result:
                tool = result["tool_result"]

                st.divider()
                st.subheader("Appointment Availability")
                st.write(f"**Department:** {tool.get('department', '').title()}")
                st.write(f"**Date:** {tool.get('date', '')}")

                slots = tool.get("available_slots", [])
                if slots:
                    st.write("**Available Slots:**")
                    for slot in slots:
                        st.write(f"- {slot}")

            sources = result.get("sources", [])

            if sources:
                st.divider()
                st.subheader("Source Documents")

                for index, source in enumerate(sources, start=1):
                    document_name = get_file_name(
                        source.get("document", "Unknown Document")
                    )

                    with st.expander(f"{index}. {document_name}"):
                        relevance = source.get("relevance")

                        if relevance:
                            st.write(f"**Relevance:** {relevance}")

                        st.write(source.get("excerpt", source.get("chunk", "")))
            else:
                st.info("No source documents returned.")