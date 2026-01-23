# Finance Standards & Formulas (Portugal)

This document defines the standard formulas, formatting rules, and definitions for the Personal Financial Advisor agent.

## 1. Localization & Formatting

- **Currency:** All monetary values must be displayed in Euros (€).
- **Number Format (PT):** Use dot (.) for thousands separator and comma (,) for decimals.
  - _Correct:_ `1.000,00 €`
  - _Incorrect:_ `1,000.00 €`
- **Date Format:** `DD/MM/YYYY`

## 2. Definitions

- **Conta Corrente (Current Account):** Liquidity for daily expenses.
- **Fundo de Maneio (Working Capital):** Short-term buffer (usually 1-2 months of expenses) kept in highly liquid accounts.
- **Fundo de Emergência (Emergency Fund):** Safety net for unexpected events (unemployment, health).
  - _Target Standard:_ 6 to 12 months of **Total Monthly Expenses**.
- **L.H. (Loan-to-Income / Taxa de Esforço):** Percentage of monthly net income dedicated to debt payments.

## 3. Official Formulas

### A. Taxa de Esforço (Debt-to-Income Ratio)

Used to assess mortgage eligibility.

$$
\text{Taxa de Esforço} = \frac{\text{Total Prestações Mensais de Créditos}}{\text{Rendimento Líquido Mensal}} \times 100
$$

- **Total Prestações:** Includes Mortgage + Personal Loans + Car Loans + Credit Cards.
- **Alert Threshold:** > 35% (Yellow), > 50% (Red).

### B. Rendimento Disponível Real (Real Disposable Income)

$$
\text{Simples} = \text{Rendimento Líquido} - \text{Custos Fixos}
$$

- **Custos Fixos:** Prestações de Crédito + Subscrições Recorrentes (Netflix, Ginásio, etc.) + Renda/Condomínio.

## 4. Taxes (Portugal Fiscal Rules)

### Capital Gains (Mais-Valias)

For investments like ETFs, Actions, Crypto (if applicable timeframe matches law).

- **Taxa Liberatória:** 28% on profit (profit = sell value - buy value).
- _Note:_ PPRs have reduced rates (21.5% down to 8.6%) depending on holding duration.

### IRS Brackets (Simplificação para Estimativa)

When estimating net income from gross updates, consider progressive progressive (Table update required annually).

- _Rule of Thumb:_ For high-level estimates, assume appropriate bracket retention + 11% SS.
