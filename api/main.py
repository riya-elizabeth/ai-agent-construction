from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.rag_pipeline import RAGPipeline

app = FastAPI(title="Construction Safety AI Agent")

# Load pipeline once at startup
pipeline = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    response: str
    sources: list
    answered: bool


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Construction Safety Agent is running"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = pipeline.ask(request.question)
    return result
