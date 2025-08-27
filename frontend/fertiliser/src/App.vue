<template>
    
    <!-- Barre du logo -->
    <div class="bg-surface-100 dark:bg-surface-800 shadow-sm border-b border-surface-200 dark:border-surface-700">
  <div class="container mx-auto px-4 py-4">
    <div class="flex items-center">
      <!-- Logo agrandi -->
      <img 
        src="/logo.png" 
        alt="Logo de la société" 
        class="h-14 w-auto mr-4"  
      />
      <!-- Texte qui suit le thème -->
      <span class="text-2xl font-bold text-surface-900 dark:text-white">
        Office chérifien des phosphates
      </span>
    </div>
  </div>
</div>
    

<div class="mt-8">
    <div class="card flex justify-center">
        <Stepper value="1" class="basis-[50rem]">
            <StepList>
                <Step value="1">Composition</Step>
                <Step value="2">Ingrédients</Step>
                <Step value="3">Résultats</Step>
            </StepList>
            <StepPanels>
                <StepPanel v-slot="{ activateCallback }" value="1">
                    <div class="flex flex-col min-h-48">
                        <div class="flex flex-col space-y-6 flex-auto">
                            <!-- Première ligne - Le bouton -->
                            <div class="card flex justify-center">
                                <SelectButton v-model="choix" :options="options" />
                            </div>

                            <!-- Lignes suivantes - Les champs avec séparation -->
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 flex-auto">
                                <!-- Champ N -->
                                <div class="card flex justify-center p-4 border-round border-1 surface-border">
                                    <div class="w-56">
                                        <label class="block text-sm font-medium mb-2">Azote (N)</label>
                                        <InputText v-model.number="N" class="w-full mb-4" />
                                        <Slider v-model="N" class="w-full" />
                                    </div>
                                </div>

                                <!-- Champ K2O5 -->
                                <div class="card flex justify-center p-4 border-round border-1 surface-border">
                                    <div class="w-56">
                                        <label class="block text-sm font-medium mb-2">Phosphate (P₂O₅)</label>
                                        <InputText v-model.number="K2O5" class="w-full mb-4" />
                                        <Slider v-model="K2O5" class="w-full" />
                                    </div>
                                </div>

                                <!-- Champ K2O -->
                                <div class="card flex justify-center p-4 border-round border-1 surface-border">
                                    <div class="w-56">
                                        <label class="block text-sm font-medium mb-2">Potasse (K₂O)</label>
                                        <InputText v-model.number="K2O" class="w-full mb-4" />
                                        <Slider v-model="K2O" class="w-full" />
                                    </div>
                                </div>

                                <!-- Champ S -->
                                <div class="card flex justify-center p-4 border-round border-1 surface-border">
                                    <div class="w-56">
                                        <label class="block text-sm font-medium mb-2">Soufre (S)</label>
                                        <InputText v-model.number="S" class="w-full mb-4" />
                                        <Slider v-model="S" class="w-full" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex pt-6 justify-end mt-auto">
                        <Button label="Next" icon="pi pi-arrow-right" iconPos="right" @click="activateCallback('2')" />
                    </div>
                </StepPanel>

                <StepPanel v-slot="{ activateCallback }" value="2">
                    <div class="flex flex-col min-h-48">
                        <!-- Tableau avec hauteur flexible -->
                        <div class="flex-grow border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 overflow-hidden">
                            <DataTable 
                                v-model:selection="selectedProducts" 
                                :value="ingredients" 
                                dataKey="id" 
                                tableStyle="min-width: 50rem"
                                class="h-full"
                                scrollable
                                :scrollHeight="ingredients.length > 5 ? 'flex' : null"
                                responsiveLayout="scroll"
                            >
                                <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                                <Column field="code" header="Code" :sortable="true"></Column>
                                <Column field="name" header="Nom" :sortable="true"></Column>
                                
                            </DataTable>
                        </div>

                        <!-- Boutons de navigation -->
                        <div class="flex pt-6 justify-between">
                            <Button label="Retour" severity="secondary" icon="pi pi-arrow-left" @click="activateCallback('1')" />
                            <Button 
                                label="Calculer" 
                                icon="pi pi-calculator" 
                                iconPos="right" 
                                @click="calculateAndProceed(activateCallback)" 
                                :disabled="!selectedProducts || selectedProducts.length === 0"
                                severity="success"
                            />
                        </div>
                    </div>
                </StepPanel>

                <StepPanel v-slot="{ activateCallback }" value="3">
                    <div class="flex flex-col min-h-48">
                        <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto p-6">
                            <div v-if="loading" class="flex justify-center items-center h-48">
                                <div class="text-center">
                                    <i class="pi pi-spin pi-spinner text-4xl text-blue-500"></i>
                                    <p class="mt-2">Calcul en cours...</p>
                                </div>
                            </div>
                            
                            <div v-else-if="error" class="flex justify-center items-center h-48">
                                <div class="text-center text-red-500">
                                    <i class="pi pi-times-circle text-4xl"></i>
                                    <p class="mt-2">{{ error }}</p>
                                </div>
                            </div>
                            
                            <div v-else-if="resultData" class="space-y-6">
                                <!-- En-tête avec statut -->
                                <div class="text-center">
                                    <div class="flex items-center justify-center mb-2">
                                        <i class="pi pi-check-circle text-green-500 text-2xl mr-2"></i>
                                        <h3 class="text-xl font-bold">Optimisation Réussie</h3>
                                    </div>
                                    <p class="text-gray-600">{{ resultData.solver_status }}</p>
                                </div>

                                <!-- Graphique de comparaison -->
                                <div class="card">
                                    <Chart type="bar" :data="chartData" :options="chartOptions" class="h-64" />
                                </div>

                                <!-- Comparaison objectif vs résultat -->
                                <Panel header="Détails des résultats" toggleable>
                                    <div class="grid grid-cols-2 gap-6 mb-4">
                                        <div>
                                            <h4 class="font-semibold mb-3 text-blue-600">Objectif</h4>
                                            <div class="space-y-2">
                                                <div class="flex justify-between"><span>N:</span><span class="font-bold">{{ resultData.target.n }}%</span></div>
                                                <div class="flex justify-between"><span>P₂O₅:</span><span class="font-bold">{{ resultData.target.p2o5 }}%</span></div>
                                                <div class="flex justify-between"><span>K₂O:</span><span class="font-bold">{{ resultData.target.k2o }}%</span></div>
                                                <div class="flex justify-between"><span>S:</span><span class="font-bold">{{ resultData.target.s }}%</span></div>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <h4 class="font-semibold mb-3 text-green-600">Résultat</h4>
                                            <div class="space-y-2">
                                                <div class="flex justify-between">
                                                    <span>N:</span>
                                                    <span :class="['font-bold', getVarianceClass('n')]">
                                                        {{ resultData.total_contribution.n.toFixed(2) }}%
                                                        <span class="text-sm ml-1">({{ formatVariance('n') }})</span>
                                                    </span>
                                                </div>
                                                <div class="flex justify-between">
                                                    <span>P₂O₅:</span>
                                                    <span :class="['font-bold', getVarianceClass('p2o5')]">
                                                        {{ resultData.total_contribution.p2o5.toFixed(2) }}%
                                                        <span class="text-sm ml-1">({{ formatVariance('p2o5') }})</span>
                                                    </span>
                                                </div>
                                                <div class="flex justify-between">
                                                    <span>K₂O:</span>
                                                    <span :class="['font-bold', getVarianceClass('k2o')]">
                                                        {{ resultData.total_contribution.k2o.toFixed(2) }}%
                                                        <span class="text-sm ml-1">({{ formatVariance('k2o') }})</span>
                                                    </span>
                                                </div>
                                                <div class="flex justify-between">
                                                    <span>S:</span>
                                                    <span :class="['font-bold', getVarianceClass('s')]">
                                                        {{ resultData.total_contribution.s.toFixed(2) }}%
                                                        <span class="text-sm ml-1">({{ formatVariance('s') }})</span>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Détails des ingrédients -->
                                    <h4 class="font-semibold mb-3 text-purple-400">Composition détaillée</h4>
                                    <div class="space-y-3">
                                        <div v-for="ingredient in resultData.ingredients" :key="ingredient.id" 
                                            class="p-3 rounded bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200">
                                            <div class="flex justify-between items-center mb-2">
                                                <span class="font-semibold">{{ ingredient.code }}</span>
                                                <span class="text-blue-500 font-bold">{{ ingredient.percentage.toFixed(2) }}%</span>
                                            </div>
                                            <div class="grid grid-cols-4 gap-2 text-sm">
                                                <div>N: {{ ingredient.contribution.n.toFixed(2) }}%</div>
                                                <div>P₂O₅: {{ ingredient.contribution.p2o5.toFixed(2) }}%</div>
                                                <div>K₂O: {{ ingredient.contribution.k2o.toFixed(2) }}%</div>
                                                <div>S: {{ ingredient.contribution.s.toFixed(2) }}%</div>
                                            </div>
                                        </div>
                                    </div>
                                </Panel>

                                <!-- Résumé des écarts -->
                                <div class="p-4 rounded bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200">
                                    <h4 class="font-semibold mb-2 text-orange-400">Écarts à l'objectif</h4>
                                    <div class="grid grid-cols-4 gap-2 text-sm">
                                        <div :class="getVarianceClass('n')">N: {{ formatVariance('n') }}</div>
                                        <div :class="getVarianceClass('p2o5')">P₂O₅: {{ formatVariance('p2o5') }}</div>
                                        <div :class="getVarianceClass('k2o')">K₂O: {{ formatVariance('k2o') }}</div>
                                        <div :class="getVarianceClass('s')">S: {{ formatVariance('s') }}</div>
                                    </div>
                                </div>
                            </div>

                            <div v-else class="flex justify-center items-center h-48">
                                <div class="text-center text-gray-500">
                                    <i class="pi pi-info-circle text-4xl"></i>
                                    <p class="mt-2">Cliquez sur "Calculer" pour voir les résultats</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex pt-6 justify-between">
                        <Button label="Retour" severity="secondary" icon="pi pi-arrow-left" @click="activateCallback('2')" />
                        <Button label="Nouveau calcul" icon="pi pi-refresh" @click="resetForm" severity="help" />
                    </div>
                </StepPanel>
            </StepPanels>
        </Stepper>
    </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import Chart from 'primevue/chart';

