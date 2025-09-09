-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

/*
-- Create a sample table for storing vector embeddings
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index for vector similarity search
CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Insert some sample data
INSERT INTO documents (title, content, embedding) VALUES 
('Sample Document 1', 'This is a sample document for testing vector search capabilities.', '[0.1, 0.2, 0.3, 0.4, 0.5]'::vector),
('Sample Document 2', 'Another sample document with different content for testing.', '[0.6, 0.7, 0.8, 0.9, 1.0]'::vector);

-- Create a function for vector similarity search
CREATE OR REPLACE FUNCTION search_similar_documents(
    query_embedding VECTOR(5),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 10
)
RETURNS TABLE (
    id INT,
    title TEXT,
    content TEXT,
    similarity FLOAT
)
LANGUAGE SQL
AS $$
    SELECT 
        documents.id,
        documents.title,
        documents.content,
        1 - (documents.embedding <=> query_embedding) AS similarity
    FROM documents
    WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
    ORDER BY documents.embedding <=> query_embedding
    LIMIT match_count;
$$;

-- Grant permissions to the app user
GRANT ALL PRIVILEGES ON DATABASE appdb TO app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app; */
