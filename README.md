# 🏋️ Infinity Fitness Gym AI Assistant

An end-to-end **Retrieval-Augmented Generation (RAG)** application built with **Python, LangChain, ChromaDB, OpenAI, LangSmith, Streamlit, and Excel**.

The Infinity Fitness Gym AI Assistant allows users to ask questions about exercises, muscle groups, trainers, certifications, and other information available in the provided knowledge base.

The application retrieves relevant document chunks and generates grounded responses using an LLM.

---

# 🎯 Project Objective

The goal of this project is to demonstrate a practical **GenAI + RAG + QA** solution for a fitness domain.

The application demonstrates:

* 📄 PDF and TXT document ingestion
* ✂️ Document chunking
* 🏷️ Metadata enrichment
* 🔢 Vector embeddings
* 🔎 Semantic retrieval
* 🗄️ ChromaDB vector storage
* 🧠 OpenAI LLM integration
* 🔬 LangSmith tracing
* 📊 Excel execution logging
* ⚡ Response latency measurement
* 🧪 RAG debugging
* 📈 QA metrics dashboard
* 🖥️ Streamlit UI
* 💾 Streamlit session-state persistence

---

# 🏗️ Application Architecture

```text
                    USER
                      │
                      ▼
             ┌─────────────────┐
             │   Streamlit UI  │
             └────────┬────────┘
                      │
                      ▼
              User Question
                      │
                      ▼
             ┌─────────────────┐
             │  RAG Pipeline   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Chroma Retriever│
             └────────┬────────┘
                      │
                      ▼
              Relevant Chunks
                      │
                      ▼
             ┌─────────────────┐
             │ Context Builder │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   OpenAI LLM    │
             └────────┬────────┘
                      │
                      ▼
              Grounded Answer
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
       Sources     LangSmith    Excel Log
          │                        │
          └──────────┬─────────────┘
                     ▼
              QA Metrics Dashboard
```

---

# 📂 Project Structure

```text
Buildathon Gym App/
│
├── mainapplication.py
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── data/
│   ├── exercise.txt
│   └── trainer_directory_30_pages.pdf
│
├── chroma_db/
│
├── output/
│   └── rag_results.xlsx
│
└── src/
    ├── __init__.py
    ├── load_documents.py
    ├── metadata.py
    ├── chunk_documents.py
    ├── embeddings.py
    ├── retriever.py
    ├── rag.py
    ├── excel_logger.py
    └── dashboard.py
```

---

# 📚 Knowledge Sources

The current knowledge base contains two document types.

## 1. Exercise Manual

```text
data/exercise.txt
```

Contains exercise information organized around muscle groups.

Examples include:

* Chest
* Back
* Shoulders
* Legs
* Arms
* Core

---

## 2. Trainer Directory

```text
data/trainer_directory_30_pages.pdf
```

Contains trainer information including:

* Trainer ID
* Trainer name
* Specialization
* Certifications
* Experience
* Location

---

# 🔄 RAG Data Preparation Pipeline

Before users can query the application, the source documents go through the following pipeline:

```text
TXT / PDF
   ↓
Document Loader
   ↓
Metadata Enrichment
   ↓
Document Chunking
   ↓
OpenAI Embeddings
   ↓
ChromaDB
```

---

# 📄 Document Loading

`src/load_documents.py`

The application loads:

### TXT

Using LangChain's text document loader.

### PDF

Using LangChain's PDF loader.

Basic metadata is attached to the loaded documents.

Example:

```text
source_type
file_name
```

---

# 🏷️ Metadata Enrichment

`src/metadata.py`

Documents are enriched with metadata.

Typical metadata:

```text
document_category
content_type
source_file
page_number
```

Example:

```text
document_category = exercise
content_type = exercise_information
source_file = exercise.txt
```

For PDF content, page information is also retained.

Metadata enables better source tracking and QA validation.

---

# ✂️ Document Chunking

`src/chunk_documents.py`

The documents are divided into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

Current configuration:

```text
Chunk Size    : 500
Chunk Overlap : 50
```

Chunking improves semantic retrieval by allowing the vector database to search smaller sections of the documents.

---

# 🔢 Embeddings

`src/embeddings.py`

The application uses:

```text
OpenAI text-embedding-3-small
```

Each document chunk is converted into a vector representation.

The vectors are stored in ChromaDB.

---

# 🗄️ ChromaDB

The vector database is stored locally:

```text
chroma_db/
```

Collection:

```text
gym_rag
```

The retriever currently retrieves:

```text
Top K = 4
```

relevant document chunks for each query.

