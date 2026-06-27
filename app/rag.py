from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma

from app.embeddings import get_embedding_model
from app.config import settings


class RAGPipeline:
    def __init__(self):
        self.embedding = get_embedding_model()
        self.vector_db = None

    def ingest_documents(self):
        loader = DirectoryLoader(
            settings.DATA_DIR,
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )

        documents = loader.load()

        if not documents:
            raise ValueError("No documents found in data folder.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(documents)

        self.vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding,
            persist_directory=settings.VECTOR_DB_DIR
        )

        return len(documents), len(chunks)

    def load_vector_db(self):
        self.vector_db = Chroma(
            persist_directory=settings.VECTOR_DB_DIR,
            embedding_function=self.embedding
        )

    def retrieve_with_scores(self, question: str):
        if self.vector_db is None:
            self.load_vector_db()

        results = self.vector_db.similarity_search_with_score(
            question,
            k=settings.TOP_K
        )

        return results