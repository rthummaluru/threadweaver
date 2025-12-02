import asyncio
import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.api.documents import chunk_document, embed_chunks
from app.db.supabase_client import get_supabase_connection


from config import config
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_chunk_document_success():
    """
    Test the chunk_document function
    """
    # ARRANGE
    test_file = Path("test_data/sample_doc.txt")
    test_content = test_file.read_text()

    # ACT
    chunks = chunk_document(test_content)

    # ASSERT
    assert len(chunks) > 0


@pytest.mark.asyncio
async def test_embed_chunks_success():
    """
    Test the embed_chunks function
    """
    # ARRANGE
    chunks = ["The Chronicle of the Starlit Forest", "Chapter 1 — The Vanishing Village"]
    # ACT
    embeddings = embed_chunks(chunks)
    # ASSERT
    assert len(embeddings) > 0
    assert len(embeddings[0]) == 1536

@pytest.mark.asyncio
async def test_embed_chunks_failure():
    """
    Test the embed_chunks function with invalid chunks
    """
    # ARRANGE
    chunks = []
    # ACT
    with pytest.raises(Exception):
        embeddings = embed_chunks(chunks)
    # ASSERT
    assert embeddings is None