---

# 🔎 Retrieval

`src/retriever.py`

The retrieval flow is:

```text
User Question
      ↓
Query Embedding
      ↓
ChromaDB Search
      ↓
Top 4 Relevant Chunks
      ↓
Context
```

The retrieved chunks are then passed to the RAG generation layer.

---

# 🧠 RAG Generation

`src/rag.py`

The application uses:

```text
OpenAI
Model: gpt-4.1-mini
Temperature: 0
```

The LLM receives:

```text
User Question
+
Retrieved Context
```

The prompt instructs the model to answer using only the provided context.

If the required information is unavailable, the application responds:

```text
I could not find this information in the provided documents.
```

This provides a basic hallucination-control mechanism.

---

# 🛡️ Grounded Response Strategy

The application follows a grounded-answer approach.

The LLM is instructed:

```text
Answer the user's question using ONLY the provided context.

Do not invent information.
```

The system identifies unavailable information and marks the response:

```text
NOT_FOUND
```

This behavior is useful for RAG QA validation.

---

# 📊 Response Status

Every query receives a status.

## SUCCESS

The application generated an answer from the available context.

```text
SUCCESS
```

## NOT_FOUND

The requested information was not available in the provided documents.

```text
NOT_FOUND
```

## FAILED

An application/runtime error occurred.

```text
FAILED
```

---

# ⚡ Response Latency

The application measures RAG execution time using:

```python
time.perf_counter()
```

Example:

```text
Response Latency: 2.35 seconds
```

The latency is stored in Excel under:

```text
Latency Seconds
```

The dashboard uses these values to calculate:

```text
Average Response Time
```

---

# 📗 Excel Execution Logging

Every query is recorded in:

```text
output/rag_results.xlsx
```

The Excel log contains:

| Column          | Description                  |
| --------------- | ---------------------------- |
| Timestamp       | Query execution time         |
| User Input      | User question                |
| AI Output       | Generated answer             |
| Status          | SUCCESS / NOT_FOUND / FAILED |
| Source Files    | Retrieved source documents   |
| Categories      | Document categories          |
| Pages           | PDF page references          |
| Latency Seconds | Response latency             |

Example:

```text
User Input:
What exercises target the chest?

Status:
SUCCESS

Source Files:
exercise.txt

Categories:
exercise

Latency Seconds:
2.35
```

---

# 📈 Metrics Dashboard

`src/dashboard.py`

The application includes a QA-focused metrics dashboard.

The dashboard reads:

```text
output/rag_results.xlsx
```

and provides:

* Total Queries
* Successful Queries
* NOT_FOUND Queries
* Failed Queries
* Success Rate
* Average Response Time
* Response Status Distribution
* Source/Category Distribution
* Recent Queries
* Complete RAG Execution Log

---

# 🧪 RAG Debug Panel

The AI Assistant includes:

```text
🔍 RAG Debug Details
```

The panel displays:

```text
User Query
Response Status
Retrieved Chunks
Response Latency
LangSmith Project
```

It also exposes retrieved document information:

```text
Source
Category
Content Type
Page
Retrieved Content
```

This makes the application useful as a **RAG QA demonstration**, not just a chatbot.

---

# 🔬 LangSmith Observability

LangSmith tracing is enabled using:

```python
@traceable(name="Gym-RAG-Application")
```

Configuration:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=Gym-RAG-Demo
```

LangSmith can be used to investigate:

* RAG executions
* Retrieval behavior
* LLM calls
* Latency
* Failures
* Prompt execution
* Application debugging

---

# 🖥️ Streamlit Application

The main application is:

```text
mainapplication.py
```

Run:

```powershell
streamlit run mainapplication.py
```

The application contains two navigation options:

```text
🤖 AI Assistant
📊 Metrics Dashboard
```

---

# 🤖 AI Assistant

The AI Assistant provides:

* Question input
* Enter-key submission
* Ask AI button
* AI-generated answer
* Source information
* RAG debug details
* Response status
* Response latency
* Retrieved document chunks

---

# ⌨️ Enter-Key Support

The question input uses a Streamlit form:

```python
with st.form("rag_question_form"):
```

and:

```python
st.form_submit_button(
    "🔍 Ask AI",
    type="primary"
)
```

This allows users to:

```text
Type Question
      ↓
Press ENTER
      ↓
Submit Query
      ↓
