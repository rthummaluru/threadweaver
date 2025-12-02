from fastapi import APIRouter, HTTPException, UploadFile, File

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.db.supabase_client import get_supabase_connection
from config import config
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["documents"])

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> str:
    """
    Upload a document to the database and process it for RAG

    Args:
        file: The file to upload

    Returns:
        str: A success message

    Raises:
        HTTPException: If the file is not a text file or if there is an error uploading the document
        Exception: If there is an error chunking the document
    """
    logger.info(f"Uploading document: {file.filename}")
    supabase_client = get_supabase_connection()
    try:
        # Upload the file to the database
        if not file.filename.endswith(('.txt')):
            raise HTTPException(status_code=400, detail="Only text files are supported")
        
        # Read the file content
        file_content = await file.read()
        text_content = file_content.decode("utf-8")

        chunked_content = chunk_document(text_content)

        # Insert the document into the database TODO: fix insert params
        response = supabase_client.table("documents").insert({
            "user_id":"7b3866ad-1ffd-49c5-94c4-4b11d11d9cb8",  # Hardcoded for now
            "original_filename": file.filename,
            "mime_type": file.content_type,
            "file_size_bytes": file.size,
            "integration_type": "upload",
            "integration_id": None,
            "external_id": None,
        }).execute()
        logger.info(f"Document uploaded successfully: {response}")
        return "Document uploaded successfully"
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def chunk_document(file_content: str) -> list[str]:
    """
    Chunk the document into smaller pieces

    Args:
        file_content: The content of the file

    Returns:
        list[str]: A list of chunks

    Raises:
        Exception: If there is an error chunking the document
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100,
        )
        chunks = text_splitter.split_text(file_content)

        logger.info(f"Document chunked successfully: {chunks}")
        return chunks
    except Exception as e:
        logger.error(f"Error chunking document: {e}")
        raise Exception(f"Error chunking document: {e}")


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Embed the chunks

    Args:
        chunks: The chunks to embed

    Returns:
        list[list[float]]: A list of embeddings
    """
    try:
        embeddings = config.get_embedding_model().embed_documents(chunks)
        logger.info(f"Chunks embedded successfully: Generated {len(embeddings)} embeddings of size {len(embeddings[0])}")
        return embeddings
    except Exception as e:
        logger.error(f"Error embedding chunks: {e}")
        raise Exception(f"Error embedding chunks: {e}")