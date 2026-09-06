from pathlib import Path

import langchain_community.document_loaders

DATA_DIR = Path("data")


def load_txt_file():
    file_path = DATA_DIR / "exercise.txt"

    loader = langchain_community.document_loaders.TextLoader(
        str(file_path),
        encoding="utf-8"
    )

    documents = loader.load()

    for doc in documents:
        doc.metadata["source_type"] = "TXT"
        doc.metadata["file_name"] = file_path.name

    return documents


def load_pdf_file():
    file_path = DATA_DIR / "trainer_directory_30_pages.pdf"

    loader = langchain_community.document_loaders.PyPDFLoader(str(file_path))

    documents = loader.load()

    for doc in documents:
        doc.metadata["source_type"] = "PDF"
        doc.metadata["file_name"] = file_path.name

    return documents


def load_all_documents():

    txt_documents = load_txt_file()
    pdf_documents = load_pdf_file()

    all_documents = txt_documents + pdf_documents

    print(f"TXT documents loaded : {len(txt_documents)}")
    print(f"PDF pages loaded     : {len(pdf_documents)}")
    print(f"Total documents      : {len(all_documents)}")

    return all_documents


if __name__ == "__main__":
    documents = load_all_documents()

    print("\nFirst document:")
    print(documents[0])
    print("\nMetadata:")
    print(documents[0].metadata)