---
name: financial-calculations
description: Python scripts for precise financial simulations (Mortgages, Compound Interest, Taxes)
---

# Financial Calculations Skill

Use these scripts to perform accurate calculations instead of relying on LLM mental math.

## Available Scripts

### 1. Mortgage Calculator (`mortgage_calculator.py`)

Calculates monthly payments based on loan amount, annual rate (Euribor + Spread), and years.

```python
# Usage Example
python /Users/luispoliveira/workspace/luispoliveira/everything-copilot-cli/.github/skills/financial-calculations/scripts/mortgage_calculator.py --amount 200000 --rate 3.5 --years 30
```

### 2. FIRE Projector (`fire_projector.py`)

Projects investment growth with compound interest.

```python
# Usage Example
python /Users/luispoliveira/workspace/luispoliveira/everything-copilot-cli/.github/skills/financial-calculations/scripts/fire_projector.py --initial 10000 --monthly 500 --rate 7 --years 20
```

### 3. Tax Estimator (`tax_estimator.py`)

Estimates net salary (approximate) and capital gains tax in Portugal.

```python
# Usage Example (Capital Gains)
python /Users/luispoliveira/workspace/luispoliveira/everything-copilot-cli/.github/skills/financial-calculations/scripts/tax_estimator.py --mode capital_gains --profit 1000 --type etf

# Usage Example (Net Salary Estimate - Simple)
python /Users/luispoliveira/workspace/luispoliveira/everything-copilot-cli/.github/skills/financial-calculations/scripts/tax_estimator.py --mode salary --gross 2000
```
