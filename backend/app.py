from flask import Flask, jsonify, request
from database import get_db_connection, init_db
import click
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

@app.cli.command("init-db")
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized!")

# GET /api/ingredients - Liste tous les ingrédients
@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT id, code, name, 
                   nitrogen_percent, phosphorus_percent, 
                   potassium_percent, sulfur_percent,
                   is_available
            FROM ingredients
            ORDER BY name
        """)
        ingredients = cur.fetchall()
        return jsonify(ingredients)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# POST /api/ingredients - Crée un nouvel ingrédient
@app.route('/api/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    
    required_fields = ['code', 'name', 'nitrogen_percent', 
                      'phosphorus_percent', 'potassium_percent', 'sulfur_percent']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO ingredients 
            (code, name, nitrogen_percent, phosphorus_percent, 
             potassium_percent, sulfur_percent)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, code, name
        """, (
            data['code'],
            data['name'],
            float(data['nitrogen_percent']),
            float(data['phosphorus_percent']),
            float(data['potassium_percent']),
            float(data['sulfur_percent'])
        ))
        
        new_ingredient = cur.fetchone()
        conn.commit()
        return jsonify(new_ingredient), 201
    
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# PUT /api/ingredients/<int:id> - Met à jour un ingrédient
@app.route('/api/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE ingredients
            SET code = %s,
                name = %s,
                nitrogen_percent = %s,
                phosphorus_percent = %s,
                potassium_percent = %s,
                sulfur_percent = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING *
        """, (
            data.get('code'),
            data.get('name'),
            float(data.get('nitrogen_percent')),
            float(data.get('phosphorus_percent')),
            float(data.get('potassium_percent')),
            float(data.get('sulfur_percent')),
            datetime.utcnow(),
            id
        ))
        
        updated = cur.fetchone()
        if not updated:
            return jsonify({"error": "Ingredient not found"}), 404
            
        conn.commit()
        return jsonify(updated)
    
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# PATCH /api/ingredients/<int:id>/availability - Toggle disponibilité
@app.route('/api/ingredients/<int:id>/availability', methods=['PATCH'])
def toggle_availability(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Récupère le statut actuel
        cur.execute("SELECT is_available FROM ingredients WHERE id = %s", (id,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({"error": "Ingredient not found"}), 404
        
        new_status = not result['is_available']
        
        # Met à jour
        cur.execute("""
            UPDATE ingredients
            SET is_available = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING id, code, name, is_available
        """, (new_status, datetime.utcnow(), id))
        
        updated = cur.fetchone()
        conn.commit()
        return jsonify(updated)
    
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)