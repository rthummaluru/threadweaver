 -- Description: Add support for RAG with contextual retrieval and hybrid search

  -- Enable pgvector extension
  CREATE EXTENSION IF NOT EXISTS vector;

  -- Add 'upload' to integration_type enum
  ALTER TYPE integration_type ADD VALUE IF NOT EXISTS 'upload';

  -- Add 'text' to content_type enum  
  ALTER TYPE content_type ADD VALUE IF NOT EXISTS 'text';

  -- Update documents table for uploads
  ALTER TABLE documents
    ALTER COLUMN integration_id DROP NOT NULL,
    ALTER COLUMN external_id DROP NOT NULL,
    ADD COLUMN IF NOT EXISTS original_filename text,
    ADD COLUMN IF NOT EXISTS file_size_bytes bigint,
    ADD COLUMN IF NOT EXISTS mime_type text;

  -- Add constraint to enforce business logic
  ALTER TABLE documents
    DROP CONSTRAINT IF EXISTS check_integration_requirements,
    ADD CONSTRAINT check_integration_requirements CHECK (
      CASE
        WHEN integration_type IN ('slack', 'notion', 'whatsapp')
          THEN integration_id IS NOT NULL AND external_id IS NOT NULL
        WHEN integration_type = 'upload'
          THEN integration_id IS NULL AND external_id IS NULL
        ELSE false
      END
    );

  -- Update chunks table for RAG
  ALTER TABLE chunks
    ADD COLUMN IF NOT EXISTS original_text text,
    ADD COLUMN IF NOT EXISTS contextualized_text text,
    ADD COLUMN IF NOT EXISTS ts_vector tsvector;

  -- Ensure embedding column exists with correct dimensions
  -- (Check first, add if missing)
  DO $$
  BEGIN
    IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_name = 'chunks' AND column_name = 'embedding'
    ) THEN
      ALTER TABLE chunks ADD COLUMN embedding vector(1536);
    END IF;
  END $$;

  -- Create indexes for hybrid search
  CREATE INDEX IF NOT EXISTS chunks_bm25_idx
    ON chunks USING GIN(ts_vector);

  CREATE INDEX IF NOT EXISTS chunks_vector_idx
    ON chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

  -- Auto-update ts_vector trigger
  CREATE OR REPLACE FUNCTION chunks_tsvector_trigger() RETURNS trigger AS $$
  BEGIN
    NEW.ts_vector := to_tsvector('english', COALESCE(NEW.original_text, ''));
    RETURN NEW;
  END
  $$ LANGUAGE plpgsql;

  DROP TRIGGER IF EXISTS tsvectorupdate ON chunks;
  CREATE TRIGGER tsvectorupdate
    BEFORE INSERT OR UPDATE ON chunks
    FOR EACH ROW EXECUTE FUNCTION chunks_tsvector_trigger();