Execute RAG
```

The user can also click:

```text
🔍 Ask AI
```

---

# 💾 Session State

The application uses Streamlit `st.session_state` to preserve the latest RAG result.

The result is stored after execution:

```python
st.session_state.result = result
```

This prevents the AI response from disappearing when Streamlit reruns the application.

The stored result contains:

```text
question
answer
documents
status
latency
retrieved_chunks
```

---

# 🔄 Navigation Behavior

The application supports:

```text
🤖 AI Assistant
        ↕
📊 Metrics Dashboard
```

When users switch between pages, Streamlit reruns the application.

The RAG result is stored in session state so that the latest AI response can remain available when returning to the AI Assistant.

---

# 🧪 QA Test Scenarios

## TC01 — Valid Exercise Query

Input:

```text
What exercises target the chest?
```

Expected:

```text
AI Answer
Sources
Retrieved Chunks
Latency
SUCCESS
```

Excel:

```text
Status = SUCCESS
```

---

## TC02 — Trainer Query

Input:

```text
Which trainers are available in the trainer directory?
```

Expected:

```text
Relevant trainer information
PDF source
Page information
```

---

## TC03 — Unsupported Query

Input:

```text
What is the gym membership fee?
```

Expected:

```text
⚠️ No such data is available in the provided documents.
```

Excel:

```text
Status = NOT_FOUND
```

---

## TC04 — Empty Query

Click:

```text
🔍 Ask AI
```

without entering a question.

Expected:

```text
Please enter a question.
```

---

## TC05 — Source Validation

Ask:

```text
What exercises target the chest?
```

Verify:

```text
Source File
Category
Page
Retrieved Content
```

match the knowledge base.

---

## TC06 — Latency Validation

Execute multiple queries.

Verify that:

```text
Latency Seconds
```

contains numeric values.

The dashboard should calculate the average response time.

---

## TC07 — Dashboard Validation

Execute several queries.

Navigate to:

```text
📊 Metrics Dashboard
```

Verify:

```text
Total Queries
Successful
NOT_FOUND
FAILED
Success Rate
Average Response Time
```

---

## TC08 — Navigation Persistence

1. Ask a question.
2. View the AI answer.
3. Open Metrics Dashboard.
4. Return to AI Assistant.

Expected:

```text
Previous AI response remains available.
```

---

# 🧪 QA Strategy

This project can be validated across multiple testing dimensions.

## Functional Testing

Validate:

* Document ingestion
* Chunking
* Metadata
* Embeddings
* Retrieval
* LLM response
* Source attribution
* Excel logging
* Dashboard calculations

## RAG Testing

Validate:

* Retrieval relevance
* Context accuracy
* Answer grounding
* Source correctness
* Metadata correctness
* NOT_FOUND behavior

## Negative Testing

Validate:

* Empty questions
* Irrelevant questions
* Unsupported questions
* Missing documents
* ChromaDB unavailable
* OpenAI API failures
* Excel file locked

## Performance Testing

Measure:

* Retrieval latency
* LLM latency
* End-to-end latency
* Average response time

## Observability Testing

Validate:

* LangSmith traces
* Excel logs
* Status tracking
* Retrieved chunk count
* Latency tracking

---

# 🛠️ Installation

## 1. Clone the Repository

```powershell
git clone <your-repository-url>
```

Navigate to the project:

```powershell
cd "Buildathon Gym App"
```

---

## 2. Create Virtual Environment

```powershell
python -m venv venv
```

---

## 3. Activate Environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 📦 Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
.env
```

Example:

```text
OPENAI_API_KEY=your_openai_api_key

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=Gym-RAG-Demo
```

Never commit real API keys to Git.

---

# 🗄️ Build the Vector Database

After adding or changing documents:

```powershell
python src/embeddings.py
```

The process is:

```text
Load
 ↓
Metadata
 ↓
Chunk
 ↓
Embed
 ↓
Store
```

The generated ChromaDB data is stored in:

```text
chroma_db/
```

---

# ▶️ Run the Application

From the project root:

```powershell
streamlit run mainapplication.py
```

---

# 📊 Reset Excel Metrics

During development, if the Excel schema changes, delete:

```text
output/rag_results.xlsx
```

Then restart the application and execute a new query.

The logger will recreate the workbook with the latest columns.

If Excel is open while the application tries to write to it, Windows may return:

```text
PermissionError: [Errno 13] Permission denied
```

Close the Excel workbook before running another query.

---

# 🔄 Rebuild ChromaDB

If the source documents are changed significantly:

1. Stop the Streamlit application.
2. Remove the existing:

```text
chroma_db/
```

3. Rebuild:

```powershell
python src/embeddings.py
```

4. Restart:

```powershell
streamlit run mainapplication.py
```

---

# 🐛 Troubleshooting