const choix = ref('NPK');
const options = ref(['NPK', 'NPK-S']);
const getPageId = (options) => (options === "NPK" ? 1 : 2);

const K2O5 = ref(50);
const N = ref(50);
const K2O = ref(50);
const S = ref(50);

const ingredients = ref([]);
const selectedProducts = ref([]);
const metaKey = ref(true);

const resultData = ref(null);
const loading = ref(false);
const error = ref(null);
const chartData = ref();
const chartOptions = ref();

// Chargement initial des ingrédients
onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:5000/api/ingredients", {
      params: { page_id: getPageId(choix.value) },
    });
    ingredients.value = response.data;
  } catch (error) {
    console.error("Erreur lors du chargement des ingredients :", error);
  }
});

// Recharger les ingrédients quand le choix change
watch(choix, async (newValue) => {
  try {
    const response = await axios.get("http://localhost:5000/api/ingredients", {
      params: { page_id: getPageId(newValue) },
    });
    ingredients.value = response.data;
    selectedProducts.value = [];
  } catch (error) {
    console.error("Erreur lors du rechargement des ingredients :", error);
  }
});

// Fonction pour calculer et passer à l'étape suivante
const calculateAndProceed = async (activateCallback) => {
    await calculateOptimization();
    if (!error.value) {
        activateCallback('3');
    }
};

