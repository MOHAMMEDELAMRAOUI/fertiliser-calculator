// Configuration de l'API
const API_BASE_URL = '/api';

// Variables globales
let ingredientsData = [];
let currentResults = null;

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', function() {
    loadIngredients();
    setupEventListeners();
});

// Configuration des écouteurs d'événements
function setupEventListeners() {
    const optimizeBtn = document.getElementById('optimize-btn');
    const exportPdfBtn = document.getElementById('export-pdf-btn');
    const newCalculationBtn = document.getElementById('new-calculation-btn');

    optimizeBtn.addEventListener('click', runOptimization);
    exportPdfBtn.addEventListener('click', exportToPDF);
    newCalculationBtn.addEventListener('click', resetCalculation);
}

// Chargement des ingrédients depuis l'API
async function loadIngredients() {
    try {
        showMessage('Chargement des ingrédients...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/ingredients`);
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        ingredientsData = await response.json();
        renderIngredients();
        hideMessage();
        
    } catch (error) {
        console.error('Erreur lors du chargement des ingrédients:', error);
        showMessage(`Erreur lors du chargement des ingrédients: ${error.message}`, 'error');
    }
}

// Rendu des cartes d'ingrédients
function renderIngredients() {
    const container = document.getElementById('ingredients-container');
    container.innerHTML = '';

    ingredientsData.Nom.forEach((nom, index) => {
        const isActive = ingredientsData.On[index] === 1;
        
        const card = document.createElement('div');
        card.className = `ingredient-card ${isActive ? 'active' : ''}`;
        card.dataset.index = index;
        
        card.innerHTML = `
            <div class="ingredient-header">
                <div>
                    <div class="ingredient-name">${nom}</div>
                    <div class="ingredient-code">${ingredientsData.Code[index]}</div>
                </div>
                <div class="ingredient-toggle ${isActive ? 'active' : ''}" data-index="${index}"></div>
            </div>
            <div class="ingredient-composition">
                <div class="composition-item">
                    <span class="composition-label">N:</span>
                    <span class="composition-value">${ingredientsData.N[index]}%</span>
                </div>
                <div class="composition-item">
                    <span class="composition-label">P₂O₅:</span>
                    <span class="composition-value">${ingredientsData.P2O5[index]}%</span>
                </div>
                <div class="composition-item">
                    <span class="composition-label">K₂O:</span>
                    <span class="composition-value">${ingredientsData.K2O[index]}%</span>
                </div>
                <div class="composition-item">
                    <span class="composition-label">S:</span>
                    <span class="composition-value">${ingredientsData.S[index]}%</span>
                </div>
            </div>
        `;
        
        // Écouteur pour le toggle
        const toggle = card.querySelector('.ingredient-toggle');
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleIngredient(index);
        });
        
        // Écouteur pour la carte entière
        card.addEventListener('click', () => {
            toggleIngredient(index);
        });
        
        container.appendChild(card);
    });
}

// Basculer l'état d'un ingrédient
function toggleIngredient(index) {
    ingredientsData.On[index] = ingredientsData.On[index] === 1 ? 0 : 1;
    renderIngredients();
}

// Lancer l'optimisation
async function runOptimization() {
    try {
        // Validation des entrées
        const targets = getTargetValues();
        if (!validateTargets(targets)) {
            return;
        }

        // Vérifier qu'au moins un ingrédient est actif
        const activeIngredients = getActiveIngredients();
        if (activeIngredients.length === 0) {
            showMessage('Veuillez sélectionner au moins un ingrédient.', 'error');
            return;
        }

        // Interface de chargement
        setLoadingState(true);
        hideMessage();

        // Préparer les données pour l'API
        const requestData = {
            target_n: targets.n,
            target_p2o5: targets.p2o5,
            target_k2o: targets.k2o,
            target_s: targets.s,
            active_ingredients: activeIngredients
        };

        // Appel à l'API
        const response = await fetch(`${API_BASE_URL}/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erreur HTTP: ${response.status}`);
        }

        currentResults = await response.json();
        
        if (!currentResults.success) {
            throw new Error(`Optimisation échouée: ${currentResults.message}`);
        }

        displayResults();
        showMessage('Optimisation réussie !', 'success');

    } catch (error) {
        console.error('Erreur lors de l\'optimisation:', error);
        showMessage(`Erreur lors de l'optimisation: ${error.message}`, 'error');
    } finally {
        setLoadingState(false);
    }
}

