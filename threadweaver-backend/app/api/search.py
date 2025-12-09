from fastapi import APIRouter, HTTPException, UploadFile, File

from app.db.supabase_client import get_supabase_connection
from app.schemas.requests import SearchResponse, SearchResult
from config import config
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["search"])

supabase_client = get_supabase_connection()

@router.post("/search")
async def search(query: str, match_threshold: float = 0.5, top_k: int = 5) -> SearchResponse:
    """
    Search the database for documents
    """
    logger.info(f"Searching for documents: {query}")
    
    try:
        # Embed the user query
        user_query_embedding = embed_user_query(query)
        logger.info(f"User query embedded successfully: {user_query_embedding}")

        # Search the database for documents
        search_results = search_chunks(user_query_embedding, match_threshold, top_k)
        logger.info(f"Search results: {search_results}")

        return SearchResponse(
            results=[SearchResult(
                chunk_text=result["original_text"],
                chunk_index=result["chunk_index"],
                similarity_score=0.0,
                document_title=result["document_id"]
            ) for result in search_results.data]
        )
    except Exception as e:
        logger.error(f"Error searching for documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def embed_user_query(query: str) -> list[float]:
    """
    Embed the user query
    """
    return config.get_embedding_model().embed_query(query)

def search_chunks(user_query_embedding: list[float], match_threshold: float = 0.5, top_k: int = 5) -> list[SearchResponse]:
    """
    Search the database for chunks
    """
    try:
        # Search the database for chunks
        search_results = supabase_client.rpc("match_documents", {
            "query_embedding": user_query_embedding,
            "match_threshold": match_threshold,
            "match_count": top_k
        }).execute()
        logger.info(f"Search results: {search_results}")
        return search_results
    except Exception as e:
        logger.error(f"Error searching for chunks: {e}")
        raise HTTPException(status_code=500, detail=str(e))