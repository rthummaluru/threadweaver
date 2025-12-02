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
        chunked_content = await chunk_document(file_content)

        # Insert the document into the database TODO: fix insert params
        response = supabase_client.table("documents").insert({
            "filename": file.filename,
            "file_path": file.filename,
            "file_type": file.content_type,
            "file_size": file.size,
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
            chunk_size=100,
            chunk_overlap=10,
        )
        chunks_document = text_splitter.create_documents([file_content])
        chunk_text = text_splitter.split_documents(chunks_document)

        logger.info(f"Document chunked successfully: {chunk_text}")
        return chunk_text
    except Exception as e:
        logger.error(f"Error chunking document: {e}")
        raise Exception(f"Error chunking document: {e}")
