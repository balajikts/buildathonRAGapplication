# 🏋️ Infinity Fitness Gym AI Assistant

A **Retrieval-Augmented Generation (RAG) based AI Assistant** built using Python, LangChain, OpenAI, ChromaDB, LangSmith, Excel, and Streamlit.

The application allows users to ask natural-language questions about:

* 🏋️ Exercise information
* 👨‍🏫 Trainer information
* 💳 Gym membership plans

The system retrieves relevant information from the gym's knowledge sources and generates **grounded responses using only the retrieved context**.

---

## 🚀 Project Objective

Build a practical **GenAI + RAG + QA demonstration application** that can:

1. Load heterogeneous knowledge sources.
2. Add metadata to documents.
3. Split documents into meaningful chunks.
4. Generate vector embeddings.
5. Store embeddings in ChromaDB.
6. Retrieve relevant information based on user questions.
7. Generate grounded answers using an LLM.
8. Trace RAG execution using LangSmith.
9. Log every query and response into Excel.
10. Display QA and performance metrics through a Streamlit dashboard.

---

# 🏗️ Architecture

```text
                    USER
                      │
                      ▼
              Streamlit Application
                      │
                      ▼
                User Question
                      │
                      ▼
              RAG Application
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Retriever                 OpenAI LLM
          │                       │
          ▼                       │
      ChromaDB                    │
          │                       │
          ▼                       │
   Relevant Chunks ───────────────┘
          │
          ▼
     Grounded Answer
          │
      ┌───┴───────────────┐
      ▼                   ▼
   Excel Log          LangSmith Trace
      │
      ▼
 Metrics Dashboard
```

---

# 📚 Knowledge Sources

The application currently uses three knowledge sources.

```text
data/
├── exercise.txt
├── gym_membership.txt
└── trainer_directory_30_pages.pdf
```

## 1. Exercise Manual

**File:**

```text
data/exercise.txt
```

Contains exercise-related information organized around different muscle groups and exercises.

Metadata:

```text
source_type       = TXT
document_category = exercise
content_type      = exercise_information
```

---

## 2. Gym Membership Plans

**File:**

```text
data/gym_membership.txt
```

Current membership information:

```text
INFINITY FITNESS GYM - MEMBERSHIP PLANS

Registration Fee: ₹500

Membership Plans:

1 Month: ₹2,500
3 Months: ₹5,000
6 Months: ₹7,000
12 Months: ₹12,000
```

Metadata:

```text
source_type       = TXT
document_category = membership
content_type      = membership_information
```

Example questions:

```text
What is the membership fee for 1 month?

How much does a 6 month membership cost?

What is the registration fee?

How much is the annual membership?

What membership plans are available?
```

---

## 3. Trainer Directory

**File:**

```text
data/trainer_directory_30_pages.pdf
```

The PDF contains trainer information including:

* Trainer ID
* Trainer name
* Primary specialization
* Certifications
* Experience
* Location

Metadata:

```text
source_type       = PDF
document_category = trainer_directory
content_type      = trainer_information
page_number      = PDF page number
```

Example questions:

```text
Who are the bodybuilding trainers?

Find trainers with NASM certification.

Which trainers are located in Boston?

Who has experience in yoga?

Find a trainer specializing in marathon preparation.
```

---

# 📁 Project Structure

```text
Buildathon Gym App/
│
├── mainapplication.py
├── README.md
├── .gitignore
├── .env
├── requirements.txt
│
├── data/
│   ├── exercise.txt
│   ├── gym_membership.txt
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

# 🔄 RAG Pipeline

## Step 1 — Document Loading

`load_documents.py` dynamically loads all TXT and PDF files from the `data` directory.

```text
TXT → TextLoader
PDF → PyPDFLoader
```

The loader automatically detects:

```text
*.txt
*.pdf
```

This means additional TXT/PDF knowledge sources can be added without modifying the loader.

---

# 🏷️ Step 2 — Metadata Enrichment

`metadata.py` assigns metadata based on the source file.

Example:

```text
exercise.txt
    ↓
document_category = exercise

gym_membership.txt
    ↓
document_category = membership

