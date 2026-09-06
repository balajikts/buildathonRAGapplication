from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma



load_dotenv()

CHROMA_PATH = "chroma_db"


def create_retriever():

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma(
        collection_name="gym_rag",
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    return retriever


def search_documents(question):

    retriever = create_retriever()

    documents = retriever.invoke(question)

    print("\n========================================")
    print("QUESTION")
    print("========================================")

    print(question)

    print("\n========================================")
    print("RETRIEVED DOCUMENTS")
    print("========================================")

    for index, document in enumerate(documents, start=1):

        print(f"\n--- Result {index} ---")

        print("\nContent:")
        print(document.page_content)

        print("\nMetadata:")
        print(document.metadata)


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    search_documents(question)