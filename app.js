// Configuration
const API_BASE_URL = "https://hazelnut.onrender.com";

// --- PUBLIC CALCULATOR LOGIC ---
const calcForm = document.getElementById('calcForm');

if (calcForm) {
    calcForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. GATHER NEW INPUTS
        // We no longer send 'certification_cost' or 'climate_type'.
        // We NOW send 'quality_class' and 'commercial_yield_pct'.
        const formData = {
            production_cost_ha: parseFloat(document.getElementById('prodCost').value),
            yield_ha: parseFloat(document.getElementById('yield').value),
            commercial_yield_pct: parseFloat(document.getElementById('commYield').value),
            quality_class: document.getElementById('qualityClass').value
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
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Calculation Error:', error);
            alert('Could not connect to the calculation engine.');
        }
    });
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const breakdownDiv = document.getElementById('breakdown');
    const b = data.breakdown;
    
    resultsDiv.classList.remove('hidden');
    
    // Update the Big Price Display
    document.getElementById('finalPrice').innerText = `€${data.final_price.toFixed(2)}`;

    // 2. DISPLAY UPDATED BREAKDOWN
    breakdownDiv.innerHTML = `
        <div class="flex justify-between border-b border-emerald-200 py-1">
            <span>Base Cost + Margin:</span> 
            <b>€${(b.base_cost_kg + b.margin_value).toFixed(2)}</b>
        </div>
        <div class="flex justify-between border-b border-emerald-200 py-1 text-emerald-700">
            <span>Quality Adjustment:</span> 
            <b>${b.quality_adj > 0 ? '+' : ''}€${b.quality_adj.toFixed(2)}</b>
        </div>
        <div class="flex justify-between border-b border-emerald-200 py-1 text-emerald-700">
            <span>Risk Premium (Yield Ratio ${b.yield_ratio}):</span> 
            <b>+€${b.risk_premium.toFixed(2)}</b>
        </div>
        
        <div class="flex justify-between pt-2 mt-2 border-t border-emerald-200 text-xs text-gray-500">
            <span>Consortium Floor Price:</span>
            <span>€${b.consortium_min.toFixed(2)}</span>
        </div>
        
        <div class="flex justify-between text-xs text-gray-500">
            <span>Marketable Yield: ${b.marketable_yield_kg} kg/ha</span>
        </div>
    `;
}