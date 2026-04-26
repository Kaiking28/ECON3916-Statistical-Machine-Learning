# Here is my Jupyter notebook for context. Use the feature names, ranges, and model setup from it.
# notebook: kai_final_project.ipynb
# features: labor_force_pct, unemployment_rate, mean_commute_min, pct_mgmt, pct_service,
#            pct_sales, pct_construction, pct_production, pct_insured, pct_poverty, collar_ratio
# collar_ratio = (pct_mgmt + pct_sales) / (pct_construction + pct_production + 0.01)
# model: RandomForestRegressor(random_state=42), CV RMSE ~$7,708

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

st.set_page_config(page_title="County Income Predictor", layout="wide")

@st.cache_resource
def load_artifacts():
    model        = joblib.load("model.pkl")
    feature_names = joblib.load("feature_names.pkl")
    cv_rmse      = joblib.load("cv_rmse.pkl")
    return model, feature_names, cv_rmse

model, feature_names, cv_rmse = load_artifacts()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("U.S. County Median Household Income Predictor")
st.markdown(
    "**Stakeholder use case:** Federal agencies (HUD / USDA Rural Development) screening counties "
    "for economic development grants. Counties where actual income falls well below the model's "
    "prediction signal structural disadvantage beyond what labor-market characteristics alone explain."
)
st.caption(
    "Data: 2024 U.S. Census Bureau American Community Survey (ACS) 5-Year Estimates — "
    "Economic Characteristics (DP03), 3,220 U.S. counties."
)

# ── Sidebar sliders ───────────────────────────────────────────────────────────
# Ranges and defaults derived from df.describe() in kai_final_project.ipynb
st.sidebar.header("County Characteristics")
st.sidebar.markdown("Adjust to match the target county's ACS profile.")

labor_force_pct   = st.sidebar.slider("Labor Force Participation (%)",      20.0,  87.0,  58.7, 0.1,
    help="Share of civilian population 16+ in the labor force. ACS range: 21.5–86.4.")
unemployment_rate = st.sidebar.slider("Unemployment Rate (%)",                0.0,  29.0,   4.5, 0.1,
    help="Percent unemployed of labor force. ACS range: 0–28.6.")
mean_commute_min  = st.sidebar.slider("Mean Commute Time (minutes)",          4.0,  50.0,  24.2, 0.5,
    help="Average one-way commute. ACS range: 4.9–49.6 min.")
pct_mgmt          = st.sidebar.slider("Management / Professional Occ. (%)",   6.0,  75.0,  34.6, 0.1,
    help="Share of workers in management, business, science, and arts. ACS range: 6.1–74.6.")
pct_service       = st.sidebar.slider("Service Occupations (%)",               0.0,  42.0,  16.6, 0.1,
    help="Share in service occupations. ACS range: 0–41.2.")
pct_sales         = st.sidebar.slider("Sales & Office Occupations (%)",        2.0,  36.0,  19.2, 0.1,
    help="Share in sales and office. ACS range: 2.3–36.0.")
pct_construction  = st.sidebar.slider("Construction & Extraction Occ. (%)",    1.0,  39.0,  11.7, 0.1,
    help="Share in construction, extraction, maintenance. ACS range: 1.2–38.2.")
pct_production    = st.sidebar.slider("Production & Transportation Occ. (%)",  0.0,  46.0,  15.9, 0.1,
    help="Share in production, transportation, material moving. ACS range: 0–45.1.")
pct_insured       = st.sidebar.slider("Health Insurance Coverage (%)",        55.0, 100.0,  92.3, 0.1,
    help="Share of population with any health insurance. ACS range: 55.4–99.8.")
pct_poverty       = st.sidebar.slider("Population Below Poverty Line (%)",     0.0,  63.0,   9.2, 0.1,
    help="Share below federal poverty threshold. ACS range: 0–62.9.")

# ── Engineered feature: must be computed from sliders before prediction ───────
collar_ratio = (pct_mgmt + pct_sales) / (pct_construction + pct_production + 0.01)

