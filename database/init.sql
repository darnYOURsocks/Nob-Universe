-- Initialize Nob-Universe database
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO patterns (name, description)
VALUES
    ('Spiral', 'A classic logarithmic spiral pattern.'),
    ('Grid', 'Aligned rectangular grid useful for experiments.'),
    ('Wave', 'Sine wave-based spatial variation.');
