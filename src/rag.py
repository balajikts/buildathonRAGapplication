import time

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import traceable

from src.retriever import create_retriever


load_dotenv()


def create_rag():

    retriever = create_retriever()

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    return retriever, llm


@traceable(name="Gym-RAG-Application")
def ask_question(question):

    start_time = time.perf_counter()

    retriever, llm = create_rag()

    # ------------------------------------------
    # RETRIEVAL
    # ------------------------------------------

    documents = retriever.invoke(question)

    # ------------------------------------------
    # BUILD CONTEXT
    # ------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # ------------------------------------------
    # PROMPT
    # ------------------------------------------

    prompt = f"""
You are a helpful Gym and Fitness information assistant.

Answer the user's question using ONLY the provided context.

If the answer is not available in the context, say:

"I could not find this information in the provided documents."

Do not invent information.

USER QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

    # ------------------------------------------
    # LLM
    # ------------------------------------------

    response = llm.invoke(prompt)

    answer = response.content

    # ------------------------------------------
    # RESPONSE STATUS
    # ------------------------------------------

    no_data_message = (
        "I could not find this information "
        "in the provided documents."
    )

    if no_data_message.lower() in answer.lower():
        status = "NOT_FOUND"
    else:
        status = "SUCCESS"

    # ------------------------------------------
    # LATENCY
    # ------------------------------------------

    end_time = time.perf_counter()

    latency = round(
        end_time - start_time,
        2
    )

    # ------------------------------------------
    # RETURN RESULT
    # ------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "documents": documents,
        "status": status,
        "latency": latency,
        "retrieved_chunks": len(documents)
    }