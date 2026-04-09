HT Lektion 8 — Multi-Agent Research System
A multi-agent research assistant built with LangChain, LangGraph, OpenAI, and hybrid RAG.
The system plans research, gathers evidence from the local knowledge base and the web, critiques its own draft, and asks for human approval before saving the final report.

✨ Features
Supervisor-based orchestration
Specialized agents:
Planner — creates a structured research plan
Researcher — collects and synthesizes evidence
Critic — evaluates quality and requests revisions if needed
Hybrid RAG pipeline:
FAISS semantic search
BM25 lexical search
CrossEncoder reranking
Human-in-the-Loop (HITL) before save_report
Structured outputs with Pydantic:
ResearchPlan
CritiqueResult
Safety limits:
max revise cycles
graph recursion limit
LLM timeout / retries
URL validation for external reads
Windows-safe FAISS fallback for OneDrive / non-ASCII paths
🧠 Architecture
🔄 How it works
The user enters a research request in the CLI.
The Supervisor delegates planning to the Planner.
The Researcher uses:
web_search
read_url
knowledge_search
The Critic checks whether the result is:
fresh enough
complete enough
well structured
If needed, the system loops through another revision.
Before saving, the user must explicitly choose:
approve
edit
reject
If the revise limit is reached, the system can still produce a best-effort draft with a disclaimer.

🗂️ Project structure
🧩 Agent responsibilities
Agent	Role	Output
Planner	Builds the research plan	ResearchPlan
Researcher	Gathers and synthesizes evidence	draft findings
Critic	Evaluates quality and requests revisions	CritiqueResult
Supervisor	Controls flow and tool calls	final decision path
🛠️ Tech stack
Layer	Tools
LLM orchestration	langchain, langgraph
Model	ChatOpenAI
Structured output	pydantic
Retrieval	FAISS, rank_bm25
Reranking	sentence-transformers (CrossEncoder)
Web tools	ddgs, trafilatura
PDF/document loading	pypdf
⚙️ Setup
1) Install dependencies
2) Create .env
Copy .env.example to .env and set your API key:

Useful defaults already included:

critique_max_rounds=2
graph_recursion_limit=25
llm_timeout_sec=90
url_fetch_timeout_sec=10
3) Build the local knowledge index
4) Run the system
💬 CLI behavior
At startup, the app:

checks whether the knowledge index exists
runs ingestion if needed
warms up the RAG retriever
starts a REPL session
Supported commands:

exit / quit — leave the app
/ingest — rebuild the index
Before saving a report, the system pauses and asks:

🧪 Example request
Expected flow:

Planner creates a plan
Researcher gathers evidence
Critic evaluates the draft
if approved, the system asks for human confirmation
report is saved to output/
🔒 Reliability and safety
The system includes several protections:

hard revise limit via critique_max_rounds
graph recursion limit
LLM timeout and retry limits
safe URL validation
HITL approval before file save
fallback handling if structured critique output is imperfect
🪟 Windows note
On Windows, especially with OneDrive or folders containing Cyrillic / non-ASCII characters, FAISS may fail to write index.faiss.

To avoid this, the project automatically relocates the FAISS binary index to a safe path under LOCALAPPDATA when needed.

📌 Educational goal
This project demonstrates:

multi-agent orchestration
agent-as-tool design
structured outputs
Evaluator–Optimizer loop
RAG + web augmentation
Human-in-the-Loop approval flow
If you want, I can next prepare a shorter portfolio-style version or an English README for public GitHub.