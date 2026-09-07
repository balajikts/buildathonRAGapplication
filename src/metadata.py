def add_metadata(documents):

    enriched_documents = []

    for doc in documents:

        source_type = doc.metadata.get("source_type")
        file_name = doc.metadata.get("file_name", "")

        # ------------------------------------------
        # EXERCISE TXT
        # ------------------------------------------

        if (
            source_type == "TXT"
            and file_name.lower() == "exercise.txt"
        ):

            doc.metadata.update({
                "document_category": "exercise",
                "content_type": "exercise_information",
                "source_file": file_name
            })


        # ------------------------------------------
        # MEMBERSHIP TXT
        # ------------------------------------------

        elif (
            source_type == "TXT"
            and file_name.lower() == "gym_membership.txt"
        ):

            doc.metadata.update({
                "document_category": "membership",
                "content_type": "membership_information",
                "source_file": file_name
            })


        # ------------------------------------------
        # TRAINER PDF
        # ------------------------------------------

        elif source_type == "PDF":

            page_number = doc.metadata.get(
                "page",
                0
            )

            doc.metadata.update({
                "document_category": "trainer_directory",
                "content_type": "trainer_information",
                "source_file": file_name,
                "page_number": page_number + 1
            })


        enriched_documents.append(doc)

    return enriched_documents


# --------------------------------------------------
# DISPLAY METADATA
# --------------------------------------------------

def display_metadata(documents):

    print("\n===== METADATA =====")

    for index, doc in enumerate(documents[:10]):

        print(
            f"\nDocument {index + 1}"
        )

        print("--------------------")

        print(
            f"Source Type       : "
            f"{doc.metadata.get('source_type')}"
        )

        print(
            f"Category          : "
            f"{doc.metadata.get('document_category')}"
        )

        print(
            f"Content Type      : "
            f"{doc.metadata.get('content_type')}"
        )

        print(
            f"Source File       : "
            f"{doc.metadata.get('source_file')}"
        )

        print(
            f"Page Number       : "
            f"{doc.metadata.get('page_number', 'N/A')}"
        )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    from src.load_documents import load_all_documents

    documents = load_all_documents()

    enriched_documents = add_metadata(
        documents
    )

    display_metadata(
        enriched_documents
    )