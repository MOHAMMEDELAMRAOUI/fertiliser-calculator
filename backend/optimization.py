from scipy.optimize import minimize
import numpy as np
from collections import defaultdict
from database import get_db_connection
from psycopg2.extras import RealDictCursor

def get_ingredients_from_db(ingredient_ids):
    if not ingredient_ids:
        return []
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        placeholders = ','.join(['%s'] * len(ingredient_ids))
        cur.execute(f"""
            SELECT
                id, code,
                nitrogen_percent as nitrogen,
                phosphorus_percent as phosphorus,
                potassium_percent as potassium,
                sulfur_percent as sulfur
            FROM ingredients
            WHERE id IN ({placeholders})
        """, tuple(ingredient_ids))
        ingredients = cur.fetchall() or []
        for ing in ingredients:
            # cast to float for safety
            for k in ('nitrogen','phosphorus','potassium','sulfur'):
                ing[k] = float(ing[k] or 0)
        return ingredients
    finally:
        cur.close(); conn.close()

def calculate_formulation(target, available_ingredients):
    """
    Calcule la formulation optimale d'engrais.
    target: dict with keys in ['n','p2o5','k2o','s'] as percentages
    available_ingredients: list of ingredient IDs
    """
    ingredients_data = get_ingredients_from_db(available_ingredients)
    if not ingredients_data:
        raise ValueError("Aucun ingrédient disponible trouvé")

    nutrient_vectors = {
        'n': np.array([ing['nitrogen'] for ing in ingredients_data], dtype=float),
        'p2o5': np.array([ing['phosphorus'] for ing in ingredients_data], dtype=float),
        'k2o': np.array([ing['potassium'] for ing in ingredients_data], dtype=float),
        's': np.array([ing['sulfur'] for ing in ingredients_data], dtype=float),
    }

   

    def objective(x):
        error = 0.0
        for nutrient, target_value in target.items():
            if nutrient in nutrient_vectors:
                contribution = float(np.dot(x, nutrient_vectors[nutrient]) / 100.0)
                error += (contribution - float(target_value)) ** 2
        return error

    constraints = (
        { 'type': 'eq', 'fun': lambda x: np.sum(x) - 100.0 },  # sum to 100%
        { 'type': 'ineq', 'fun': lambda x: np.min(x) }          # all >= 0
    )

    bounds = [(0.0, 100.0) for _ in ingredients_data]
    x0 = np.array([100.0/len(ingredients_data)] * len(ingredients_data), dtype=float)

    solution = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'maxiter': 1000, 'ftol': 1e-6}
    )

    if not solution.success:
        raise RuntimeError(f"Échec de l'optimisation: {solution.message}")

    results = {
        'ingredients': [],
        'total_contribution': defaultdict(float),
        'target': target,
        'solver_status': solution.message,
    }

    for i, ing in enumerate(ingredients_data):
        pct = round(float(solution.x[i]), 2)
        if pct > 0.01:
            contrib = {
                'n': round(pct * ing['nitrogen'] / 100.0, 2),
                'p2o5': round(pct * ing['phosphorus'] / 100.0, 2),
                'k2o': round(pct * ing['potassium'] / 100.0, 2),
                's': round(pct * ing['sulfur'] / 100.0, 2),
            }
            results['ingredients'].append({
                'id': ing['id'],
                'code': ing['code'],
                'percentage': pct,
                'contribution': contrib,
            })
            for k, v in contrib.items():
                results['total_contribution'][k] += v

    results['total_contribution'] = dict(results['total_contribution'])
    results['variance'] = {
        k: round(results['total_contribution'].get(k, 0.0) - float(target.get(k, 0.0)), 2)
        for k in ('n','p2o5','k2o','s')
    }
    return results