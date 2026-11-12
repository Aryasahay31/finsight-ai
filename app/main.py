"""FinSight AI - FastAPI Backend"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.agents.orchestrator import run_analysis
from app.memory.store import memory

os.makedirs("./charts", exist_ok=True)
os.makedirs("./data/chromadb", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 50)
    print("  FinSight AI - Multi-Agent Financial Analyst")
    print(f"  Past analyses in memory: {memory.get_analysis_count()}")
    print("=" * 50)
    yield
    print("FinSight AI shutting down.")


app = FastAPI(
    title="FinSight AI",
    description="Multi-Agent Financial Analysis Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/charts", StaticFiles(directory="charts"), name="charts")


@app.get("/")
def root():
    return {
        "app": "FinSight AI",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Run analysis for a company",
            "GET /history": "Past analyses from memory",
            "GET /health": "Health check",
        },
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "analyses_in_memory": memory.get_analysis_count()}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_company(request: AnalysisRequest):
    company = request.company.strip()
    if not company:
        raise HTTPException(status_code=400, detail="Company name is required")
    if len(company) > 100:
        raise HTTPException(status_code=400, detail="Company name too long")

    try:
        result = run_analysis(company)

        if result.get("report") and not result["report"].startswith("Error"):
            memory.store_analysis(
                company=company,
                ticker=result.get("ticker", ""),
                report=result.get("report", ""),
                evaluation=result.get("evaluation", {}),
            )

        return AnalysisResponse(
            company=company,
            ticker=result.get("ticker", ""),
            report=result.get("report", ""),
            evaluation=result.get("evaluation", {}),
            chart_paths=result.get("chart_paths", []),
            agent_logs=result.get("agent_logs", []),
            errors=result.get("errors", []),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/history")
def get_history():
    count = memory.get_analysis_count()
    if count == 0:
        return {"total": 0, "analyses": []}
    recent = memory.recall_past_analysis("financial analysis")
    return {"total": count, "analyses": recent}