// Fonction de calcul d'optimisation
const calculateOptimization = async () => {
    loading.value = true;
    error.value = null;
    resultData.value = null;
    
    try {
        const requestData = {
            target: {
                N: parseFloat(N.value),
                P2O5: parseFloat(K2O5.value),
                K2O: parseFloat(K2O.value),
                S: parseFloat(S.value)
            },
            available_ingredients: selectedProducts.value.map(p => p.id)
        };

        console.log("Envoi des données au backend:", requestData);
        
        const response = await axios.post("http://localhost:5000/api/calculate", requestData);
        resultData.value = response.data;
        console.log("Réponse reçue:", resultData.value);
        
        updateChart();
        
    } catch (err) {
        console.error("Erreur lors du calcul:", err);
        error.value = err.response?.data?.message || "Erreur lors du calcul d'optimisation";
    } finally {
        loading.value = false;
    }
};

// Fonctions utilitaires
const formatVariance = (element) => {
    if (!resultData.value?.variance) return "0";
    const variance = resultData.value.variance[element];
    return variance > 0 ? `+${variance.toFixed(2)}` : variance.toFixed(2);
};

const getVarianceClass = (element) => {
    if (!resultData.value?.variance) return 'text-gray-500';
    const variance = resultData.value.variance[element];
    if (Math.abs(variance) < 0.1) return 'text-green-500';
    if (variance > 1) return 'text-green-500';
    if (variance < -1) return 'text-red-500';
    return 'text-yellow-500';
};

const updateChart = () => {
    if (!resultData.value) return;
    
    const documentStyle = getComputedStyle(document.documentElement);
    
    chartData.value = {
        labels: ['N', 'P₂O₅', 'K₂O', 'S'],
        datasets: [
            {
                label: 'Objectif',
                data: [
                    resultData.value.target.n,
                    resultData.value.target.p2o5,
                    resultData.value.target.k2o,
                    resultData.value.target.s
                ],
                backgroundColor: documentStyle.getPropertyValue('--blue-500'),
                borderColor: documentStyle.getPropertyValue('--blue-500'),
                borderWidth: 1
            },
            {
                label: 'Résultat',
                data: [
                    resultData.value.total_contribution.n,
                    resultData.value.total_contribution.p2o5,
                    resultData.value.total_contribution.k2o,
                    resultData.value.total_contribution.s
                ],
                backgroundColor: documentStyle.getPropertyValue('--green-500'),
                borderColor: documentStyle.getPropertyValue('--green-500'),
                borderWidth: 1
            }
        ]
    };
    
    chartOptions.value = {
        maintainAspectRatio: false,
        aspectRatio: 0.8,
        plugins: {
            legend: {
                labels: {
                    color: documentStyle.getPropertyValue('--text-color')
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: documentStyle.getPropertyValue('--text-secondary-color')
                },
                grid: {
                    color: documentStyle.getPropertyValue('--surface-border')
                }
            },
            y: {
                ticks: {
                    color: documentStyle.getPropertyValue('--text-secondary-color')
                },
                grid: {
                    color: documentStyle.getPropertyValue('--surface-border')
                }
            }
        }
    };
};

const resetForm = () => {
    resultData.value = null;
    selectedProducts.value = [];
};
</script>