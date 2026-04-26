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

# ACS national medians and std devs from df.describe() (3,220 counties)
ACS_STATS = {
    "labor_force_pct":   dict(median=58.7, std=7.8,  min=20.0, max=87.0, default=58.7),
    "unemployment_rate": dict(median=4.5,  std=2.7,  min=0.0,  max=29.0, default=4.5),
    "mean_commute_min":  dict(median=24.2, std=5.7,  min=4.0,  max=50.0, default=24.2),
    "pct_mgmt":          dict(median=34.6, std=7.4,  min=6.0,  max=75.0, default=34.6),
    "pct_service":       dict(median=16.6, std=3.8,  min=0.0,  max=42.0, default=16.6),
    "pct_sales":         dict(median=19.2, std=3.1,  min=2.0,  max=36.0, default=19.2),
    "pct_construction":  dict(median=11.7, std=4.1,  min=1.0,  max=39.0, default=11.7),
    "pct_production":    dict(median=15.9, std=5.7,  min=0.0,  max=46.0, default=15.9),
    "pct_insured":       dict(median=92.3, std=4.9,  min=55.0, max=100.0,default=92.3),
    "pct_poverty":       dict(median=9.2,  std=7.1,  min=0.0,  max=63.0, default=9.2),
}

LABELS = {
    "labor_force_pct":   "Labor Force Participation (%)",
    "unemployment_rate": "Unemployment Rate (%)",
    "mean_commute_min":  "Mean Commute Time (min)",
    "pct_mgmt":          "Management / Professional Occ. (%)",
    "pct_service":       "Service Occupations (%)",
    "pct_sales":         "Sales & Office Occupations (%)",
    "pct_construction":  "Construction & Extraction Occ. (%)",
    "pct_production":    "Production & Transport Occ. (%)",
    "pct_insured":       "Health Insurance Coverage (%)",
    "pct_poverty":       "Population Below Poverty Line (%)",
    "collar_ratio":      "Collar Ratio (engineered)",
}

# ── Sidebar sliders ───────────────────────────────────────────────────────────
st.sidebar.header("County Characteristics")
st.sidebar.caption("2024 ACS 5-Year Estimates — 3,220 U.S. counties.")

slider_vals = {}
for feat in feature_names:
    if feat in ACS_STATS:
        s = ACS_STATS[feat]
        slider_vals[feat] = st.sidebar.slider(
            LABELS[feat], min_value=s["min"], max_value=s["max"],
            value=s["default"], step=0.1
        )

# Engineered feature computed from sliders before prediction
if "collar_ratio" in feature_names:
    slider_vals["collar_ratio"] = (
        (slider_vals["pct_mgmt"] + slider_vals["pct_sales"])
        / (slider_vals["pct_construction"] + slider_vals["pct_production"] + 0.01)
    )

# Build input in exact feature_names order
input_df = pd.DataFrame([[slider_vals[f] for f in feature_names]], columns=feature_names)

# ── Prediction ────────────────────────────────────────────────────────────────
prediction = float(model.predict(input_df)[0])
lower      = max(prediction - cv_rmse, 0)
upper      = prediction + cv_rmse

# ── Header ────────────────────────────────────────────────────────────────────
st.title("U.S. County Median Household Income Predictor")
st.markdown(
    "**Use case:** Federal agencies (HUD / USDA Rural Development) screening counties for "
    "economic development grants. Counties whose actual income falls well below the model's "
    "prediction may signal structural disadvantage beyond what their labor-market profile explains."
)
st.caption(
    "Data: 2024 U.S. Census Bureau ACS 5-Year Estimates — Economic Characteristics (DP03)."
)

# ── Prediction metrics ────────────────────────────────────────────────────────
st.subheader("Predicted Median Household Income")
col1, col2, col3 = st.columns(3)
col1.metric("Lower Bound", f"${lower:,.0f}",      help=f"Prediction − CV RMSE (±${cv_rmse:,.0f})")
col2.metric("Prediction",  f"${prediction:,.0f}")
col3.metric("Upper Bound", f"${upper:,.0f}",      help=f"Prediction + CV RMSE (±${cv_rmse:,.0f})")
st.caption(
    f"Prediction interval based on 5-fold CV RMSE of **${cv_rmse:,.0f}** (CV R² = 0.83). "
    "Reflects average model error on held-out counties."
)

