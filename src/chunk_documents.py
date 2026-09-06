from src.load_documents import load_all_documents
from src.metadata import add_metadata

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def display_chunks(chunks):

    print("\n===== CHUNK INFORMATION =====")

    print(f"Total chunks created: {len(chunks)}")

    for index, chunk in enumerate(chunks[:5]):

        print(f"\nChunk {index + 1}")
        print("--------------------")

        print("Content:")
        print(chunk.page_content[:300])

        print("\nMetadata:")
        print(chunk.metadata)


if __name__ == "__main__":

    # Step 1: Load documents
    documents = load_all_documents()

    # Step 2: Add metadata
    enriched_documents = add_metadata(documents)

    # Step 3: Split documents
    chunks = split_documents(enriched_documents)

    # Step 4: Display result
    display_chunks(chunks)