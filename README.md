# PGI Hazelnut Price Calculator 🌰

**A transparent, open-source tool for determining the economically sustainable minimum price for PGI Hazelnuts.**

This project allows producers to calculate a fair minimum price ($P_{min}$) that covers production costs, guarantees a profit margin, and automatically adjusts for quality grades and climate-induced yield losses.

---

## 📐 Calculation Methodology

The calculator uses a 5-step algorithm to ensure fairness and economic sustainability.

### 1. The Core Formula
The minimum price is calculated as:

$$P_{min} = \text{Cost with Margin} + \text{Quality Adjustment} + \text{Risk Premium}$$

*The final price is always the greater of $P_{min}$ or the Consortium Floor Price.*

### 2. Step-by-Step Logic

#### Step 1: Marketable Yield
First, we calculate the actual net weight of kernels (or yield point) per hectare.
> `Marketable_Yield = Raw_Yield_kg_ha × (Commercial_Yield_% / 100)`

#### Step 2: Base Production Cost
We determine the break-even cost per kg, adding the fixed certification fees set by the Consortium.
> `Base_Cost = (Production_Costs_ha + Certification_Defaults_ha) / Marketable_Yield`

#### Step 3: Economic Margin
A mandatory profit margin is applied to the base cost to ensure farm sustainability.
> `Cost_with_Margin = Base_Cost × (1 + Margin_%)`

#### Step 4: Quality Adjustment
Prices are adjusted based on the quality class of the batch.

| Class | Description | Adjustment (€/kg) |
| :--- | :--- | :--- |
| **A** | **Premium:** Fully compliant, high uniformity, low defects. | **+ €0.20** |
| **B** | **Standard:** PGI-compliant, standard commercial quality. | **€0.00** |
| **C** | **Low:** Borderline quality, higher defects. | **- €0.15** |

#### Step 5: Climate Risk Premium
Instead of subjective "Year Types," the system calculates a **Yield Ratio** to objectively measure crop stress.

> `Yield_Ratio = Marketable_Yield / Reference_Yield`

*Reference Yield is set by the Consortium (default: 1600 kg/ha).*

| Yield Ratio | Interpretation | Risk Premium (€/kg) |
| :--- | :--- | :--- |
| **≥ 0.90** | Normal Year | **€0.00** |
| **0.70 – 0.89** | Mild Stress | **+ €0.10** |
| **0.50 – 0.69** | Severe Stress | **+ €0.25** |
| **< 0.50** | Extreme Year | **+ €0.40** |