# ── Build input DataFrame in the exact column order saved by the notebook ─────
# feature_names.pkl = list(X_train.columns) after collar_ratio was appended
input_df = pd.DataFrame([{
    "labor_force_pct":   labor_force_pct,
    "unemployment_rate": unemployment_rate,
    "mean_commute_min":  mean_commute_min,
    "pct_mgmt":          pct_mgmt,
    "pct_service":       pct_service,
    "pct_sales":         pct_sales,
    "pct_construction":  pct_construction,
    "pct_production":    pct_production,
    "pct_insured":       pct_insured,
    "pct_poverty":       pct_poverty,
    "collar_ratio":      collar_ratio,
}])[feature_names]  # reorder to match training column order

# ── Prediction ─────────────────────────────────────────────────────────────────
prediction = float(model.predict(input_df)[0])
lower      = max(prediction - cv_rmse, 0)
upper      = prediction + cv_rmse

st.subheader("Predicted Median Household Income")

col1, col2, col3 = st.columns(3)
col1.metric("Lower Bound",  f"${lower:,.0f}", help=f"Prediction − CV RMSE  (±${cv_rmse:,.0f})")
col2.metric("Prediction",   f"${prediction:,.0f}")
col3.metric("Upper Bound",  f"${upper:,.0f}", help=f"Prediction + CV RMSE  (±${cv_rmse:,.0f})")

st.caption(
    f"Uncertainty range based on 5-fold cross-validated RMSE of **${cv_rmse:,.0f}** "
    f"(CV R² = 0.83). This reflects average model error on held-out counties, "
    f"not a statistical confidence interval. "
    f"Actual county incomes ranged from $16,314 (Las Marías, PR) to $181,765 (Loudoun Co., VA)."
)

# ── Grant-flag logic ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Grant Screening Signal")
actual_income = st.number_input(
    "Enter county's actual reported median income (optional, for gap analysis):",
    min_value=0, max_value=250000, value=0, step=1000,
    help="Leave at 0 to skip. Enter the ACS-reported median income for this county."
)
if actual_income > 0:
    gap = prediction - actual_income
    pct_gap = gap / prediction * 100
    if gap > cv_rmse:
        st.error(
            f"**Flag for review:** Actual income (${actual_income:,.0f}) is **${gap:,.0f} "
            f"({pct_gap:.1f}%) below** the model's prediction — more than 1 CV RMSE gap. "
            f"This county may be underperforming relative to its labor-market profile."
        )
    elif gap > 0:
        st.warning(
            f"Actual income (${actual_income:,.0f}) is ${gap:,.0f} below prediction "
            f"but within the model's normal error range (< 1 CV RMSE)."
        )
    else:
        st.success(
            f"Actual income (${actual_income:,.0f}) meets or exceeds the model's prediction. "
            f"No structural underperformance signal."
        )

# ── Feature importance chart ──────────────────────────────────────────────────
st.divider()
st.subheader("Feature Importances")
st.caption(
    ":orange[**Predictive, not causal.**] These scores show which features the Random Forest "
    "relied on most — they do not imply that changing a feature will cause income to change. "
    "Note: pct_poverty accounts for ~52% of importance, meaning the model partly predicts "
    "economic distress from economic distress. See the notebook's robustness check for a "
    "poverty-excluded version."
)

importances = model.feature_importances_
imp_df = (
    pd.DataFrame({"Feature": feature_names, "Importance": importances})
    .sort_values("Importance")
)

fig, ax = plt.subplots(figsize=(8, 4.5))
colors = ["#d62728" if f == "pct_poverty" else "#4C72B0" for f in imp_df["Feature"]]
bars = ax.barh(imp_df["Feature"], imp_df["Importance"], color=colors)
ax.set_xlabel("Mean Decrease in Impurity (normalized)")
ax.set_title("Random Forest Feature Importances\n(Predictive only — not causal)", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
for bar, val in zip(bars, imp_df["Importance"]):
    ax.text(val + 0.003, bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}", va="center", fontsize=8)
fig.tight_layout()
st.pyplot(fig)

# ── Engineered feature detail ─────────────────────────────────────────────────
st.divider()
with st.expander("collar_ratio — engineered feature details"):
    st.markdown(
        f"""
**collar_ratio** = (pct\\_mgmt + pct\\_sales) / (pct\\_construction + pct\\_production + 0.01)

Current value: **{collar_ratio:.3f}**

Captures the relative share of white-collar versus blue-collar occupations.
The +0.01 offset prevents division by zero in counties with negligible blue-collar employment.
Higher values indicate a workforce skewed toward professional and office occupations.
        """
    )
