Lab 5: The Architecture of Bias
Overview
This lab conducts a systematic forensic investigation into Data Generating Processes (DGP) and Sampling Bias in machine learning pipelines. Using the Titanic dataset as a pedagogical sandbox, I demonstrate how seemingly innocuous sampling decisions introduce measurable statistical bias that compromises model generalization.
Technical Implementation
Tech Stack

Python 3.x
pandas & numpy: Data manipulation and simulation
scipy.stats: Chi-Square goodness-of-fit testing
sklearn.model_selection: Stratified sampling implementation
seaborn: Dataset provisioning

Methodology
1. Simple Random Sampling (SRS) — The Variance Problem
Objective: Quantify sampling error under naive randomization.

Manually shuffled the Titanic population using np.random.permutation()
Applied an 80/20 train-test split on shuffled indices
Result: Computed the delta (bias) between train/test survival rates to demonstrate high variance inherent to SRS when dealing with imbalanced outcomes

pythondelta = |train_survival_rate - test_survival_rate|
```

**Finding**: SRS produces non-identical distributions across splits, violating the i.i.d. assumption required for valid generalization bounds.

---

#### 2. Stratified Sampling — Eliminating Covariate Shift
**Objective**: Enforce distributional invariance across train/test partitions.

- Implemented `sklearn.train_test_split()` with `stratify=df['pclass']`
- Verified that passenger class proportions remained identical across splits
- **Result**: Eliminated *Covariate Shift* in the feature space, ensuring test set representativeness

**Why this matters**: Covariate Shift occurs when P(X) differs between train and test, causing models to fail on out-of-distribution data. Stratification is a hard constraint that preserves marginal distributions.

---

#### 3. Sample Ratio Mismatch (SRM) Detection — A/B Test Forensics
**Objective**: Detect engineering failures in experimental designs.

- Applied **Chi-Square goodness-of-fit tests** to A/B test traffic splits
- Tested null hypothesis: H₀: Observed ratios match expected design ratios
- **Result**: SRM detection flags data pipeline bugs (e.g., bot traffic, logging errors, bucketing failures) that invalidate causal inference

**Real-world impact**: Companies like Booking.com have documented cases where undetected SRM led to incorrect product decisions affecting millions of users.

---

## Theoretical Deep Dive: Survivorship Bias in Unicorn Startup Analysis

### The Question
*"Why does analyzing only successful Unicorn startups (on TechCrunch) lead to Survivorship Bias, and what specific type of Ghost Data would I need to fix it using a Heckman Correction?"*

### The Diagnosis

**Survivorship Bias** occurs when your dataset is *selection-conditioned* on an outcome of interest. TechCrunch articles about unicorns represent a **non-random sample** from the universe of all startups:
```
P(Observed | Unicorn Status = 1) ≠ P(All Startups)
```

**The Problem**: 
- You only observe startups that *survived* to reach $1B+ valuation
- The features you measure (founder pedigree, market timing, pivot strategy) are **post-hoc rationalizations**
- The true Data Generating Process includes thousands of failed startups with *identical early characteristics* that never made TechCrunch

**Classic Example**: "All successful founders dropped out of college" ← You never counted the thousands of dropouts running failed startups in obscurity.

---

### The Ghost Data You Need

To apply a **Heckman Correction** (the econometric solution to sample selection bias), you require:

#### 1. **The Censored Population** (Ghost Data Type 1)
- **All startups** that raised a seed round in the same cohort, not just unicorns
- This includes: Failed startups, lifestyle businesses, acqui-hires, zombie companies
- **Why**: You need the denominator to estimate P(Unicorn | Features)

#### 2. **The Selection Mechanism** (Ghost Data Type 2)
- Variables that predict *being observed* (appearing on TechCrunch) but don't directly cause unicorn status
- Examples:
  - Founder's social media follower count (drives media coverage)
  - Geographic proximity to tech journalists
  - PR budget expenditure
  - Participation in high-profile accelerators (YC, Techstars)

**Why this matters**: These are **exclusion restrictions** — variables correlated with selection but not with the outcome, conditional on other features.

---

### The Heckman Two-Step Procedure

**Step 1: Selection Equation** (Probit Model)
```
P(Observed on TechCrunch) = Φ(α₀ + α₁·Features + α₂·ExclusionRestrictions)
```
Estimate the *inverse Mills ratio* (λ) from this model.

**Step 2: Outcome Equation** (Corrected Regression)
```
P(Unicorn Status | Observed) = β₀ + β₁·Features + β₂·λ + ε
```
The λ term corrects for selection bias by modeling the unobserved correlation between "being in the sample" and "becoming a unicorn."

---

### The Verdict

Without the **ghost data** of failed startups and selection mechanism variables, any analysis of TechCrunch unicorns will:
1. Overestimate the causal effect of "success factors"
2. Ignore the base rate of failure (P(Unicorn) ≈ 0.001%)
3. Produce non-generalizable insights for aspiring founders

**Heckman Correction transforms the question** from:
- ❌ "What do unicorns have in common?" 
- ✅ "What predicts unicorn status *after controlling for the fact that we only observe survivors*?"

---

## Key Takeaways

1. **Sampling is not neutral** — Every data collection method encodes assumptions about the DGP
2. **Stratification is insurance** — It enforces distributional invariants that SRS cannot guarantee
3. **SRM detection is defensive engineering** — Chi-Square tests catch pipeline bugs before they corrupt experiments
4. **Selection bias is invisible** — Without the counterfactual (ghost data), you're fitting models to an illusion

---

## Repository Structure
```
lab5-architecture-of-bias/
├── notebook.ipynb          # Full implementation
├── data/
│   └── titanic.csv         # Dataset (loaded via seaborn)
├── figures/
│   ├── sampling_variance.png
│   └── stratified_comparison.png
└── README.md               # This file

References

Kohavi, R., et al. (2020). Online Controlled Experiments at Scale
Heckman, J. (1979). "Sample Selection Bias as a Specification Error"
Pearl, J. (2009). Causality: Models, Reasoning, and Inference
