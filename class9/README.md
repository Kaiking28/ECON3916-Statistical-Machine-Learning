## Recovering Experimental Truths via Propensity Score Matching

---

### Objective

To rehabilitate a corrupted observational estimate by modeling and neutralizing the selection mechanism that caused it — recovering a credible causal treatment effect without access to a randomized experiment.

---

### Methodology

- **Diagnosing the Observational Failure**
  Using the observational subset of the Lalonde (1986) dataset, a naive difference-in-means comparison was computed as the baseline. Because participation in job training was self-selected rather than randomly assigned, the raw estimate was contaminated by systematic differences between the treatment and control populations — producing a deeply misleading signal that will be corrected in subsequent steps.

- **Propensity Score Estimation**
  A logistic regression model was trained on eight pre-treatment covariates — age, education, race, marital status, degree attainment, and pre-program earnings in 1974 and 1975 — to estimate each individual's conditional probability of receiving treatment given their observed characteristics: P(treat = 1 | X). This propensity score compresses the high-dimensional confounder space into a single scalar, enabling like-for-like comparison across groups.

- **Nearest Neighbor Matching**
  With propensity scores assigned to all units, a 1:1 Nearest Neighbor matching algorithm was applied — implemented via Scikit-Learn — pairing each treated individual with the control unit whose estimated propensity score was closest in value. Matching was performed with replacement to minimize bias in a setting where the supply of high-quality control matches is limited. This procedure constructs a matched control pool that mirrors the treated population on all modeled confounders.

- **Balance Verification & Effect Estimation**
  Post-matching covariate balance was assessed using the Standardized Mean Difference (SMD) across all covariates, with a threshold of < 0.1 indicating acceptable balance. A two-sample T-test was then applied to the matched sample to estimate the Average Treatment Effect on the Treated (ATT).

---

### Key Findings

| Estimate | Value |
|---|---|
| Naive (Unmatched) Difference | −$15,204 |
| Recovered (Matched) Treatment Effect | ~+$1,800 |
| Direction Corrected? | ✅ Yes — sign fully reversed |

The naive observational estimate produced a treatment effect of **−$15,204**, suggesting that job training substantially *reduced* earnings — a conclusion that is not only economically implausible but directly contradicted by the experimental benchmark. After propensity score matching neutralized the selection mechanism, the recovered estimate converged to approximately **+$1,800**, closely aligning with the experimental ground truth established by Lalonde's original randomized trial.

The magnitude of the correction — nearly $17,000 — illustrates why raw observational comparisons in non-experimental labor data are not merely imprecise, but systematically misleading. Selection bias does not add noise to an otherwise valid estimate; it replaces the signal entirely.

---

*Dataset: Lalonde, R.J. (1986). "Evaluating the Econometric Evaluations of Training Programs with Experimental Data." American Economic Review.*
