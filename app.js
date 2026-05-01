// Configurazione
const API_BASE_URL = "https://hazelnut.onrender.com";

// --- AGGIORNAMENTO LIVE VALORI SLIDER ---
const climateSlider = document.getElementById('climateCoeff');
const copingSlider  = document.getElementById('copingCoeff');

function formatCoeff(val) {
    // Italian decimal separator: comma
    return parseFloat(val).toFixed(1).replace('.', ',');
}

if (climateSlider) {
    climateSlider.addEventListener('input', () => {
        document.getElementById('climateCoeffVal').textContent = formatCoeff(climateSlider.value);
    });
}
if (copingSlider) {
    copingSlider.addEventListener('input', () => {
        document.getElementById('copingCoeffVal').textContent = formatCoeff(copingSlider.value);
    });
}

// --- PRECOMPILAZIONE VALORI DEFAULT DAL PANNELLO ADMIN ---
async function prefillDefaults() {
    const commYieldInput = document.getElementById('commYield');
    if (!commYieldInput) return;

    try {
        const response = await fetch(`${API_BASE_URL}/public/defaults`);
        if (response.ok) {
            const defaults = await response.json();
            if (defaults.default_marketable_pct != null) {
                commYieldInput.placeholder = `ad esempio ${defaults.default_marketable_pct}`;
                commYieldInput.value = defaults.default_marketable_pct;
            }
        }
    } catch (e) {
        // Backend non raggiungibile — il placeholder HTML rimane
    }
}

prefillDefaults();

// --- LOGICA CALCOLATORE ---
const calcForm = document.getElementById('calcForm');

if (calcForm) {
    calcForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            production_cost_ha:   parseFloat(document.getElementById('prodCost').value),
            yield_ha:             parseFloat(document.getElementById('yield').value),
            commercial_yield_pct: parseFloat(document.getElementById('commYield').value),
            quality_class:        document.getElementById('qualityClass').value,
            climate_coeff:        parseFloat(document.getElementById('climateCoeff').value),
            coping_coeff:         parseFloat(document.getElementById('copingCoeff').value)
        };

        try {
            const response = await fetch(`${API_BASE_URL}/calculate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                alert(`Errore: ${data.error}`);
            }
        } catch (error) {
            console.error('Errore di calcolo:', error);
            alert('Impossibile connettersi al motore di calcolo.');
        }
    });
}

function getRiskLabel(ratio) {
    if (ratio >= 0.90) return '<span class="bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs font-bold">NORMALE</span>';
    if (ratio >= 0.70) return '<span class="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-xs font-bold">STRESS LIEVE</span>';
    if (ratio >= 0.50) return '<span class="bg-orange-100 text-orange-800 px-2 py-0.5 rounded text-xs font-bold">GRAVE</span>';
    return '<span class="bg-red-100 text-red-800 px-2 py-0.5 rounded text-xs font-bold">ESTREMO</span>';
}

function displayResults(data) {
    const resultsDiv   = document.getElementById('results');
    const breakdownDiv = document.getElementById('breakdown');
    const b = data.breakdown;

    resultsDiv.classList.remove('hidden');
    document.getElementById('finalPrice').innerText = `€${data.final_price.toFixed(2).replace('.', ',')}`;

    breakdownDiv.innerHTML = `
        <div class="flex justify-between border-b border-emerald-200 py-1">
            <span>Costo Base + Margine:</span>
            <b>€${(b.base_cost_kg + b.margin_value).toFixed(2).replace('.', ',')}</b>
        </div>
        <div class="flex justify-between border-b border-emerald-200 py-1">
            <span>Correzione Qualità:</span>
            <b class="${b.quality_adj >= 0 ? 'text-emerald-700' : 'text-red-600'}">${b.quality_adj > 0 ? '+' : ''}€${b.quality_adj.toFixed(2).replace('.', ',')}</b>
        </div>

        <div class="border-b border-emerald-200 py-2 space-y-1">
            <div class="flex justify-between">
                <span>Premio di Rischio:</span>
                <b class="text-emerald-700">+€${b.risk_premium.toFixed(2).replace('.', ',')}</b>
            </div>
            <div class="bg-blue-50 rounded p-2 text-xs text-blue-800 space-y-0.5">
                <div class="flex justify-between">
                    <span>Coeff. effetto climatico:</span><b>${formatCoeff(b.climate_coeff)}</b>
                </div>
                <div class="flex justify-between">
                    <span>Coeff. resilienza aziendale:</span><b>${formatCoeff(b.coping_coeff)}</b>
                </div>
                <div class="flex justify-between">
                    <span>Resa adeguata al clima:</span><b>${b.climate_adjusted_yield} kg/ha</b>
                </div>
                <div class="flex justify-between items-center">
                    <span>Rapporto adeguato:</span>
                    <span class="flex items-center gap-1"><b>${String(b.adjusted_ratio).replace('.', ',')}</b> ${getRiskLabel(b.adjusted_ratio)}</span>
                </div>
            </div>
        </div>

        <div class="flex justify-between pt-2 mt-1 border-t border-emerald-200 text-xs text-gray-500">
            <span>Prezzo Minimo Consortile:</span>
            <span>€${b.consortium_min.toFixed(2).replace('.', ',')}</span>
        </div>
        <div class="flex justify-between text-xs text-gray-500">
            <span>Resa Commercializzabile:</span>
            <span>${b.marketable_yield_kg} kg/ha</span>
        </div>
    `;
}