trainer_directory_30_pages.pdf
    ↓
document_category = trainer_directory
```

Metadata helps with:

* Source identification
* Debugging
* Retrieval analysis
* Excel reporting
* Future metadata filtering

---

# ✂️ Step 3 — Document Chunking

`chunk_documents.py` uses:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

Current configuration:

| Parameter     |                          Value |
| ------------- | -----------------------------: |
| Chunk Size    |                            500 |
| Chunk Overlap |                             50 |
| Splitter      | RecursiveCharacterTextSplitter |

The metadata is preserved when documents are converted into chunks.

---

# 🧠 Step 4 — Embeddings

The project uses OpenAI embeddings:

```text
text-embedding-3-small
```

Each document chunk is converted into a vector representation.

---

# 🗄️ Step 5 — ChromaDB

The embeddings are stored locally in:

```text
chroma_db/
```

Collection:

```text
gym_rag
```

ChromaDB provides vector similarity search for retrieving relevant chunks.

---

# 🔍 Step 6 — Retrieval

The retriever uses ChromaDB and retrieves the top 4 relevant chunks.

```python
vectorstore.as_retriever(
    search_kwargs={"k": 4}
)
```

The user's question is converted into an embedding and compared against stored document vectors.

---

# 🤖 Step 7 — LLM Response Generation

The application uses:

```text
gpt-4.1-mini
```

with:

```text
temperature = 0
```

The RAG prompt instructs the model to:

* Use only the retrieved context.
* Avoid inventing information.
* Return a predefined message when the information is unavailable.

Fallback response:

```text
I could not find this information in the provided documents.
```

---

# 🛡️ Grounded AI Response

The application follows a grounded-generation approach.

```text
User Question
      ↓
Retriever
      ↓
Relevant Documents
      ↓
Context
      ↓
LLM
      ↓
Grounded Answer
```

The model is instructed not to generate unsupported information.

---

# 📊 Response Status

Every RAG execution receives a status.

### SUCCESS

Information was successfully retrieved and an answer was generated.

### NOT_FOUND

The requested information was not available in the retrieved context.

### FAILED

An unexpected application or processing error occurred.

---

# ⚡ Latency Tracking

The RAG execution measures response time using Python's performance timer.

Example:

```text
Latency Seconds
---------------
1.82
2.14
1.67
```

Latency is stored in Excel and displayed on the dashboard.

---

# 📗 Excel Logging

Every RAG execution is logged to:

```text
output/rag_results.xlsx
```

Columns:

| Column          | Description                  |
| --------------- | ---------------------------- |
| Timestamp       | Query execution time         |
| User Input      | User question                |
| AI Output       | Generated answer             |
| Status          | SUCCESS / NOT_FOUND / FAILED |
| Source Files    | Retrieved source files       |
| Categories      | Document categories          |
| Pages           | Retrieved PDF pages          |
| Latency Seconds | RAG response time            |

Example:

```text
Timestamp
User Input
AI Output
Status
Source Files
Categories
Pages
Latency Seconds
```

---

# 📊 RAG QA Dashboard

The Streamlit dashboard provides visibility into RAG execution quality.

Metrics include:

```text
Total Queries
Successful Queries
Not Found
Failed Queries
Success Rate
Average Response Time
```

Additional visualizations:

* Response status distribution
* Source/category distribution
* Recent queries
* Complete RAG execution log

---

# 🧪 QA / Debug Panel

The application includes a debug section displaying:

```text
User Query
Status
Retrieved Chunks
Latency
LangSmith Project
Retrieved Documents
```

This is useful for validating the RAG pipeline during development and QA.

---

# 🔬 LangSmith Integration

LangSmith tracing is enabled for RAG execution monitoring.

Environment configuration:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=Gym-RAG-Demo
```

LangSmith can be used to analyze:

* RAG execution
* Retriever behavior
* LLM calls
* Latency
* Errors
* Debugging information

---

# 🖥️ Streamlit Application

The application is launched using:

```powershell
streamlit run mainapplication.py
```

The UI provides two primary sections:

```text
🤖 AI Assistant
📊 Metrics Dashboard
```

