import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import run_research_pipeline
from dotenv import load_dotenv

load_dotenv()

# Map Gemini_API_KEY to GOOGLE_API_KEY for LangChain if necessary
if "Gemini_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["Gemini_API_KEY"]

app = FastAPI(
    title="Multi-Agent RAG System API",
    description="REST API for the multi-agent research pipeline.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
def home():
    return {"status": "online", "docs": "/docs"}

@app.post("/research")
def research(request: ResearchRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic is empty")
    try:
        return run_research_pipeline(request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
