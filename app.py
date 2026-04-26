import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

st.set_page_config(page_title="County Income Predictor", layout="wide")

@st.cache_resource
def load_artifacts():
    model = joblib.load("model.pkl")
    feature_names = joblib.load("feature_names.pkl")
    cv_rmse = joblib.load("cv_rmse.pkl")
    return model, feature_names, cv_rmse

model, feature_names, cv_rmse = load_artifacts()

st.title("U.S. County Median Household Income Predictor")
st.caption(
    "Data source: 2024 U.S. Census Bureau American Community Survey (ACS) 5-Year Estimates. "
    "Intended for federal agency use in screening counties for economic development grants."
)

st.sidebar.header("County Characteristics")
st.sidebar.markdown("Adjust sliders to match the target county's ACS profile.")

labor_force_pct   = st.sidebar.slider("Labor Force Participation (%)",      35.0, 80.0, 62.0, 0.5)
unemployment_rate = st.sidebar.slider("Unemployment Rate (%)",                2.0, 25.0,  5.5, 0.1)
mean_commute_min  = st.sidebar.slider("Mean Commute Time (minutes)",         10.0, 55.0, 27.0, 0.5)
pct_mgmt          = st.sidebar.slider("Management / Professional Occ. (%)",   5.0, 50.0, 22.0, 0.5)
pct_service       = st.sidebar.slider("Service Occupations (%)",              8.0, 40.0, 18.0, 0.5)
pct_sales         = st.sidebar.slider("Sales & Office Occupations (%)",       8.0, 35.0, 22.0, 0.5)
pct_construction  = st.sidebar.slider("Construction & Extraction Occ. (%)",   2.0, 25.0,  9.0, 0.5)
pct_production    = st.sidebar.slider("Production & Transportation Occ. (%)", 2.0, 30.0, 10.0, 0.5)
pct_insured       = st.sidebar.slider("Health Insurance Coverage (%)",       50.0,100.0, 90.0, 0.5)
pct_poverty       = st.sidebar.slider("Population Below Poverty Line (%)",    2.0, 45.0, 13.0, 0.5)

collar_ratio = (pct_mgmt + pct_sales) / (pct_construction + pct_production + 0.01)

feature_values = {
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
}

input_df = pd.DataFrame([{k: feature_values[k] for k in feature_names}])

prediction = model.predict(input_df)[0]
lower = prediction - cv_rmse
upper = prediction + cv_rmse

st.subheader("Predicted Median Household Income")
col1, col2, col3 = st.columns(3)
col1.metric("Lower Bound", f"${max(lower, 0):,.0f}", help=f"Prediction − CV RMSE (±${cv_rmse:,.0f})")
col2.metric("Prediction",  f"${prediction:,.0f}")
col3.metric("Upper Bound", f"${upper:,.0f}",         help=f"Prediction + CV RMSE (±${cv_rmse:,.0f})")

st.caption(
    f"Uncertainty range based on cross-validated RMSE of **${cv_rmse:,.0f}**. "
    "Range reflects model error on held-out counties, not a statistical confidence interval."
)

st.divider()

st.subheader("Feature Importances")
st.caption(
    ":orange[**Predictive, not causal.**] Importance scores reflect which features the model "
    "relies on most — they do not imply that changing a feature will cause income to change."
)

importances = model.feature_importances_
importance_df = (
    pd.DataFrame({"Feature": feature_names, "Importance": importances})
    .sort_values("Importance")
)

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(importance_df["Feature"], importance_df["Importance"], color="#4C72B0")
ax.set_xlabel("Mean Decrease in Impurity (normalized)")
ax.set_title("Random Forest Feature Importances", fontsize=12, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="y", labelsize=9)
for bar, val in zip(bars, importance_df["Importance"]):
    ax.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}", va="center", fontsize=8)
fig.tight_layout()
st.pyplot(fig)

st.divider()
with st.expander("Engineered feature details"):
    st.markdown(
        f"""
**collar_ratio** = (pct\\_mgmt + pct\\_sales) / (pct\\_construction + pct\\_production + 0.01)

Current value: **{collar_ratio:.3f}**

Captures the relative share of white-collar versus blue-collar occupations in the county workforce.
The +0.01 offset prevents division by zero in counties with negligible blue-collar employment.
        """
    )
