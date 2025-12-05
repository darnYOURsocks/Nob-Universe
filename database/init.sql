CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

INSERT INTO patterns (name, description)
VALUES
    ('Recognition', 'Detects input patterns.'),
    ('Integration', 'Combines signals harmonically.'),
    ('Propagation', 'Broadcasts coherent patterns.')
ON CONFLICT DO NOTHING;
