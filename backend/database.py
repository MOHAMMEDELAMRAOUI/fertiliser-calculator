import os
import psycopg2
from psycopg2.extras import RealDictCursor

PGHOST = os.getenv('PGHOST', 'localhost')
PGPORT = int(os.getenv('PGPORT', '5432'))
PGUSER = os.getenv('PGUSER', 'postgres')
PGPASSWORD = os.getenv('PGPASSWORD', 'admin')
PGDATABASE = os.getenv('PGDATABASE', 'postgres')


def get_db_connection():
    return psycopg2.connect(
        host=PGHOST,
        port=PGPORT,
        user=PGUSER,
        password=PGPASSWORD,
        dbname=PGDATABASE,
        cursor_factory=RealDictCursor,
    )


def init_db():
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ingredients (
            id SERIAL PRIMARY KEY,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            nitrogen_percent NUMERIC NOT NULL CHECK (nitrogen_percent >= 0 AND nitrogen_percent <= 100),
            phosphorus_percent NUMERIC NOT NULL CHECK (phosphorus_percent >= 0 AND phosphorus_percent <= 100),
            potassium_percent NUMERIC NOT NULL CHECK (potassium_percent >= 0 AND potassium_percent <= 100),
            sulfur_percent NUMERIC NOT NULL CHECK (sulfur_percent >= 0 AND sulfur_percent <= 100),
            is_available BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    conn.commit(); cur.close(); conn.close()
