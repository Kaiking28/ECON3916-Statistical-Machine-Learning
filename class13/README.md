# The Architecture of Dimensionality: Hedonic Pricing & the FWL Theorem

## Objective
Estimate a multivariate hedonic pricing model on 2026 California real estate data and furnish a step-by-step algebraic proof of the Frisch-Waugh-Lovell (FWL) theorem, demonstrating how OLS mechanically achieves *ceteris paribus* isolation in the presence of correlated confounders.

---

## Methodology

- **Baseline Bivariate Regression** — Estimated a naive OLS model regressing `Sale_Price` solely on `Property_Age` to establish a contaminated benchmark coefficient, deliberately omitting the confounding location variable.

- **Multivariate Expansion** — Introduced `Distance_to_Tech_Hub` as a second regressor, forcing the hyperplane to partition explained variance across both dimensions simultaneously and absorb the location signal that the bivariate model could not distinguish.

- **FWL Residual Partialling (Step 1 of 3)** — Regressed `Sale_Price` on `Distance_to_Tech_Hub` and extracted the orthogonal residuals, isolating the component of price that is *linearly independent* of proximity to tech employment centers.

- **FWL Residual Partialling (Step 2 of 3)** — Regressed `Property_Age` on `Distance_to_Tech_Hub` and extracted its residuals, purging the shared covariance between age and location from the feature of interest.

- **Residuals-on-Residuals Regression (Step 3 of 3)** — Regressed price residuals strictly on age residuals with no intercept term, recovering the pure, unconfounded coefficient for `Property_Age` from the stripped signal alone.

- **Epistemological Proof** — Confirmed that the FWL-isolated coefficient matches the multivariate OLS coefficient to machine precision (Δ ≈ 9.55 × 10⁻¹²), providing an exact algebraic verification of the theorem.

**Stack:** Python 3.10+ · pandas · statsmodels.formula.api · matplotlib

---

## Key Findings

The 2026 California dataset exposed a textbook case of **Omitted Variable Bias (OVB)** driven by a strong negative correlation between `Property_Age` and `Distance_to_Tech_Hub` (r = −0.937). Older housing stock is disproportionately concentrated near legacy coastal tech corridors — San Francisco and San Jose — while newer developments have been pushed further inland. A naive algorithm blind to this geographic reality cannot decompose the two signals and is forced to conflate them.

The consequences were severe and directionally misleading:

| Model | `Property_Age` Coefficient | Implication |
|---|---|---|
| Naive Bivariate | **+$5,574 / year** | Aging *increases* home value — economically incoherent |
| Multivariate OLS | **−$2,063 / year** | Aging *decreases* home value — directionally correct |
| FWL Proof | **−$2,063 / year** | Exact match — theorem verified |

The naive model **stole $7,637/year** in pricing signal from the distance variable and misattributed it to physical age, producing a coefficient that was not merely imprecise but *inverted in sign* — a mispricing scenario that would systematically overpay for old properties near tech hubs and underprice new construction further from them.

The FWL proof confirms that multivariate OLS does not simply "add variables." It executes a precise orthogonal decomposition: each coefficient in a multivariate model is algebraically equivalent to a bivariate regression run entirely on residuals that have been scrubbed of every other regressor's influence. The algorithm achieves *ceteris paribus* not as a philosophical assumption, but as a provable geometric operation — projecting each feature onto the subspace orthogonal to all confounders before estimating its marginal effect.