// Récupérer les valeurs cibles
function getTargetValues() {
    return {
        n: parseFloat(document.getElementById('target-n').value) || 0,
        p2o5: parseFloat(document.getElementById('target-p2o5').value) || 0,
        k2o: parseFloat(document.getElementById('target-k2o').value) || 0,
        s: parseFloat(document.getElementById('target-s').value) || 0
    };
}

// Valider les valeurs cibles
function validateTargets(targets) {
    const errors = [];
    
    Object.entries(targets).forEach(([key, value]) => {
        if (isNaN(value) || value < 0 || value > 100) {
            errors.push(`${key.toUpperCase()}: valeur invalide (${value})`);
        }
    });
    
    if (errors.length > 0) {
        showMessage(`Erreurs de validation:\n${errors.join('\n')}`, 'error');
        return false;
    }
    
    return true;
}

// Récupérer les indices des ingrédients actifs
function getActiveIngredients() {
    return ingredientsData.On
        .map((status, index) => status === 1 ? index : null)
        .filter(index => index !== null);
}

// Gérer l'état de chargement
function setLoadingState(loading) {
    const btn = document.getElementById('optimize-btn');
    const btnText = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.loading-spinner');
    
    if (loading) {
        btn.disabled = true;
        btnText.style.display = 'none';
        spinner.style.display = 'block';
    } else {
        btn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

// Afficher les résultats
function displayResults() {
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    
    displayCompositionComparison();
    displayQuantitiesTable();
    
    // Faire défiler vers les résultats
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Afficher la comparaison de composition
function displayCompositionComparison() {
    const grid = document.getElementById('composition-grid');
    const final = currentResults.final_composition;
    const target = currentResults.target_composition;
    
    const elements = ['N', 'P2O5', 'K2O', 'S'];
    const labels = ['N', 'P₂O₅', 'K₂O', 'S'];
    
    grid.innerHTML = '';
    
    elements.forEach((element, index) => {
        const finalValue = final[element];
        const targetValue = target[element];
        const difference = Math.abs(finalValue - targetValue);
        const isGood = difference < 0.1;
        
        const item = document.createElement('div');
        item.className = 'comparison-item';
        
        item.innerHTML = `
            <div class="comparison-label">${labels[index]}</div>
            <div class="comparison-values">
                <span class="target-value">Cible: ${targetValue.toFixed(2)}%</span>
                <span class="actual-value">${finalValue.toFixed(2)}%</span>
            </div>
            <div class="difference ${isGood ? 'good' : 'warning'}">
                Écart: ${difference.toFixed(3)}%
            </div>
        `;
        
        grid.appendChild(item);
    });
}

// Afficher le tableau des quantités
function displayQuantitiesTable() {
    const tbody = document.querySelector('#quantities-table tbody');
    tbody.innerHTML = '';
    
    currentResults.ingredients_info.forEach(ingredient => {
        const row = document.createElement('tr');
        const isZero = ingredient.quantity < 0.0001;
        
        row.innerHTML = `
            <td>${ingredient.nom}</td>
            <td>${ingredient.code}</td>
            <td class="${isZero ? 'zero-quantity' : 'quantity-value'}">
                ${isZero ? '0.0000' : ingredient.quantity.toFixed(4)}
            </td>
            <td>${ingredient.composition.N.toFixed(1)}%</td>
            <td>${ingredient.composition.P2O5.toFixed(1)}%</td>
            <td>${ingredient.composition.K2O.toFixed(1)}%</td>
            <td>${ingredient.composition.S.toFixed(1)}%</td>
        `;
        
        tbody.appendChild(row);
    });
}

// Exporter en PDF (fonctionnalité basique)
function exportToPDF() {
    if (!currentResults) {
        showMessage('Aucun résultat à exporter.', 'error');
        return;
    }
    
    // Créer le contenu pour l'impression
    const printContent = generatePrintContent();
    
    // Ouvrir une nouvelle fenêtre pour l'impression
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Résultats d'Optimisation - Engrais</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #2563eb; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f8fafc; }
                .comparison { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }
                .comparison-item { border: 1px solid #ddd; padding: 15px; text-align: center; }
                @media print { body { margin: 0; } }
            </style>
        </head>
        <body>
            ${printContent}
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.focus();
    
    // Attendre que le contenu soit chargé puis imprimer
    setTimeout(() => {
        printWindow.print();
        printWindow.close();
    }, 250);
}

// Générer le contenu pour l'impression
function generatePrintContent() {
    const final = currentResults.final_composition;
    const target = currentResults.target_composition;
    const date = new Date().toLocaleDateString('fr-FR');
    
    let content = `
        <h1>🧪 Résultats d'Optimisation d'Engrais</h1>
        <p><strong>Date:</strong> ${date}</p>
        
        <h2>📊 Objectifs vs Résultats</h2>
        <div class="comparison">
            <div class="comparison-item">
                <h3>N</h3>
                <p>Cible: ${target.N.toFixed(2)}%</p>
                <p>Obtenu: ${final.N.toFixed(2)}%</p>
                <p>Écart: ${Math.abs(final.N - target.N).toFixed(3)}%</p>
            </div>
            <div class="comparison-item">
                <h3>P₂O₅</h3>
                <p>Cible: ${target.P2O5.toFixed(2)}%</p>
                <p>Obtenu: ${final.P2O5.toFixed(2)}%</p>
                <p>Écart: ${Math.abs(final.P2O5 - target.P2O5).toFixed(3)}%</p>
            </div>
            <div class="comparison-item">
                <h3>K₂O</h3>
                <p>Cible: ${target.K2O.toFixed(2)}%</p>
                <p>Obtenu: ${final.K2O.toFixed(2)}%</p>
                <p>Écart: ${Math.abs(final.K2O - target.K2O).toFixed(3)}%</p>
            </div>
            <div class="comparison-item">
                <h3>S</h3>
                <p>Cible: ${target.S.toFixed(2)}%</p>
                <p>Obtenu: ${final.S.toFixed(2)}%</p>
                <p>Écart: ${Math.abs(final.S - target.S).toFixed(3)}%</p>
            </div>
        </div>
        
        <h2>📈 Quantités Optimales</h2>
        <table>
            <thead>
                <tr>
                    <th>Ingrédient</th>
                    <th>Code</th>
                    <th>Quantité</th>
                    <th>N (%)</th>
                    <th>P₂O₅ (%)</th>
                    <th>K₂O (%)</th>
                    <th>S (%)</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    currentResults.ingredients_info.forEach(ingredient => {
        const isZero = ingredient.quantity < 0.0001;
        content += `
            <tr>
                <td>${ingredient.nom}</td>
                <td>${ingredient.code}</td>
                <td>${isZero ? '0.0000' : ingredient.quantity.toFixed(4)}</td>
                <td>${ingredient.composition.N.toFixed(1)}%</td>
                <td>${ingredient.composition.P2O5.toFixed(1)}%</td>
                <td>${ingredient.composition.K2O.toFixed(1)}%</td>
                <td>${ingredient.composition.S.toFixed(1)}%</td>
            </tr>
        `;
    });
    
    content += `
            </tbody>
        </table>
        
        <p><small>Généré par l'Optimiseur de Formulation d'Engrais</small></p>
    `;
    
    return content;
}

// Réinitialiser le calcul
function resetCalculation() {
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'none';
    currentResults = null;
    hideMessage();
    
    // Faire défiler vers le haut
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Afficher un message
function showMessage(message, type = 'info') {
    hideMessage(); // Cacher les messages précédents
    
    let messageElement;
    if (type === 'error') {
        messageElement = document.getElementById('error-message');
    } else if (type === 'success') {
        messageElement = document.getElementById('success-message');
    } else {
        // Pour les messages d'info, utiliser le message de succès avec un style différent
        messageElement = document.getElementById('success-message');
    }
    
    messageElement.textContent = message;
    messageElement.style.display = 'flex';
    
    // Auto-masquer les messages de succès après 5 secondes
    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            hideMessage();
        }, 5000);
    }
}

// Masquer les messages
function hideMessage() {
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('success-message').style.display = 'none';
}
