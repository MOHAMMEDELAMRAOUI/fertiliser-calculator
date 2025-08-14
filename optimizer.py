import pandas as pd
from scipy.optimize import minimize

def optimize_fertilizer_blend(ingredients_df, target_n, target_p2o5, target_k2o, target_s, active_ingredients):
    """
    Optimise le mélange d'engrais pour atteindre les objectifs de composition.

    Args:
        ingredients_df (pd.DataFrame): DataFrame avec les colonnes 'N', 'P2O5', 'K2O', 'S' pour chaque ingrédient.
        target_n (float): Objectif de N en pourcentage.
        target_p2o5 (float): Objectif de P2O5 en pourcentage.
        target_k2o (float): Objectif de K2O en pourcentage.
        target_s (float): Objectif de S en pourcentage.
        active_ingredients (list): Liste des indices des ingrédients actifs (On/Off).

    Returns:
        dict: Résultats de l'optimisation, incluant les quantités optimales, la composition obtenue et l'écart.
    """

    num_ingredients = len(ingredients_df)

    # Conditions initiales (quantités égales pour les ingrédients actifs, 0 pour les inactifs)
    x0 = [1.0 if i in active_ingredients else 0.0 for i in range(num_ingredients)]

    # Bornes pour les variables (quantités >= 0)
    bounds = [(0, None) for _ in range(num_ingredients)]

    # Contraintes d'activation (si inactif, quantité = 0)
    constraints = []
    for i in range(num_ingredients):
        if i not in active_ingredients:
            constraints.append({'type': 'eq', 'fun': lambda x, i=i: x[i]})

    def objective(x):
        total_mass = sum(x)
        if total_mass == 0:
            return float('inf') # Éviter la division par zéro

        actual_n = sum(x[i] * ingredients_df.loc[i, 'N'] for i in range(num_ingredients)) / total_mass
        actual_p2o5 = sum(x[i] * ingredients_df.loc[i, 'P2O5'] for i in range(num_ingredients)) / total_mass
        actual_k2o = sum(x[i] * ingredients_df.loc[i, 'K2O'] for i in range(num_ingredients)) / total_mass
        actual_s = sum(x[i] * ingredients_df.loc[i, 'S'] for i in range(num_ingredients)) / total_mass

        # Fonction objectif: minimiser l'écart quadratique par rapport aux objectifs
        return (
            (actual_n - target_n)**2 +
            (actual_p2o5 - target_p2o5)**2 +
            (actual_k2o - target_k2o)**2 +
            (actual_s - target_s)**2
        )

    # Exécuter l'optimisation
    result = minimize(objective, x0, bounds=bounds, constraints=constraints, method='SLSQP')

    # Calculer les résultats finaux
    optimal_quantities = result.x.tolist()
    total_optimal_mass = sum(optimal_quantities)

    if total_optimal_mass == 0:
        final_n, final_p2o5, final_k2o, final_s = 0, 0, 0, 0
    else:
        final_n = sum(optimal_quantities[i] * ingredients_df.loc[i, 'N'] for i in range(num_ingredients)) / total_optimal_mass
        final_p2o5 = sum(optimal_quantities[i] * ingredients_df.loc[i, 'P2O5'] for i in range(num_ingredients)) / total_optimal_mass
        final_k2o = sum(optimal_quantities[i] * ingredients_df.loc[i, 'K2O'] for i in range(num_ingredients)) / total_optimal_mass
        final_s = sum(optimal_quantities[i] * ingredients_df.loc[i, 'S'] for i in range(num_ingredients)) / total_optimal_mass

    return {
        'success': result.success,
        'message': result.message,
        'optimal_quantities': optimal_quantities,
        'final_composition': {
            'N': final_n,
            'P2O5': final_p2o5,
            'K2O': final_k2o,
            'S': final_s
        },
        'target_composition': {
            'N': target_n,
            'P2O5': target_p2o5,
            'K2O': target_k2o,
            'S': target_s
        },
        'objective_value': result.fun
    }

if __name__ == '__main__':
    # Exemple d'utilisation avec les données du CSV
    data = {
        'On': [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
        'Code': ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'e'],
        'Nom': ['TSP', 'SSP', 'AS', 'S elementaire', 'DAP', 'MAP', 'Uree', 'SOP', 'MOP', 'Ballast'],
        'N': [0.0, 0.0, 21.0, 0.0, 18.0, 12.0, 46.0, 0.0, 0.0, 0.0],
        'P2O5': [46.0, 20.0, 0.0, 0.0, 46.0, 52.0, 0.0, 0.0, 0.0, 0.0],
        'K2O': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 50.0, 60.0, 0.0],
        'S': [0.5, 14.0, 24.0, 100.0, 0.8, 0.8, 0.0, 18.0, 0.0, 0.0]
    }
    ingredients_df = pd.DataFrame(data)

    # Définir les objectifs et les ingrédients actifs
    target_n = 10.0
    target_p2o5 = 20.0
    target_k2o = 10.0
    target_s = 5.0

    # Indices des ingrédients actifs (basé sur la colonne 'On' du CSV)
    active_ingredients_indices = ingredients_df[ingredients_df['On'] == 1].index.tolist()

    results = optimize_fertilizer_blend(
        ingredients_df, target_n, target_p2o5, target_k2o, target_s, active_ingredients_indices
    )

    print("\n--- Résultats de l'optimisation ---")
    print(f"Succès: {results['success']}")
    print(f"Message: {results['message']}")
    print("Quantités optimales par ingrédient:")
    for i, qty in enumerate(results['optimal_quantities']):
        print(f"  {ingredients_df.loc[i, 'Nom']}: {qty:.4f}")
    print("\nComposition finale obtenue:")
    print(f"  N: {results['final_composition']['N']:.2f}%")
    print(f"  P2O5: {results['final_composition']['P2O5']:.2f}%")
    print(f"  K2O: {results['final_composition']['K2O']:.2f}%")
    print(f"  S: {results['final_composition']['S']:.2f}%")
    print("\nObjectifs:")
    print(f"  N: {results['target_composition']['N']:.2f}%")
    print(f"  P2O5: {results['target_composition']['P2O5']:.2f}%")
    print(f"  K2O: {results['target_composition']['K2O']:.2f}%")
    print(f"  S: {results['target_composition']['S']:.2f}%")
    print(f"\nValeur de la fonction objectif (écart quadratique): {results['objective_value']:.6f}")