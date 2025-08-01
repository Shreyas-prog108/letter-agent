# ingest.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS  # ✅ Replaced Chroma

load_dotenv()

DATA_PATH = "data/"
DB_PATH = "db/"

def ingest_data():
    print("🚀 Starting data ingestion...")
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.pdf')]
    documents = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(os.path.join(DATA_PATH, pdf_file))
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_docs = text_splitter.split_documents(documents)
    print(f"📄 Loaded and split {len(chunked_docs)} document chunks.")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vector_store = FAISS.from_documents(chunked_docs, embeddings)
    vector_store.save_local(DB_PATH)
    print(f"🎉 Data ingestion complete. FAISS vector store saved at: {DB_PATH}")

if __name__ == '__main__':
    ingest_data()