---

# ⌨️ User Interaction

The AI Assistant supports:

* Question input
* Ask AI button
* Enter-key submission
* Latest-answer persistence
* Retrieved-source visibility
* Status display
* Latency display

Example:

```text
User:
What is the membership fee for 1 month?

AI:
The 1-month membership fee is ₹2,500.
The registration fee is ₹500.
```

---

# 🔄 Rebuilding the Vector Database

Whenever a knowledge source is:

* Added
* Deleted
* Modified
* Corrected

the ChromaDB should be rebuilt.

### Delete existing database

PowerShell:

```powershell
Remove-Item -Recurse -Force .\chroma_db
```

### Rebuild

```powershell
python -m src.embeddings
```

Expected output:

```text
Loading TXT: exercise.txt
Loading TXT: gym_membership.txt
Loading PDF: trainer_directory_30_pages.pdf

TXT documents loaded : 2
PDF pages loaded     : 31
Total documents      : 33

Adding metadata...
Creating chunks...
Creating embeddings...
Creating Chroma vector database...

Vector database created successfully!
```

---

# 🔎 RAG Retrieval Verification

Before testing through Streamlit, retrieval can be tested directly.

```powershell
python -c "from src.retriever import create_retriever; r=create_retriever(); docs=r.invoke('What is the membership fee for 1 month?'); [print(d.metadata, d.page_content) for d in docs]"
```

This helps determine whether the problem is in:

```text
Document Loading
       ↓
Chunking
       ↓
Embedding
       ↓
ChromaDB
       ↓
Retriever
       ↓
LLM
       ↓
Streamlit
```

---

# 🧪 QA Test Scenarios

## Membership Tests

| Test                                 | Expected Result           |
| ------------------------------------ | ------------------------- |
| What is the registration fee?        | ₹500                      |
| What is the 1 month fee?             | ₹2,500                    |
| What is the 3 month fee?             | ₹5,000                    |
| What is the 6 month fee?             | ₹7,000                    |
| What is the 12 month fee?            | ₹12,000                   |
| What membership plans are available? | All four plans            |
| What is the price of a 2-year plan?  | Information not available |

---

## Trainer Tests

Examples:

```text
Find bodybuilding trainers.

Find trainers in Boston.

Who specializes in yoga?

Find a trainer with NASM certification.
```

---

## Exercise Tests

Examples:

```text
Give me exercises for chest.

What exercises target the back?

What exercises target the shoulders?
```

---

## Negative / Hallucination Tests

Ask questions that are not present in the knowledge base.

Example:

```text
What is the gym's cancellation policy?
```

Expected:

```text
I could not find this information in the provided documents.
```

This validates the application's grounding behavior.

---

# ⚙️ Installation

## 1. Clone the repository

```powershell
git clone <your-github-repository>
cd "Buildathon Gym App"
```

---

## 2. Create virtual environment

```powershell
python -m venv venv
```

---

## 3. Activate virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 📦 Install Dependencies

```powershell
pip install -r requirements.txt
```

Major dependencies:

```text
langchain
langchain-community
langchain-openai
langchain-chroma
langchain-text-splitters
pypdf
python-dotenv
openpyxl
pandas
langsmith
tiktoken
streamlit
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

**Never commit real API keys to GitHub.**

Add `.env` to `.gitignore`.

---

# ▶️ Running the Application

## Build Vector Database

```powershell
python -m src.embeddings
```

## Start Streamlit

```powershell
streamlit run mainapplication.py
```

---

# 🐛 Troubleshooting

## Membership information returns "No data found"

Check the following:

### 1. Verify file exists

```powershell
Get-ChildItem .\data
```

You should see:

```text
exercise.txt
gym_membership.txt
trainer_directory_30_pages.pdf
```

### 2. Verify membership content

```powershell
Get-Content .\data\gym_membership.txt
```

### 3. Verify metadata

```powershell
python -m src.metadata
```

Expected:

```text
Source File       : gym_membership.txt
Category          : membership
Content Type      : membership_information
```

### 4. Rebuild ChromaDB

```powershell
Remove-Item -Recurse -Force .\chroma_db
python -m src.embeddings
```

### 5. Test retrieval

```powershell
python -c "from src.retriever import create_retriever; r=create_retriever(); docs=r.invoke('What is the membership fee for 1 month?'); [print(d.metadata, d.page_content) for d in docs]"
```

---

# ⚠️ Encoding Issue

If PowerShell displays:

```text
â‚¹
```

instead of:

```text
₹
```

the file has an encoding/display mismatch.

The membership amounts themselves can still be represented correctly, but the file should ideally be saved as **UTF-8**.

In VS Code:

```text
File
 → Save with Encoding
 → UTF-8