# ── Grant flag ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Grant Screening Signal")
actual = st.number_input(
    "Enter county's actual ACS median income (optional):",
    min_value=0, max_value=250_000, value=0, step=1_000,
)
if actual > 0:
    gap = prediction - actual
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

# ── Tabs for two charts ───────────────────────────────────────────────────────
st.divider()
tab1, tab3 = st.tabs(
    ["County Profile vs. National Median", "Feature Importances"]
)

# ── Tab 1: County Profile (INTERACTIVE — updates with every slider change) ────
with tab1:
    st.info("Make sure you select each county characteristic in the sidebar to see the visualization update.")
    st.markdown(
        "Each bar shows how far this county's inputs deviate from the **national ACS median**, "
        "measured in standard deviations. Move the sliders to see the profile update."
    )
    base_feats = [f for f in feature_names if f in ACS_STATS]
    z_scores   = [
        (slider_vals[f] - ACS_STATS[f]["median"]) / ACS_STATS[f]["std"]
        for f in base_feats
    ]
    labels_short = [LABELS[f] for f in base_feats]

    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    colors1 = ["#d62728" if z < 0 else "#2ca02c" for z in z_scores]
    ax1.barh(labels_short, z_scores, color=colors1)
    ax1.axvline(0, color="black", linewidth=0.8)
    ax1.set_xlabel("Standard Deviations from National Median")
    ax1.set_title("County Profile vs. National ACS Median  (updates with sliders)", fontsize=11)
    ax1.spines[["top", "right"]].set_visible(False)
    for i, z in enumerate(z_scores):
        ax1.text(z + (0.05 if z >= 0 else -0.05), i,
                 f"{z:+.2f}σ", va="center",
                 ha="left" if z >= 0 else "right", fontsize=8)
    fig1.tight_layout()
    st.pyplot(fig1)

# ── Tab 2: Feature Importances (static — from model.pkl) ─────────────────────
with tab3:
    st.caption(
        ":orange[**Predictive, not causal.**] Importance scores reflect which features the "
        "model relied on most during training — not whether changing a feature causes income to change."
    )
    imp_df = (
        pd.DataFrame({"Feature": [LABELS[f] for f in feature_names],
                      "Importance": model.feature_importances_})
        .sort_values("Importance")
    )
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    colors3 = ["#d62728" if "Poverty" in f else "#4C72B0" for f in imp_df["Feature"]]
    bars3 = ax3.barh(imp_df["Feature"], imp_df["Importance"], color=colors3)
    ax3.set_xlabel("Mean Decrease in Impurity (normalized)")
    ax3.set_title("Random Forest Feature Importances  —  Predictive, not causal", fontsize=11)
    ax3.spines[["top", "right"]].set_visible(False)
    for bar, val in zip(bars3, imp_df["Importance"]):
        ax3.text(val + 0.003, bar.get_y() + bar.get_height() / 2,
                 f"{val:.3f}", va="center", fontsize=8)
    fig3.tight_layout()
    st.pyplot(fig3)

# ── collar_ratio detail ────────────────────────────────────────────────────────
if "collar_ratio" in feature_names:
    st.divider()
    with st.expander("collar_ratio — engineered feature"):
        cr = slider_vals["collar_ratio"]
        idx = list(feature_names).index("collar_ratio")
        st.markdown(
            f"**collar\\_ratio** = (pct\\_mgmt + pct\\_sales) / (pct\\_construction + pct\\_production + 0.01)\n\n"
            f"Current value: **{cr:.3f}**  |  "
            f"Feature importance: **{model.feature_importances_[idx]:.3f}**\n\n"
            "Higher values indicate a workforce skewed toward white-collar occupations. "
            "The +0.01 offset prevents division by zero."
        )
