-- Match documents using cosine distance (<=>)
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns setof chunks
language sql
as $$
  select *,
  -- Calculate cosine distance as similarity score
  -- 1 - (chunks.embedding <=> query_embedding) as similarity_score,
  from chunks
  where chunks.embedding <=> query_embedding < 1 - match_threshold
  order by chunks.embedding <=> query_embedding asc
  limit least(match_count, 200);
$$;