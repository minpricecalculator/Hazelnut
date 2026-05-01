import os
import json
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)

# Security & Config
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'pgi_hazelnut_secure_key_2026')
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,
    SECRET_KEY='minpricecalculator'
)

CORS(app, supports_credentials=True, origins=[
    "https://minpricecalculator.github.io"
])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_FILE = os.path.join(BASE_DIR, 'params.json')
ADMIN_PASSWORD = os.environ.get('HAZELNUT_ADMIN_PASS', 'Consortium2026')

# --- DATA PERSISTENCE ---

def load_params():
    default_params = {
        "min_margin_pct": 0.15,
        "reference_yield_kg_ha": 1660.0,
        "certification_defaults_ha": 25.0,
        "default_marketable_pct": 45.0,
        "min_consortium_price": 0.0,
        "quality_table": { "A": 0.20, "B": 0.00, "C": -0.15 },
        "risk_table": {
            "thresholds": [0.90, 0.70, 0.50],
            "premiums": [0.00, 0.10, 0.25, 0.40]
        }
    }

    if not os.path.exists(PARAMS_FILE):
        return default_params

    try:
        with open(PARAMS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default_params

def save_params(params):
    with open(PARAMS_FILE, 'w') as f:
        json.dump(params, f, indent=4)

# --- AUTHENTICATION ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({"error": "Accesso non autorizzato"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- LOGIC ---

def get_risk_premium(adjusted_ratio, table):
    t = table['thresholds']
    p = table['premiums']
    if adjusted_ratio >= t[0]: return p[0]
    elif adjusted_ratio >= t[1]: return p[1]
    elif adjusted_ratio >= t[2]: return p[2]
    else: return p[3]

# --- PUBLIC ROUTES ---

@app.route('/public/defaults', methods=['GET'])
def public_defaults():
    params = load_params()
    return jsonify({
        "default_marketable_pct": params.get('default_marketable_pct', 45.0)
    })

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    params = load_params()

    try:
        # Input del produttore
        costs_ha       = float(data['production_cost_ha'])
        yield_ha       = float(data['yield_ha'])
        marketable_pct = float(data['commercial_yield_pct'])
        quality_class  = data['quality_class']
        climate_coeff  = float(data['climate_coeff'])
        coping_coeff   = float(data['coping_coeff'])

        # Validazione coefficienti
        for coeff, name in [(climate_coeff, 'Coefficiente climatico'), (coping_coeff, 'Coefficiente di resilienza')]:
            if not (0.5 <= coeff <= 1.5):
                return jsonify({"error": f"{name} deve essere compreso tra 0,5 e 1,5"}), 400

        # Passo 1: Resa Commercializzabile (per il calcolo dei costi)
        y_marketable = yield_ha * (marketable_pct / 100.0)
        if y_marketable <= 0:
            return jsonify({"error": "La resa commercializzabile non può essere zero"}), 400

        # Passo 2: Costo Base
        cert_defaults = params['certification_defaults_ha']
        base_cost_kg = (costs_ha + cert_defaults) / y_marketable

        # Passo 3: Margine
        margin_pct = params['min_margin_pct']
        cost_with_margin = base_cost_kg * (1 + margin_pct)

        # Passo 4: Correzione Qualità
        quality_adj = params['quality_table'].get(quality_class, 0.0)

        # Passo 5: Premio di Rischio Adeguato al Clima
        # Resa Grezza × Coeff. Clima × Coeff. Resilienza = segnale composito di stress
        y_ref = params['reference_yield_kg_ha']
        climate_adjusted_yield = yield_ha * climate_coeff * coping_coeff
        adjusted_ratio = climate_adjusted_yield / y_ref
        risk_premium = get_risk_premium(adjusted_ratio, params['risk_table'])

        # Arrotondamento componenti per coerenza visiva
        b_base    = round(base_cost_kg, 2)
        b_margin  = round(cost_with_margin - base_cost_kg, 2)
        b_quality = round(quality_adj, 2)
        b_risk    = round(risk_premium, 2)

        calculated_price = b_base + b_margin + b_quality + b_risk
        final_price = max(calculated_price, params.get('min_consortium_price', 0))

        return jsonify({
            "final_price": final_price,
            "breakdown": {
                "marketable_yield_kg":    round(y_marketable, 1),
                "climate_adjusted_yield": round(climate_adjusted_yield, 1),
                "adjusted_ratio":         round(adjusted_ratio, 2),
                "climate_coeff":          climate_coeff,
                "coping_coeff":           coping_coeff,
                "base_cost_kg":           b_base,
                "margin_value":           b_margin,
                "quality_adj":            b_quality,
                "risk_premium":           b_risk,
                "consortium_min":         params.get('min_consortium_price', 0)
            }
        })

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Input non valido: {str(e)}"}), 400

# --- ROTTE AMMINISTRAZIONE ---

@app.route('/admin/login', methods=['POST'])
def login():
    data = request.json
    if data.get('password') == ADMIN_PASSWORD:
        session['logged_in'] = True
        return jsonify({"message": "Accesso effettuato con successo"}), 200
    return jsonify({"error": "Password non valida"}), 401

@app.route('/admin/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({"message": "Disconnessione effettuata"}), 200

@app.route('/admin/parameters', methods=['GET'])
@login_required
def get_parameters():
    return jsonify(load_params())

@app.route('/admin/parameters', methods=['POST'])
@login_required
def update_parameters():
    new_params = request.json
    save_params(new_params)
    return jsonify({"message": "Parametri aggiornati con successo"}), 200

if __name__ == '__main__':
    if not os.path.exists(PARAMS_FILE):
        save_params(load_params())
    app.run(debug=True, host='0.0.0.0', port=5000)
