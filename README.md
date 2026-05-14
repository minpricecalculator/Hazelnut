# PGI Hazelnut Price Calculator 🌰

**A transparent, open-source tool for determining the economically sustainable minimum price for Giffoni Hazelnut PGI producers.**

This project allows farmers to calculate a fair minimum price ($P_{min}$) that covers production costs, guarantees a profit margin, and automatically adjusts for quality grade and a composite climate risk assessment. All parameters are managed by the Consortium administrator and applied consistently across all farms.

---

## 🌐 Live Calculator

**[minpricecalculator.github.io/Hazelnut/index.html](https://minpricecalculator.github.io/Hazelnut/index.html)**

---

## 📐 Calculation Methodology

The calculator uses a 7-step algorithm to ensure fairness, transparency, and economic sustainability.

### The Core Formula

$$P_{min} = \text{Cost with Margin} + \text{Quality Adjustment} + \text{Risk Premium}$$

*The final price is always the greater of $P_{min}$ or the Consortium Floor Price.*

---

### Step-by-Step Logic

#### Step 1: Marketable Yield
The actual net kernel weight per hectare, derived from the raw in-shell harvest.

```
Marketable_Yield = Raw_Yield_kg_ha × (Marketable_% / 100)
```

> Yield is expressed **in-shell (kg/ha)**. The Marketable % (kernel-to-shell ratio, also known as "yield point") defaults to **45%** but is editable by the farmer per batch.

---

#### Step 2: Base Production Cost
The break-even cost per kg, incorporating the fixed certification fee set by the Consortium.

```
Base_Cost = (Production_Costs_ha + Certification_Defaults_ha) / Marketable_Yield
```

> Certification defaults are currently set at **€25/ha**, managed by the Consortium administrator.

---

#### Step 3: Economic Margin
A mandatory profit margin is applied to ensure farm sustainability.

```
Cost_with_Margin = Base_Cost × (1 + Margin_%)
```

> The margin is currently set at **10%**, fixed by the Consortium.

---

#### Step 4: Quality Adjustment
A fixed €/kg correction is applied based on the quality class of the batch.

| Class | Description | Adjustment (€/kg) |
| :--- | :--- | :--- |
| **A** | Premium: high uniformity, low defects. | **+€0.20** |
| **B** | Standard: PGI-compliant commercial quality. | **€0.00** |
| **C** | Low: borderline quality, higher defects. | **−€0.15** |

> Defaults to **Class B**. Editable by the farmer per batch.

---

#### Step 5: Climate-Adjusted Yield
Rather than relying on raw yield alone, the system computes a composite signal combining the actual harvest with two farmer-reported coefficients.

```
Climate_Adjusted_Yield = Raw_Yield × Climate_Coeff × Coping_Coeff
```

| Coefficient | Description | Range |
| :--- | :--- | :--- |
| **Climate Effect** | Farmer's self-assessment of seasonal climate impact on yield potential. 1.0 = neutral year; < 1.0 = adverse; > 1.0 = favourable. | 0.5 – 1.5 |
| **Coping Capacity** | Farmer's self-assessment of farm resilience to climate stress (irrigation, insurance, financial reserves). | 0.5 – 1.5 |

Both are entered via sliders in the calculator interface.

---

#### Step 6: Adjusted Ratio
The climate-adjusted yield is compared against the Consortium's reference yield benchmark.

```
Adjusted_Ratio = Climate_Adjusted_Yield / Reference_Yield
```

> Reference Yield is currently set at **1,660 kg/ha**, managed by the Consortium administrator.

---

#### Step 7: Risk Premium
The Adjusted Ratio determines the risk tier and corresponding premium.

| Adjusted Ratio | Interpretation | Risk Premium (€/kg) |
| :--- | :--- | :--- |
| **≥ 0.90** | Normal year | **€0.00** |
| **0.70 – 0.89** | Mild stress | **+€0.10** |
| **0.50 – 0.69** | Severe stress | **+€0.25** |
| **< 0.50** | Extreme year | **+€0.40** |

---

## ⚙️ Consortium Parameters

All fixed parameters are managed by the Consortium administrator via the admin panel and take effect immediately for all subsequent calculations.

| Parameter | Current Value |
| :--- | :--- |
| Certification Defaults | €25/ha |
| Default Marketable % | 45% |
| Minimum Margin | 10% |
| Reference Yield | 1,660 kg/ha |
| Floor Price | €3.62/kg |

---

## 🏗 Technical Architecture

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML / Tailwind CSS / Vanilla JS — hosted on GitHub Pages |
| **Backend** | Python / Flask REST API — deployed on Render |
| **Parameters** | JSON file, editable at runtime via admin panel |
| **Auth** | Session-based admin login (cookie, HTTPS) |

---

## 📁 Project Structure

```
├── index.html        # Public calculator (Italian)
├── about.html        # Methodology documentation (English)
├── about_it.html     # Methodology documentation (Italian)
├── admin.html        # Consortium admin panel
├── app.js            # Frontend logic
├── app.py            # Flask backend & calculation engine
├── params.json       # Live consortium parameters
└── requirements.txt  # Python dependencies
```

---

## 🚀 Running Locally

**Backend:**
```bash
cd hazelnut-project
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd hazelnut-project
python -m http.server 8000
```

Then open **[http://127.0.0.1:8000/index.html](http://127.0.0.1:8000/index.html)**

> Make sure to serve the frontend via HTTP server — opening `index.html` directly as a file (`file://`) will block API calls.

---

## 📄 License

Open source. Developed for the Consortium for the Protection of the Giffoni Hazelnut PGI.
