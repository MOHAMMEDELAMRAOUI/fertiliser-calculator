import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'postgres'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'admin'),
        port=os.getenv('DB_PORT', '5432'),
        cursor_factory=RealDictCursor
    )
    return conn

def load_ingredients_from_json():
    with open('ingredients.json', 'r') as f:
        return json.load(f)

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Suppression des tables existantes
        cur.execute("DROP TABLE IF EXISTS formulation_ingredients")
        cur.execute("DROP TABLE IF EXISTS formulations")
        cur.execute("DROP TABLE IF EXISTS ingredients")

        # Création des tables
        cur.execute("""
        CREATE TABLE ingredients (
            id SERIAL PRIMARY KEY,
            code VARCHAR(10) UNIQUE,
            name VARCHAR(100) NOT NULL,
            nitrogen_percent DECIMAL(5,2) DEFAULT 0.0,
            phosphorus_percent DECIMAL(5,2) DEFAULT 0.0,
            potassium_percent DECIMAL(5,2) DEFAULT 0.0,
            sulfur_percent DECIMAL(5,2) DEFAULT 0.0,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
        """)

        cur.execute("""
        CREATE TABLE formulations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            target_nitrogen DECIMAL(5,2),
            target_phosphorus DECIMAL(5,2),
            target_potassium DECIMAL(5,2),
            target_sulfur DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT NOW(),
            user_id INTEGER
        )
        """)

        cur.execute("""
        CREATE TABLE formulation_ingredients (
            formulation_id INTEGER REFERENCES formulations(id),
            ingredient_id INTEGER REFERENCES ingredients(id),
            percentage DECIMAL(5,2) NOT NULL,
            PRIMARY KEY (formulation_id, ingredient_id)
        )
        """)

        # Insertion des données depuis le JSON
        ingredients = load_ingredients_from_json()
        for ing in ingredients:
            cur.execute("""
            INSERT INTO ingredients 
            (code, name, nitrogen_percent, phosphorus_percent, 
             potassium_percent, sulfur_percent, is_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (code) DO UPDATE SET
                name = EXCLUDED.name,
                nitrogen_percent = EXCLUDED.nitrogen_percent,
                phosphorus_percent = EXCLUDED.phosphorus_percent,
                potassium_percent = EXCLUDED.potassium_percent,
                sulfur_percent = EXCLUDED.sulfur_percent,
                is_available = EXCLUDED.is_available,
                updated_at = NOW()
            """, (
                ing['code'],
                ing['name'],
                ing['nitrogen_percent'],
                ing['phosphorus_percent'],
                ing['potassium_percent'],
                ing['sulfur_percent'],
                ing.get('is_available', True)
            ))

        conn.commit()
        print(f"Successfully initialized database with {len(ingredients)} ingredients")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database initialization failed: {str(e)}")
        raise
    finally:
        if conn:
            if cur:
                cur.close()
            conn.close()