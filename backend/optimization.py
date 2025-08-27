import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from collections import defaultdict
from database import get_db_connection
from psycopg2.extras import RealDictCursor
import numpy as np

# --- Récupération des ingrédients depuis la base ---
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
            for k in ('nitrogen', 'phosphorus', 'potassium', 'sulfur'):
                ing[k] = float(ing[k] or 0)
        return ingredients
    finally:
        cur.close()
        conn.close()

# --- Calcul de la formulation ---
def calculate_formulation(target, available_ingredients):
    ingredients_data = get_ingredients_from_db(available_ingredients)
    if not ingredients_data:
        raise ValueError("Aucun ingrédient trouvé")

    n_ing = len(ingredients_data)
    nutrients = ['n','p2o5','k2o','s']

    # --- Définition du modèle Pyomo ---
    model = pyo.ConcreteModel()
    model.I = pyo.RangeSet(0, n_ing-1)

    # Variables : pourcentages des ingrédients
    model.x = pyo.Var(model.I, domain=pyo.NonNegativeReals)

    # Contraintes : somme = 100%
    model.sum_constraint = pyo.Constraint(expr=sum(model.x[i] for i in model.I) == 100)

    # Fonction objectif : somme des carrés des écarts
    def obj_rule(m):
        error = 0.0
        for nutrient in nutrients:
            target_value = target.get(nutrient, 0.0)
            contribution = sum(model.x[i] * ingredients_data[i][
                'nitrogen' if nutrient=='n' else
                'phosphorus' if nutrient=='p2o5' else
                'potassium' if nutrient=='k2o' else
                'sulfur'
            ] / 100.0 for i in model.I)
            error += (contribution - target_value)**2
        return error
    model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

    # --- Résolution avec IPOPT ---
    opt = SolverFactory('ipopt')
    opt.options['tol'] = 1e-12
    opt.options['max_iter'] = 5000
    results = opt.solve(model, tee=False)

    if (results.solver.status != pyo.SolverStatus.ok) or (results.solver.termination_condition != pyo.TerminationCondition.optimal):
        raise RuntimeError(f"Échec de l'optimisation: {results.solver.termination_condition}")

    # --- Récupérer les résultats ---
    x_values = np.array([pyo.value(model.x[i]) for i in model.I])

    # Arrondir et normaliser comme Excel
    x_values = np.round(x_values, 2)
    x_values *= 100 / x_values.sum()

    # Construire le résultat final
    output = {
        'ingredients': [],
        'total_contribution': defaultdict(float),
        'target': target,
        'solver_status': str(results.solver.termination_condition)
    }

    for i, ing in enumerate(ingredients_data):
        pct = x_values[i]
        contrib = {
            'n': round(pct * ing['nitrogen'] / 100.0, 2),
            'p2o5': round(pct * ing['phosphorus'] / 100.0, 2),
            'k2o': round(pct * ing['potassium'] / 100.0, 2),
            's': round(pct * ing['sulfur'] / 100.0, 2),
        }
        output['ingredients'].append({
            'id': ing['id'],
            'code': ing['code'],
            'percentage': pct,
            'contribution': contrib
        })
        for k, v in contrib.items():
            output['total_contribution'][k] += v

    output['total_contribution'] = dict(output['total_contribution'])
    output['variance'] = {
        k: round(output['total_contribution'].get(k,0.0) - float(target.get(k,0.0)),2)
        for k in nutrients
    }

    return output
