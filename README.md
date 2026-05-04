# Construction Safety AI Agent — RAG Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Claude API](https://img.shields.io/badge/Anthropic_Claude_API-CC785C?style=flat&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-6E40C9?style=flat)
![Status](https://img.shields.io/badge/Phase_4-Complete-brightgreen)

> **An agentic AI assistant that answers construction safety and OSHA compliance questions in real time — grounded entirely in verified source documents.**

---

## Results

| Metric | Value |
|---|---|
| **Question coverage** | **84% (63 / 75 questions answered)** |
| **Hallucination rate** | **0.0%** |
| **Avg correctness** | **2.92 / 3.0** |
| Fully correct answers (score 3) | 94.3% of answered questions |
| Confidence threshold | 0.55 (below = routed to fallback) |
| Knowledge base | 288 chunks from 3 OSHA documents |
| Unanswered questions | 12 — confirmed knowledge gaps, logged for review |

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
| Evaluation | Custom 75-question ground truth pipeline + LLM-as-judge scoring |
| Language | Python 3.10 |

---

## Knowledge Base

The agent's knowledge is grounded in three verified OSHA documents:
- **Cal/OSHA Pocket Guide for the Construction Industry** (2022 Edition)
- **OSHA Construction Safety Manual**
- **OSHA Trenching & Excavation Safety Guide**

Chunked into **288 segments** using page/section-based splitting optimised for this corpus. No outside knowledge is used — the agent is explicitly prohibited from answering beyond its source documents.

**Chunking analysis:** Three strategies were tested (288 page-based chunks, 1,101 chunks at 500 chars, 497 chunks at 1,200 chars). The original page/section-based chunking at ~1,880 char avg achieved 84% coverage vs 24% and 13% for the algorithmic alternatives — larger semantically coherent chunks produce stronger embeddings for dense regulatory text.

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

## Evaluation

### Coverage
Run the 75-question evaluation pipeline:
```bash
python evaluate_quick.py
# Compare collections: python evaluate_quick.py --collection construction_procedures_v2
```

### Hallucination Scoring
LLM-as-judge scoring using Claude on correctness (0–3), completeness (0–3), and hallucination (yes/no):
```bash
python evaluation/score_hallucination.py
```

Results are saved to `evaluation/eval_results.csv`.

### Final Metrics (Phase 4)

| Metric | Result |
|---|---|
| Coverage | 84% (63/75) |
| Hallucination rate | **0.0%** |
| Avg correctness | **2.92 / 3.0** |
| Correctness = 3 | 50/53 answered questions (94.3%) |
| Correctness ≤ 1 | 1/53 (1.9%) |
| Unanswered (knowledge gaps) | 12 questions across 3 topic areas |

---

## Known Limitations

The 16% unanswered rate (12 questions) represents confirmed **knowledge gaps** — content not present in any of the 3 source documents. They fall into three patterns:

- **Heat illness specifics** — water quantity requirements, written prevention plan details
- **California excavation rules** — permit requirements, atmospheric testing, support system details
- **Operational procedures** — toolbox talk format, PPE program components, mobile equipment checks

These questions are intentionally left unanswered rather than risk hallucination. See [`model_limitations.md`](model_limitations.md) for the full gap analysis.

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
│   ├── evaluate.py            # Full 75-question evaluation pipeline
│   ├── score_hallucination.py # LLM-as-judge hallucination scoring
│   ├── eval_results.csv       # Full evaluation results with scores
│   ├── ground_truth.csv       # 75-question ground truth Q&A set
│   └── unanswered_questions.csv  # Flagged knowledge gaps
├── frontend/
│   └── app.py                 # Streamlit chat UI
├── data/
│   └── procedures/            # Source OSHA PDFs
├── model_limitations.md       # Known gaps and roadmap
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

**3. Run the FastAPI backend**
```bash
uvicorn api.main:app --reload
```

**4. Run the Streamlit frontend**
```bash
streamlit run frontend/app.py
```

---

## Context

Built as part of the **Ampytics Practicum** — an applied AI project for a construction industry client. The agent is designed to be deployed on job sites where workers need immediate, reliable access to OSHA safety guidance.

---

*Part of my MSBA AI/ML Portfolio · [GitHub](https://github.com/riya-elizabeth)*
