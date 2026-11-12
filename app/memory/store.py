"""FinSight AI - Memory Store (ChromaDB)"""

import json
from datetime import datetime

import chromadb
from chromadb.config import Settings

from app.config import settings


class MemoryStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="analysis_history",
            metadata={"description": "Past financial analyses"},
        )

    def store_analysis(self, company: str, ticker: str, report: str, evaluation: dict):
        """Store a completed analysis in memory."""
        doc_id = f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.collection.add(
            documents=[report],
            metadatas=[{
                "company": company,
                "ticker": ticker,
                "date": datetime.now().isoformat(),
                "overall_score": str(evaluation.get("overall", "N/A")),
            }],
            ids=[doc_id],
        )

    def recall_past_analysis(self, company: str, limit: int = 3) -> list[dict]:
        """Retrieve past analyses for a company."""
        try:
            results = self.collection.query(
                query_texts=[f"{company} financial analysis"],
                n_results=limit,
            )
            if not results["documents"][0]:
                return []

            past = []
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i]
                past.append({
                    "company": meta.get("company", ""),
                    "ticker": meta.get("ticker", ""),
                    "date": meta.get("date", ""),
                    "score": meta.get("overall_score", ""),
                    "report_preview": doc[:300] + "...",
                })
            return past
        except Exception:
            return []

    def get_analysis_count(self) -> int:
        return self.collection.count()


memory = MemoryStore()