from fastapi import APIRouter, HTTPException, UploadFile, File

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.db.supabase_client import get_supabase_connection
from app.schemas.requests import DocumentUploadResponse
from config import config
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["documents"])


@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
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

         # Insert the document into the database
        response = supabase_client.table("documents").insert({
            "user_id":"7b3866ad-1ffd-49c5-94c4-4b11d11d9cb8",  # Hardcoded for now
            "original_filename": file.filename,
            "mime_type": file.content_type,
            "file_size_bytes": file.size,
            "integration_type": "upload",
            "integration_id": None,
            "external_id": None,
            "content_type": "file",
            "title": file.filename
        }).execute()

        document_id = response.data[0]["id"]

        # Chunk and embed the content
        chunked_content = _chunk_document(text_content)
        embedded_content = _embed_chunks(chunked_content)

        # Insert the chunks into the database
        chunk_records = []
        for i ,(chunk, embedding) in enumerate(zip(chunked_content, embedded_content)):
            chunk_records.append({
                "document_id": document_id,
                "user_id":"7b3866ad-1ffd-49c5-94c4-4b11d11d9cb8",  # Hardcoded for now
                "integration_type": "upload",
                "chunk_index": i,
                "original_text": chunk,
                "embedding": embedding,
            })
            logger.info(f"Chunk {i} uploaded successfully")

        response = supabase_client.table("chunks").insert(chunk_records).execute()
        logger.info(f"Stored {len(chunk_records)} chunks in database")
    
        # Return the document and chunks
        return DocumentUploadResponse(
            message="Document and chunks uploaded successfully",
            document_id=document_id,
            chunks_created=len(chunk_records)
        )
    # Possible failure points:
    # - Error chunking the document
    # - Error embedding the chunks
    # - Error inserting the chunks into the database
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=503, detail="Unable to upload document. Please try again later.")

def _chunk_document(file_content: str) -> list[str]:
    """
    Chunk the document into smaller pieces

    Args:
        file_content: The content of the file

    Returns:
        list[str]: A list of chunks

    Raises:
        ValueError: If the file content is empty
    """

    if not file_content:
        raise ValueError("File content is empty")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )
    chunks = text_splitter.split_text(file_content)

    logger.info(f"Document chunked successfully: {chunks}")
    return chunks


def _embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Embed the chunks

    Args:
        chunks: The chunks to embed

    Returns:
        list[list[float]]: A list of embeddings
    """
    if not chunks:
        raise ValueError("Chunks are empty")

    embeddings = config.get_embedding_model().embed_documents(chunks)
    logger.info(f"Chunks embedded successfully: Generated {len(embeddings)} embeddings of size {len(embeddings[0])}")
    return embeddings