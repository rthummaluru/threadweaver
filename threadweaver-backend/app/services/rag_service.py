import logging
import time as t
from config import config

from app.db.supabase_client import get_supabase_connection

from app.schemas.requests import SearchResponse, SearchResult

logger = logging.getLogger(__name__)

supabase_client = get_supabase_connection()

class RAGService:
    """
    RAG service class
    """
    def __init__(self):
        """
        Initialize the RAG service
        """
        self.supabase_client = supabase_client

    
    def _embed_user_query(self, query: str) -> list[float]:
        """
        Embed the user query
        """
        return config.get_embedding_model().embed_query(query)

    def _search_chunks(self, user_query_embedding: list[float], match_threshold: float = 0.5, top_k: int = 5):
        """
        Search the database for chunks
        """
        try:
            # Search the database for chunks
            search_results = self.supabase_client.rpc("match_documents", {
                "query_embedding": user_query_embedding,
                "match_threshold": match_threshold,
                "match_count": top_k
            }).execute()
            return search_results
        except Exception as e:
            logger.error(f"Error searching for chunks: {e}")
            raise Exception(f"Error searching for chunks: {e}")
    

    def search(self, query: str, match_threshold: float = 0.2, top_k: int = 5) -> SearchResponse:
        """
        Search the database for documents
        """
        logger.info(f"Searching for documents: {query}")
        
        try:
            # Embed the user query
            user_query_embedding = self._embed_user_query(query)
            logger.info(f"User query embedded successfully: {len(user_query_embedding)}")

            # Search the database for documents
            search_results = self._search_chunks(user_query_embedding, match_threshold, top_k)

            return SearchResponse(
                results=[SearchResult(
                    chunk_text=result["original_text"],
                    chunk_index=result["chunk_index"],
                    similarity_score=0.0,
                    document_id=result["document_id"]
                ) for result in search_results.data]
            )
        except Exception as e:
            logger.error(f"Error searching for documents: {e}")
            raise Exception(f"Error searching for documents: {e}")