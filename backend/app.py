from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from psycopg2.extras import RealDictCursor

from database import get_db_connection, init_db
from optimization import calculate_formulation

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

# ------------------- CLI -------------------
import click
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database schema."""
    init_db()
    click.echo("Database initialized!")

# ------------------- Helpers -------------------

def _json_error(msg, code=400):
    return jsonify({"error": str(msg)}), code

# ------------------- Routes -------------------

# GET /api/ingredients - Liste tous les ingrédients
@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    page_id = request.args.get('page_id', default=1, type=int)
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            """
            SELECT id, code, name,
                   nitrogen_percent, phosphorus_percent,
                   potassium_percent, sulfur_percent,
                   is_available, created_at, updated_at
            FROM ingredients 
            WHERE page_id = %s
            ORDER BY name
            """,
            (page_id, )
        )
        rows = cur.fetchall()
        return jsonify(rows)
    except Exception as e:
        return _json_error(e, 500)
    finally:
        cur.close(); conn.close()

# POST /api/ingredients - Crée un nouvel ingrédient
@app.route('/api/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json() or {}
    required = ['code','name','nitrogen_percent','phosphorus_percent','potassium_percent','sulfur_percent', 'page_id']
    if not all(k in data for k in required):
        return _json_error("Missing required fields", 400)

    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            """
            INSERT INTO ingredients (code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, page_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, page_id , is_available
            """,
            (
                data['code'], data['name'],
                float(data['nitrogen_percent']), float(data['phosphorus_percent']),
                float(data['potassium_percent']), float(data['sulfur_percent']),
                data.get('page_id', 1) 
            )
        )
        row = cur.fetchone(); conn.commit()
        return jsonify(row), 201
    except Exception as e:
        conn.rollback(); return _json_error(e, 400)
    finally:
        cur.close(); conn.close()

# PUT /api/ingredients/<id> - Met à jour un ingrédient
@app.route('/api/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id:int):
    data = request.get_json() or {}
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            """
            UPDATE ingredients
            SET code = %s, name = %s,
                nitrogen_percent = %s,
                phosphorus_percent = %s,
                potassium_percent = %s,
                sulfur_percent = %s,
                page_id = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id, code, name, nitrogen_percent, phosphorus_percent, potassium_percent, sulfur_percent, is_available, page_id , updated_at
            """,
            (
                data.get('code'), data.get('name'),
                float(data.get('nitrogen_percent')), float(data.get('phosphorus_percent')),
                float(data.get('potassium_percent')), float(data.get('sulfur_percent')),
                int(data['page_id']),
                datetime.utcnow(), id
            )
        )
        row = cur.fetchone()
        if not row:
            return _json_error("Ingredient not found", 404)
        conn.commit(); return jsonify(row)
    except Exception as e:
        conn.rollback(); return _json_error(e, 400)
    finally:
        cur.close(); conn.close()

# PATCH /api/ingredients/<id>/availability - Toggle disponibilité
@app.route('/api/ingredients/<int:id>/availability', methods=['PATCH'])
def toggle_availability(id:int):
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT is_available FROM ingredients WHERE id = %s", (id,))
        current = cur.fetchone()
        if not current:
            return _json_error("Ingredient not found", 404)
        new_status = not current['is_available']
        cur.execute(
            """
            UPDATE ingredients
            SET is_available = %s, updated_at = %s
            WHERE id = %s
            RETURNING id, code, name, is_available, page_id , updated_at
            """,
            (new_status, datetime.utcnow(), id)
        )
        row = cur.fetchone(); conn.commit(); return jsonify(row)
    except Exception as e:
        conn.rollback(); return _json_error(e, 400)
    finally:
        cur.close(); conn.close()

# POST /api/calculate - calcul formulation
@app.route('/api/calculate', methods=['POST'])
def calculate_formulation_endpoint():
    try:
        data = request.get_json() or {}
        if 'target' not in data or 'available_ingredients' not in data:
            return _json_error("Invalid request format", 400)

        target = {k.lower(): float(v) for k, v in data['target'].items()}
        result = calculate_formulation(target=target, available_ingredients=data['available_ingredients'])
        return jsonify(result)
    except ValueError as e:
        return _json_error(e, 400)
    except Exception as e:
        print(f"Calculation error: {e}")
        return _json_error("Internal server error", 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