## Excel Permission Error

```text
PermissionError: [Errno 13] Permission denied
```

Solution:

* Close `rag_results.xlsx`.
* Restart the query.

---

## Cannot Convert List to Excel

```text
Cannot convert [] to Excel
```

Cause:

A Python list was passed directly to an Excel cell.

Solution:

Convert metadata collections into strings before writing to Excel.

---

## Latency List Error

```text
float() argument must be a string or a real number, not 'list'
```

Latency must be numeric:

```python
latency = 2.35
```

and not:

```python
latency = [2.35]
```

---

## Streamlit Width Warning

If Streamlit reports:

```text
For use_container_width=True, use width='stretch'.
```

Use:

```python
width="stretch"
```

instead of:

```python
use_container_width=True
```

For content-sized components:

```python
width="content"
```

---

## ModuleNotFoundError

Run Streamlit from the project root:

```powershell
cd "C:\Users\Balaji KT\Buildathon Gym App"
```

Then:

```powershell
streamlit run mainapplication.py
```

Use package imports:

```python
from src.rag import ask_question
```

---

# 🔒 Git Security

Recommended `.gitignore`:

```gitignore
__pycache__/
*.py[cod]

venv/
.venv/
env/

.env
.env.*
!.env.example

chroma_db/

output/
*.xlsx
*.xls

.streamlit/secrets.toml

.vscode/
.idea/

.DS_Store
Thumbs.db

*.log
.ipynb_checkpoints/
*.tmp
*.temp
```

Do not commit:

```text
.env
API keys
chroma_db/
output/rag_results.xlsx
venv/
```

---

# 📦 Technology Stack

| Layer                | Technology                    |
| -------------------- | ----------------------------- |
| Programming Language | Python                        |
| UI                   | Streamlit                     |
| RAG Framework        | LangChain                     |
| LLM                  | OpenAI GPT-4.1-mini           |
| Embeddings           | OpenAI text-embedding-3-small |
| Vector Database      | ChromaDB                      |
| PDF Processing       | PyPDF                         |
| Excel Logging        | OpenPyXL                      |
| Data Analysis        | Pandas                        |
| Observability        | LangSmith                     |
| Configuration        | python-dotenv                 |

---

# 🏆 GenAI + QA Capabilities Demonstrated

This project demonstrates a practical combination of:

## GenAI

* LLM integration
* Prompt engineering
* Embeddings
* Grounded generation

## RAG

* Document ingestion
* Chunking
* Metadata
* Vector search
* Context retrieval
* Source attribution

## QA

* Functional testing
* Negative testing
* RAG validation
* Source validation
* Performance measurement
* Observability
* Execution logging
* Metrics monitoring

## Engineering

* Python
* LangChain
* ChromaDB
* Streamlit
* Excel
* LangSmith
* Environment configuration
* Modular project structure

---

# 🚀 Future Enhancements

Potential next versions can include:

* 💬 Conversation history
* 🧠 Long-term memory
* 🏷️ Metadata filtering
* 🔎 Advanced trainer search
* 💪 Personalized exercise recommendations
* 🔐 Authentication
* 👥 Role-based access
* 🧪 Automated RAG evaluation
* 📏 Faithfulness scoring
* 🎯 Answer relevance scoring
* 📊 Retrieval precision/recall
* ⚡ Performance testing
* 🧪 Automated regression suite
* 🔌 FastAPI backend
* 🔄 CI/CD integration
* 🤖 Agentic AI workflows
* 👥 Multi-agent fitness assistant
* 🚦 Automated AI quality gates
* 📈 Advanced LangSmith evaluation

---

# 🎓 Portfolio / Buildathon Value

This project can be presented as an:

> **End-to-End GenAI RAG QA Application**

It demonstrates not only chatbot functionality but also:

```text
Data
 ↓
RAG
 ↓
LLM
 ↓
Observability
 ↓
QA Validation
 ↓
Performance Metrics
 ↓
Execution Logging
 ↓
Dashboard
```

This makes the project suitable for demonstrating practical skills in:

* GenAI
* RAG
* AI Quality Engineering
* Automation Testing
* LLM Testing
* AI Observability
* Performance Engineering
* QA Leadership

---

# 👨‍💻 Author

**Balaji Thiyagarajan**

QA Lead / QA Manager

Focus Areas:

```text
GenAI
Agentic AI
RAG
AI Quality Engineering
Automation Testing
Performance Testing
API Testing
Selenium
Python
```

---

# 📄 License

This project is intended for educational, demonstration, buildathon, and portfolio purposes.
