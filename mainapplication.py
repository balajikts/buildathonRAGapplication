import streamlit as st

from src.rag import ask_question
from src.excel_logger import log_rag_result
from src.dashboard import show_dashboard


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Infinity Fitness AI",
    page_icon="🏋️",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏋️ Infinity Fitness Gym AI Assistant")

st.markdown(
    """
Ask questions about:

- 💪 Exercises - Targeted for each Muscle
- 🏃 Training information
- 👤 Trainers and Certification Information
- 💵 Membership Tariff
- 📄 Information available in the provided documents
"""
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("RAG Application")

    st.write(
        """
        **Knowledge Sources**

        📄 Exercises Manual  
        📑 Trainer's Information
        💵 Gym Membership Tariff

        **AI Components**

        🔎 Chroma Retriever  
        🧠 OpenAI LLM  
        📊 LangSmith  
        📗 Excel Logging
        """
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🤖 AI Assistant",
            "📊 Metrics Dashboard"
        ]
    )

    st.divider()

    st.info(
        "Answers are generated only from the "
        "documents provided to the RAG system."
    )


# ==================================================
# METRICS DASHBOARD
# ==================================================

if page == "📊 Metrics Dashboard":

    show_dashboard()


# ==================================================
# AI ASSISTANT
# ==================================================

else:

    # --------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------

    with st.form("rag_question_form"):

        question = st.text_input(
            "Ask your question:",
            placeholder="Example: What exercises target the chest?"
        )

        submitted = st.form_submit_button(
            "🔍 Search",
            type="primary"
        )


    # --------------------------------------------------
    # RUN RAG
    # --------------------------------------------------

    if submitted:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "Thinking... Please wait..."
            ):

                try:

                    # ------------------------------------------
                    # RUN RAG
                    # ------------------------------------------

                    result = ask_question(question)

                    # Store result permanently in session
                    st.session_state.result = result

                    answer = result["answer"]
                    documents = result["documents"]
                    status = result["status"]
                    latency = result["latency"]
                    retrieved_chunks = result["retrieved_chunks"]


                    # ------------------------------------------
                    # EXCEL LOGGING
                    # ------------------------------------------

                    log_rag_result(
                        question=question,
                        answer=answer,
                        status=status,
                        documents=documents
                        if status == "SUCCESS"
                        else [],
                        latency=latency
                    )


                except Exception as error:

                    st.error(
                        "Sorry, the RAG application "
                        "encountered an error."
                    )

                    st.exception(error)

                    try:

                        log_rag_result(
                            question=question,
                            answer=str(error),
                            status="FAILED",
                            documents=[],
                            latency=0
                        )

                    except Exception:

                        pass


    # ==================================================
    # DISPLAY STORED RESULT
    # ==================================================

    if st.session_state.result is not None:

        result = st.session_state.result

        answer = result["answer"]
        documents = result["documents"]
        status = result["status"]
        latency = result["latency"]
        retrieved_chunks = result["retrieved_chunks"]


        # ------------------------------------------
        # RESPONSE
        # ------------------------------------------

        if status == "NOT_FOUND":

            st.warning(
                "⚠️ No such data is available "
                "in the provided documents."
            )

        elif status == "SUCCESS":

            st.subheader("🤖 AI Answer")

            st.write(answer)


            # ------------------------------------------
            # SOURCES
            # ------------------------------------------

            st.subheader("📚 Sources")

            displayed_sources = set()

            for document in documents:

                metadata = document.metadata

                source_file = metadata.get(
                    "source_file",
                    "Unknown"
                )

                page_number = metadata.get(
                    "page_number",
                    "N/A"
                )

                category = metadata.get(
                    "document_category",
                    "Unknown"
                )

                source_key = (
                    source_file,
                    page_number
                )

                if source_key not in displayed_sources:

                    displayed_sources.add(
                        source_key
                    )

                    st.write(
                        f"📄 **File:** {source_file}"
                    )

                    st.write(
                        f"📂 **Category:** {category}"
                    )

                    st.write(
                        f"📑 **Page:** {page_number}"
                    )

                    st.divider()


        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        if status == "SUCCESS":

            st.success(
                "Response generated and logged successfully."
            )

        elif status == "NOT_FOUND":

            st.info(
                "Question processed and logged as NOT_FOUND."
            )


        # ------------------------------------------
        # RAG DEBUG PANEL
        # ------------------------------------------

        with st.expander(
            "🔍 RAG Debug Details"
        ):

            st.write(
                f"**User Query:** "
                f"{result['question']}"
            )

            st.write(
                f"**Response Status:** "
                f"{status}"
            )

            st.write(
                f"**Retrieved Chunks:** "
                f"{retrieved_chunks}"
            )

            st.write(
                f"**Response Latency:** "
                f"{latency} seconds"
            )

            st.write(
                "**LangSmith Project:** "
                "Gym-RAG-Demo"
            )


            st.divider()

            st.subheader(
                "Retrieved Documents"
            )


            for index, document in enumerate(
                documents,
                start=1
            ):

                metadata = document.metadata

                st.write(
                    f"### Chunk {index}"
                )

                st.write(
                    "**Source:** "
                    f"{metadata.get('source_file', 'Unknown')}"
                )

                st.write(
                    "**Category:** "
                    f"{metadata.get('document_category', 'Unknown')}"
                )

                st.write(
                    "**Content Type:** "
                    f"{metadata.get('content_type', 'Unknown')}"
                )

                st.write(
                    "**Page:** "
                    f"{metadata.get('page_number', 'N/A')}"
                )

                st.code(
                    document.page_content,
                    language="text"
                )

                st.divider()