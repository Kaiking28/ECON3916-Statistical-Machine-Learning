# Lab 5: The Architecture of Bias

## Overview
An empirical investigation into the **Data Generating Process (DGP)** and the statistical pathologies that emerge when sampling mechanisms fail. This lab exposes the hidden architectures that create bias in machine learning pipelines—from simple random sampling variance to systematic covariate shift and survivorship bias.

## Tech Stack
- **Python 3.x**
- **pandas** - Data manipulation and analysis
- **numpy** - Random sampling and numerical operations
- **scipy** - Chi-Square statistical testing
- **scikit-learn** - Stratified sampling implementation
- **seaborn** - Titanic dataset

## Methodology

### 1. Simple Random Sampling (SRS) & Variance Demonstration
Manually simulated the classic "shuffle and split" approach on the Titanic dataset to expose its fundamental weakness:

```
Random Permutation → 80/20 Split → Bias Measurement (Delta)
```

**Key Insight:** Even with proper randomization, SRS produces **high sampling variance**. The train/test survival rates deviate significantly due to chance alone—a form of Monte Carlo noise that destabilizes model evaluation.

### 2. Stratified Sampling (Variance Reduction)
Implemented **stratified random sampling** using `sklearn.model_selection.train_test_split()` with the `stratify` parameter to enforce distributional constraints:

```python
train_test_split(df, stratify=df['pclass'], test_size=0.2)
```

**Outcome:** Eliminated **Covariate Shift** by guaranteeing identical class distributions (1st/2nd/3rd class passengers) across train and test sets. This reduces sampling variance and ensures the test set is a representative microcosm of the population.

### 3. Sample Ratio Mismatch (SRM) Forensic Audit
Conducted a statistical quality control audit using **Chi-Square tests** to detect engineering failures in A/B testing infrastructure:

```
H₀: Observed split ratio = Expected ratio (e.g., 50/50)
H₁: Systematic deviation detected (bot traffic, logging bugs)
```

**Application:** SRM detection is critical in production environments where silent data corruption can invalidate experimental results. A significant χ² statistic flags non-random assignment mechanisms.

---

## Theoretical Deep Dive: Survivorship Bias & The Ghost Data Problem

### The TechCrunch Unicorn Paradox

**Question:** Why does analyzing only successful Unicorn startups lead to Survivorship Bias, and what specific type of Ghost Data is needed to fix it using a Heckman Correction?

### The Bias Mechanism

When you scrape TechCrunch for Unicorn case studies, you're observing a **selected sample**—companies that survived multiple filters:

1. **Selection Filter 1:** Survived Series A, B, C funding rounds
2. **Selection Filter 2:** Achieved $1B+ valuation
3. **Selection Filter 3:** Received media coverage

This creates **Survivorship Bias** because your dataset is systematically missing the counterfactual: startups that failed at each stage. You're analyzing `P(Strategy | Unicorn)` when you actually need `P(Unicorn | Strategy)`.

**The Result:** Any pattern you find (e.g., "All unicorns pivoted twice!") is contaminated because you can't see the failures who also pivoted twice but died anyway.

### The Ghost Data Requirement

To apply a **Heckman Selection Correction**, you need two types of data:

#### 1. **Outcome Equation Data** (What you have)
- Features of successful unicorns: team size, funding amount, pivot count, etc.
- Outcome: Valuation, growth rate, exit multiple

#### 2. **Selection Equation Data** (The Ghost Data you're missing)
This is the critical piece:

- **The full population of startups that *entered* the race**, including those that:
  - Failed to raise Series A
  - Shut down after Series B
  - Became profitable small businesses (never sought unicorn status)
  - Exited via acquisition before $1B valuation

**Specifically, you need:**
```
Ghost Data = {
  startup_id,
  features_at_founding (team, market, tech),
  selection_indicator (1 = became observable unicorn, 0 = disappeared),
  exclusion_restriction (instrument that predicts selection but not outcome)
}
```

### The Heckman Two-Stage Solution

**Stage 1 (Selection Model):**  
Estimate `P(Observable as Unicorn | Founding Characteristics)` using a **probit model** on the *full population* (including ghosts):

```
Pr(Selected = 1) = Φ(Z₁γ)
```

Where Z₁ includes variables like: VC network density, founder geography, macro funding climate (instruments that affect *visibility* but not necessarily *success quality*).

**Stage 2 (Outcome Model):**  
Use the **Inverse Mills Ratio** (λ) from Stage 1 as a control variable when modeling outcomes *among observed unicorns*:

```
ln(Valuation) = Xβ + ρλ + ε
```

The λ term corrects for the fact that observed unicorns are a non-random sample—it adjusts for the correlation between selection and unobserved outcome determinants.

### The Brutal Truth

Without ghost data on failed startups, **no statistical technique can fully recover causal effects**. The Heckman correction requires you to model *why* companies become observable, which is impossible if you only have data on survivors. This is why industry "best practices" derived from unicorn case studies often fail catastrophically when applied to the broader startup ecosystem.

---

## Key Takeaways

1. **Sampling isn't neutral** - The mechanism by which data enters your pipeline determines what biases emerge
2. **Stratification beats randomization** - When you know the DGP structure, enforce it
3. **Selection creates ghost dimensions** - The most dangerous bias comes from data you *can't* see
4. **Trust, but verify** - Even in production systems, SRM audits are essential quality controls

## Files
- `lab5_bias_architecture.ipynb` - Full implementation and experiments
- `README.md` - This document

---

**Status:** Complete ✅  
**Author:** [Your Name]  
**Date:** February 2026
