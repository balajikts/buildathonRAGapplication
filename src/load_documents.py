from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)


DATA_DIR = Path("data")


# --------------------------------------------------
# LOAD ALL TXT FILES
# --------------------------------------------------

def load_txt_files():

    documents = []

    txt_files = list(DATA_DIR.glob("*.txt"))

    for file_path in txt_files:

        print(f"Loading TXT: {file_path.name}")

        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

        txt_documents = loader.load()

        for doc in txt_documents:

            doc.metadata["source_type"] = "TXT"
            doc.metadata["file_name"] = file_path.name

        documents.extend(txt_documents)

    return documents


# --------------------------------------------------
# LOAD ALL PDF FILES
# --------------------------------------------------

def load_pdf_files():

    documents = []

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    for file_path in pdf_files:

        print(f"Loading PDF: {file_path.name}")

        loader = PyPDFLoader(
            str(file_path)
        )

        pdf_documents = loader.load()

        for doc in pdf_documents:

            doc.metadata["source_type"] = "PDF"
            doc.metadata["file_name"] = file_path.name

        documents.extend(pdf_documents)

    return documents


# --------------------------------------------------
# LOAD ALL DOCUMENTS
# --------------------------------------------------

def load_all_documents():

    txt_documents = load_txt_files()
    pdf_documents = load_pdf_files()

    all_documents = (
        txt_documents +
        pdf_documents
    )

    print(
        f"\nTXT documents loaded : "
        f"{len(txt_documents)}"
    )

    print(
        f"PDF pages loaded     : "
        f"{len(pdf_documents)}"
    )

    print(
        f"Total documents      : "
        f"{len(all_documents)}"
    )

    return all_documents


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    documents = load_all_documents()

    print("\nLoaded Sources:")

    for document in documents:

        print(
            document.metadata.get(
                "file_name",
                "Unknown"
            )
        )