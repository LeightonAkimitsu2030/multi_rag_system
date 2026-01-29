import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_dbs():
    # Use Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # 1. Swiss Airline Poli cy DB
    if os.path.exists('data/unstructured_docs/swiss_airline_policy/'):
        policy_loader = DirectoryLoader('data/unstructured_docs/swiss_airline_policy/', glob="**/*.pdf", loader_cls=PyPDFLoader)
        policy_docs = policy_loader.load_and_split(splitter)
        Chroma.from_documents(policy_docs, embeddings, persist_directory="data/airline_policy_vectordb")

    # 2. Stories DB
    if os.path.exists('data/unstructured_docs/stories/'):
        stories_loader = DirectoryLoader('data/unstructured_docs/stories/', glob="**/*.txt")
        stories_docs = stories_loader.load_and_split(splitter)
        Chroma.from_documents(stories_docs, embeddings, persist_directory="data/stories_vectordb")

if __name__ == "__main__":
    create_dbs()
    print("Vector databases created successfully using Gemini Embeddings.")