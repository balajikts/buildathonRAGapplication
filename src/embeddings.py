from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from src.chunk_documents import split_documents
from src.load_documents import load_all_documents
from src.metadata import add_metadata


load_dotenv()


CHROMA_PATH = "chroma_db"


def create_vector_database():

    print("Loading documents...")

    documents = load_all_documents()

    print("Adding metadata...")

    enriched_documents = add_metadata(documents)

    print("Creating chunks...")

    chunks = split_documents(enriched_documents)

    print(f"Total chunks: {len(chunks)}")

    print("Creating embeddings...")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    print("Creating Chroma vector database...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="gym_rag"
    )

    print("\nVector database created successfully!")

    print(f"Database location: {CHROMA_PATH}")

    return vectorstore


if __name__ == "__main__":

    create_vector_database()