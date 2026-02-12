import os
import json
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)

# Security & Config
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'pgi_hazelnut_secure_key_2026')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False 
CORS(app, supports_credentials=True, origins=[
    "https://minpricecalculator.github.io",
    "http://127.0.0.1:8000",
    "http://localhost:8000"
    ])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_FILE = os.path.join(BASE_DIR, 'params.json')
ADMIN_PASSWORD = os.environ.get('HAZELNUT_ADMIN_PASS', 'Consortium2026')

# --- DATA PERSISTENCE ---

def load_params():
    default_params = {
        "min_margin_pct": 0.15,
        "reference_yield_kg_ha": 1600.0,
        "certification_defaults_ha": 200.0,
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
            return jsonify({"error": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- LOGIC ---

def get_risk_premium(yield_ratio, table):
    t = table['thresholds']
    p = table['premiums']
    if yield_ratio >= t[0]: return p[0]
    elif yield_ratio >= t[1]: return p[1]
    elif yield_ratio >= t[2]: return p[2]
    else: return p[3]

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    params = load_params()
    
    try:
        # Inputs from User
        costs_ha = float(data['production_cost_ha'])
        yield_ha = float(data['yield_ha'])
        marketable_pct = float(data['commercial_yield_pct'])
        quality_class = data['quality_class']

        # Step 1: Marketable Yield
        y_marketable = yield_ha * (marketable_pct / 100.0)

        if y_marketable <= 0:
            return jsonify({"error": "Marketable yield cannot be zero"}), 400

        # Step 2: Base Cost Calculation
        cert_defaults = params['certification_defaults_ha']
        base_cost_kg = (costs_ha + cert_defaults) / y_marketable

        # Step 3: Margin
        margin_pct = params['min_margin_pct']
        cost_with_margin = base_cost_kg * (1 + margin_pct)

        # Step 4: Quality Adjustment
        quality_adj = params['quality_table'].get(quality_class, 0.0)

        # Step 5: Risk Adjustment
        y_ref = params['reference_yield_kg_ha']
        yield_ratio = y_marketable / y_ref
        risk_premium = get_risk_premium(yield_ratio, params['risk_table'])

        # --- VISUAL CONSISTENCY LOGIC ---
        # Round components FIRST so the sum matches the display exactly
        b_base = round(base_cost_kg, 2)
        b_margin = round(cost_with_margin - base_cost_kg, 2)
        b_quality = round(quality_adj, 2)
        b_risk = round(risk_premium, 2)

        # Sum the rounded parts
        calculated_price = b_base + b_margin + b_quality + b_risk
        
        # Apply Floor
        final_price = max(calculated_price, params.get('min_consortium_price', 0))

        return jsonify({
            "final_price": final_price, 
            "breakdown": {
                "marketable_yield_kg": round(y_marketable, 1),
                "yield_ratio": round(yield_ratio, 2),
                "base_cost_kg": b_base,
                "margin_value": b_margin,
                "quality_adj": b_quality,
                "risk_premium": b_risk,
                "consortium_min": params.get('min_consortium_price', 0)
            }
        })

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['POST'])
def login():
    data = request.json
    if data.get('password') == ADMIN_PASSWORD:
        session['logged_in'] = True
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid password"}), 401

@app.route('/admin/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({"message": "Logged out"}), 200

@app.route('/admin/parameters', methods=['GET'])
@login_required
def get_parameters():
    return jsonify(load_params())

@app.route('/admin/parameters', methods=['POST'])
@login_required
def update_parameters():
    new_params = request.json
    save_params(new_params)
    return jsonify({"message": "Parameters updated successfully"}), 200

if __name__ == '__main__':
    if not os.path.exists(PARAMS_FILE):
        save_params(load_params())
    app.run(debug=True, host='0.0.0.0', port=5000)