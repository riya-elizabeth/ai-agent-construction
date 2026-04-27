from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.rag_pipeline import RAGPipeline

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app = FastAPI(title="Construction Safety AI Agent")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please wait a moment before trying again."}
    )

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
@limiter.limit("10/minute")
def ask_question(request: QuestionRequest, req: Request):
    # Input validation
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if len(request.question) > 500:
        raise HTTPException(status_code=400, detail="Question must be under 500 characters")

    result = pipeline.ask(request.question)
    return result