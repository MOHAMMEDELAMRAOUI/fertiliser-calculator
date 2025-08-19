import json
import psycopg2
from psycopg2.extras import execute_values

# 🔹 Connexion à ta base
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="admin"
)
cur = conn.cursor()

# 🔹 Charger ton fichier JSON
with open("ingredients.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔹 Préparer les colonnes
cols = (
    "code", "name", "nitrogen_percent", "phosphorus_percent",
    "potassium_percent", "sulfur_percent", "is_available", "page_id"
)

# 🔹 Convertir les données en tuples
values = [
    (
        ing["code"], ing["name"], ing["nitrogen_percent"], ing["phosphorus_percent"],
        ing["potassium_percent"], ing["sulfur_percent"], ing["is_available"], ing["page_id"]
    )
    for ing in data
]

# 🔹 Insérer dans PostgreSQL
query = """
    INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id)
    VALUES %s
    ON CONFLICT (code, page_id) DO UPDATE
    SET name = EXCLUDED.name,
        nitrogen_percent = EXCLUDED.nitrogen_percent,
        phosphorus_percent = EXCLUDED.phosphorus_percent,
        potassium_percent = EXCLUDED.potassium_percent,
        sulfur_percent = EXCLUDED.sulfur_percent,
        is_available = EXCLUDED.is_available,
        updated_at = NOW()
"""


execute_values(cur, query, values)
conn.commit()

print("✅ Import terminé avec succès")

cur.close()
conn.close()
