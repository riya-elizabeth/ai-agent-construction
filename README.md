# Construction Safety AI Agent — RAG Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Claude API](https://img.shields.io/badge/Anthropic_Claude_API-CC785C?style=flat&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-6E40C9?style=flat)
![Status](https://img.shields.io/badge/Phase_3-Complete-brightgreen)

> **An agentic AI assistant that answers construction safety and OSHA compliance questions in real time — grounded entirely in verified source documents.**

---

## Results

| Metric | Value |
|---|---|
| Question coverage | **84% (63 / 75 questions answered)** |
| Confidence threshold | 0.55 (below = routed to fallback) |
| Knowledge base | 288 chunks from 2 OSHA documents |
| Unanswered questions | Automatically logged for team lead review |
| Hallucination control | Source-grounded only — no outside knowledge used |

---

## Problem Statement

Construction workers on job sites need fast, accurate answers to safety and OSHA compliance questions — often in high-pressure situations where consulting a manual or waiting for a supervisor is not practical.

**This project builds a RAG (Retrieval-Augmented Generation) AI agent** that:
- Answers safety questions grounded exclusively in Cal/OSHA and OSHA source documents
- Cites the specific regulation or section number in every answer
- Flags unanswered questions for human review instead of hallucinating
- Adds automatic safety disclaimers for critical topics (falls, electrical, confined spaces, heat)

---

## Architecture

```
User Question
     │
     ▼
FastAPI Backend (/ask endpoint)
     │   ├── Input validation & rate limiting
     │
     ▼
RAG Pipeline
     │   ├── Query → ChromaDB vector store
     │   ├── Retrieve top-k chunks (similarity scored)
     │   ├── Confidence threshold check (≥ 0.55 to answer)
     │
     ▼
Claude API (Anthropic)
     │   ├── System prompt: OSHA safety assistant rules
     │   ├── Context: retrieved document chunks
     │   └── Answer with regulation citations
     │
     ▼
Response → User
     └── If unanswered: logged to CSV for team lead review
```

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Anthropic Claude API |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Backend | FastAPI |
| Frontend | Streamlit |
| Evaluation | Custom 75-question ground truth pipeline |
| Language | Python 3.10 |

---

## Knowledge Base

The agent's knowledge is grounded in two verified OSHA documents:
- **Cal/OSHA Pocket Guide for the Construction Industry** (2022 Edition)
- **OSHA Construction Safety Manual**

Chunked into **288 segments** with overlap to preserve context across section boundaries. No outside knowledge is used — the agent is explicitly prohibited from answering beyond its source documents.

---

## Key Features

**Source-grounded answers only**
Every response cites the specific regulation number or section. If the answer isn't in the documents, the agent says so — it does not hallucinate.

**Confidence thresholding**
Retrieval similarity scores below 0.55 are routed to a fallback response. Borderline retrievals do not produce low-confidence answers.

**Automatic fallback logging**
Unanswered questions are automatically logged to `evaluation/unanswered_questions.csv` for team lead review — building a feedback loop for future knowledge base expansion.

**Safety-critical disclaimers**
Questions about fall protection, electrical hazards, confined spaces, and heat illness automatically append: *"⚠️ Safety-critical topic: When in doubt, stop work and consult a qualified supervisor."*

**Rate limiting & input validation**
The FastAPI backend includes per-minute rate limiting and input sanitization to protect against misuse.

---

## Project Structure

```
ai-agent-construction/
├── agent/
│   ├── ingest.py              # Document chunking & ChromaDB ingestion
│   ├── rag_pipeline.py        # Core RAG logic — retrieval + Claude API call
│   └── system_prompt.txt      # Agent rules and behavior constraints
├── api/
│   └── main.py                # FastAPI backend — /ask endpoint
├── evaluation/
│   ├── evaluate.py            # Automated 75-question evaluation pipeline
│   ├── eval_results.csv       # Full evaluation results
│   └── unanswered_questions.csv  # Flagged gaps for review
├── docs/
│   ├── technical_guide.md     # Setup and architecture documentation
│   ├── model_limitations.md   # Known gaps and Phase 4 roadmap
│   ├── retrospective.md       # Project retrospective
│   └── risk_cba_report.md     # Risk and cost-benefit analysis
├── frontend/                  # Streamlit UI
├── .env.example               # Environment variable template
└── README.md
```

---

## Setup

**1. Clone the repo and install dependencies**
```bash
git clone https://github.com/riya-elizabeth/ai-agent-construction.git
cd ai-agent-construction
pip install -r requirements.txt
```

**2. Set up environment variables**
```bash
cp .env.example .env
# Add your Anthropic API key to .env
```

**3. Ingest documents into ChromaDB**
```bash
python agent/ingest.py
```

**4. Run the FastAPI backend**
```bash
uvicorn api.main:app --reload
```

**5. Run the Streamlit frontend**
```bash
streamlit run frontend/app.py
```

---

## Evaluation

Run the full 75-question evaluation pipeline:
```bash
python evaluate_quick.py
```

Results are saved to `evaluation/eval_results.csv`. Unanswered questions are logged to `evaluation/unanswered_questions.csv` for review.

---

## Known Limitations & Roadmap

See [`docs/model_limitations.md`](docs/model_limitations.md) for the full documented gap analysis.

Key items on the Phase 4 roadmap:
- Expand knowledge base to close the 16% coverage gap (heat illness, excavation topics)
- Add conversation memory for follow-up question handling
- Formal hallucination rate scoring (target: < 5%)
- Increase chunk overlap from 800 → 1000 characters for better boundary handling

---

## Context

Built as part of the **Ampytics Practicum** — an applied AI project for a construction industry client. The agent is designed to be deployed on job sites where workers need immediate, reliable access to OSHA safety guidance.

---

*Part of my MSBA AI/ML Portfolio · [GitHub](https://github.com/riya-elizabeth)*
