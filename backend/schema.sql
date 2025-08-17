CREATE TABLE IF NOT EXISTS ingredients (
  id SERIAL PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  nitrogen_percent NUMERIC NOT NULL CHECK (nitrogen_percent BETWEEN 0 AND 100),
  phosphorus_percent NUMERIC NOT NULL CHECK (phosphorus_percent BETWEEN 0 AND 100),
  potassium_percent NUMERIC NOT NULL CHECK (potassium_percent BETWEEN 0 AND 100),
  sulfur_percent NUMERIC NOT NULL CHECK (sulfur_percent BETWEEN 0 AND 100),
  is_available BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);