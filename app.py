import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

st.set_page_config(page_title="County Income Predictor", layout="wide")

@st.cache_resource
def load_artifacts():
    model         = joblib.load("model.pkl")
    feature_names = joblib.load("feature_names.pkl")
    cv_rmse       = joblib.load("cv_rmse.pkl")
    return model, feature_names, cv_rmse

model, feature_names, cv_rmse = load_artifacts()

# Slider config for every feature the model knows about.
# collar_ratio is computed, so it has no slider entry — the app skips it automatically.
SLIDER_CFG = {
    "labor_force_pct":   dict(label="Labor Force Participation (%)",      min_value=20.0, max_value=87.0, value=58.7, step=0.1),
    "unemployment_rate": dict(label="Unemployment Rate (%)",               min_value=0.0,  max_value=29.0, value=4.5,  step=0.1),
    "mean_commute_min":  dict(label="Mean Commute Time (min)",             min_value=4.0,  max_value=50.0, value=24.2, step=0.5),
    "pct_mgmt":          dict(label="Management / Professional Occ. (%)",  min_value=6.0,  max_value=75.0, value=34.6, step=0.1),
    "pct_service":       dict(label="Service Occupations (%)",             min_value=0.0,  max_value=42.0, value=16.6, step=0.1),
    "pct_sales":         dict(label="Sales & Office Occupations (%)",      min_value=2.0,  max_value=36.0, value=19.2, step=0.1),
    "pct_construction":  dict(label="Construction & Extraction Occ. (%)",  min_value=1.0,  max_value=39.0, value=11.7, step=0.1),
    "pct_production":    dict(label="Production & Transport Occ. (%)",     min_value=0.0,  max_value=46.0, value=15.9, step=0.1),
    "pct_insured":       dict(label="Health Insurance Coverage (%)",       min_value=55.0, max_value=100.0,value=92.3, step=0.1),
    "pct_poverty":       dict(label="Population Below Poverty Line (%)",   min_value=0.0,  max_value=63.0, value=9.2,  step=0.1),
}

# ── Sidebar: show a slider for every feature_name that has a config entry ─────
st.sidebar.header("County Characteristics")
st.sidebar.caption("Ranges from 2024 ACS 5-Year Estimates, 3,220 U.S. counties.")

slider_vals = {}
for feat in feature_names:
    if feat in SLIDER_CFG:
        slider_vals[feat] = st.sidebar.slider(**SLIDER_CFG[feat])

# Compute engineered feature from sliders — must happen before prediction
if "collar_ratio" in feature_names:
    slider_vals["collar_ratio"] = (
        (slider_vals["pct_mgmt"] + slider_vals["pct_sales"])
        / (slider_vals["pct_construction"] + slider_vals["pct_production"] + 0.01)
    )

# Build input DataFrame in the exact column order from feature_names.pkl
input_df = pd.DataFrame([[slider_vals[f] for f in feature_names]], columns=feature_names)

# ── Prediction ────────────────────────────────────────────────────────────────
prediction = float(model.predict(input_df)[0])
lower      = max(prediction - cv_rmse, 0)
upper      = prediction + cv_rmse

st.title("U.S. County Median Household Income Predictor")
st.markdown(
    "**Use case:** Federal agencies (HUD / USDA Rural Development) screening counties for "
    "economic development grants. Counties where actual income falls well below the prediction "
    "may signal structural disadvantage worth investigating."
)
st.caption(
    "Data: 2024 U.S. Census Bureau ACS 5-Year Estimates — Economic Characteristics (DP03)."
)

st.subheader("Predicted Median Household Income")
col1, col2, col3 = st.columns(3)
col1.metric("Lower Bound", f"${lower:,.0f}",      help=f"Prediction − CV RMSE (±${cv_rmse:,.0f})")
col2.metric("Prediction",  f"${prediction:,.0f}")
col3.metric("Upper Bound", f"${upper:,.0f}",      help=f"Prediction + CV RMSE (±${cv_rmse:,.0f})")

st.caption(
    f"Uncertainty based on 5-fold CV RMSE of **${cv_rmse:,.0f}** (CV R² = 0.83). "
    "Reflects average model error on held-out counties, not a statistical confidence interval."
)

# ── Grant screening signal ────────────────────────────────────────────────────
st.divider()
st.subheader("Grant Screening Signal")
actual = st.number_input(
    "Enter county's actual ACS median income (optional):",
    min_value=0, max_value=250_000, value=0, step=1_000,
    help="If provided, compares actual to predicted to flag structural underperformance."
)
if actual > 0:
    gap     = prediction - actual
    pct_gap = gap / prediction * 100
    if gap > cv_rmse:
        st.error(
            f"**Flag for review:** Actual income (${actual:,.0f}) is **${gap:,.0f} "
            f"({pct_gap:.1f}%) below** the prediction — exceeds 1 CV RMSE. "
            "Possible structural underperformance relative to labor-market profile."
        )
    elif gap > 0:
        st.warning(
            f"Actual income (${actual:,.0f}) is ${gap:,.0f} below prediction "
            "but within the model's normal error range (< 1 CV RMSE)."
        )
    else:
        st.success(
            f"Actual income (${actual:,.0f}) meets or exceeds the prediction. "
            "No structural underperformance signal."
        )

# ── Feature importance chart ───────────────────────────────────────────────────
st.divider()
st.subheader("Feature Importances")
st.caption(
    ":orange[**Predictive, not causal.**] Shows which features the model relied on most — "
    "not whether changing a feature would change income."
)

imp_df = (
    pd.DataFrame({"Feature": feature_names, "Importance": model.feature_importances_})
    .sort_values("Importance")
)

fig, ax = plt.subplots(figsize=(8, 4.5))
colors = ["#d62728" if f == "pct_poverty" else "#4C72B0" for f in imp_df["Feature"]]
bars = ax.barh(imp_df["Feature"], imp_df["Importance"], color=colors)
ax.set_xlabel("Mean Decrease in Impurity (normalized)")
ax.set_title("Random Forest Feature Importances  —  Predictive, not causal", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
for bar, val in zip(bars, imp_df["Importance"]):
    ax.text(val + 0.003, bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}", va="center", fontsize=8)
fig.tight_layout()
st.pyplot(fig)

# ── collar_ratio detail ────────────────────────────────────────────────────────
if "collar_ratio" in feature_names:
    st.divider()
    with st.expander("collar_ratio — engineered feature"):
        cr = slider_vals["collar_ratio"]
        st.markdown(
            f"**collar\\_ratio** = (pct\\_mgmt + pct\\_sales) / (pct\\_construction + pct\\_production + 0.01)\n\n"
            f"Current value: **{cr:.3f}**  |  "
            f"Feature importance: **{model.feature_importances_[list(feature_names).index('collar_ratio')]:.3f}**\n\n"
            "Captures white-collar vs. blue-collar occupation share. "
            "The +0.01 offset prevents division by zero."
        )