```

Then rebuild ChromaDB.

---

# 🔒 Git Security

Never commit:

```text
.env
```

or API keys.

Recommended `.gitignore`:

```text
venv/
.env
__pycache__/
*.pyc
chroma_db/
output/
.streamlit/
```

---

# 🧰 Technology Stack

| Technology | Purpose                       |
| ---------- | ----------------------------- |
| Python     | Application development       |
| LangChain  | RAG orchestration             |
| OpenAI     | Embeddings + LLM              |
| ChromaDB   | Vector database               |
| PyPDF      | PDF document processing       |
| LangSmith  | AI tracing and observability  |
| OpenPyXL   | Excel logging                 |
| Pandas     | Metrics processing            |
| Streamlit  | Web application and dashboard |
| Git/GitHub | Version control               |

---

# 🤖 GenAI Capabilities

This project demonstrates:

* Retrieval-Augmented Generation
* Vector embeddings
* Semantic search
* LLM-based answer generation
* Grounded responses
* Hallucination prevention
* Metadata enrichment
* Multi-source knowledge retrieval
* AI observability
* RAG performance monitoring

---

# 🧪 QA Capabilities

This project also demonstrates practical GenAI QA concepts:

* Functional testing
* Negative testing
* Retrieval validation
* Hallucination testing
* Source verification
* Metadata validation
* Response-status validation
* Latency measurement
* Error handling
* Regression validation
* RAG pipeline debugging
* Excel-based execution logging
* Dashboard-based quality monitoring

---

# 🚀 Future Enhancements

Potential improvements:

### 1. Metadata Filtering

Allow queries such as:

```text
Search only membership information.
```

or:

```text
Search only trainer information.
```

### 2. Hybrid Search

Combine:

```text
Vector Search
+
Keyword Search
```

for improved retrieval accuracy.

### 3. Reranking

Add a reranking layer after vector retrieval to improve relevance.

### 4. Conversation Memory

Allow users to ask follow-up questions while maintaining conversation context.

### 5. Authentication

Add role-based access for:

```text
Admin
Trainer
Member
Support
```

### 6. Advanced QA Metrics

Add:

```text
Retrieval Accuracy
Answer Relevance
Faithfulness
Context Precision
Context Recall
```

### 7. Automated RAG Evaluation

Create an evaluation dataset containing:

```text
Question
Expected Answer
Retrieved Context
Actual Answer
Evaluation Score
```

### 8. Agentic AI

Extend the application into an agent that can:

```text
Understand Goal
      ↓
Plan
      ↓
Retrieve Information
      ↓
Use Tools
      ↓
Validate Result
      ↓
Respond
```

---

# 🎯 Project Outcome

The Infinity Fitness Gym AI Assistant demonstrates a complete practical GenAI pipeline:

```text
Heterogeneous Documents
        ↓
Document Loading
        ↓
Metadata Enrichment
        ↓
Chunking
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Semantic Retrieval
        ↓
LLM
        ↓
Grounded Response
        ↓
Excel Logging
        ↓
QA Dashboard
        ↓
LangSmith Observability
```

This makes the project suitable as a **GenAI / RAG / Agentic AI QA portfolio and buildathon project**.

---

# 👨‍💻 Author

**Balaji Thiyagarajan**

QA Lead / QA Manager
GenAI & Agentic AI QA
RAG | LLM | Selenium | Python | API | Performance Testing

---

# 📄 License

This project is intended for educational, demonstration, portfolio, and buildathon purposes.
