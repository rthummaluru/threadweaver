from fastapi import APIRouter, HTTPException, UploadFile, File

from app.db.supabase_client import get_supabase_connection
from app.schemas.requests import SearchResponse, SearchResult
from app.services.rag_service import RAGService
from config import config
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["search"])

supabase_client = get_supabase_connection()

@router.post("/search")
def search(query: str) -> SearchResponse:
    """
    Search the database for documents
    """
    logger.info(f"Searching for documents: {query}")
    rag_service = RAGService()
    try:
        search_results = rag_service.search(query=query)
        return search_results
    except Exception as e:
        logger.error(f"Error searching for documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
