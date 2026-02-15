# Audit 02: Deconstructing Statistical Lies

## Overview
This audit exposes three common statistical manipulations used to distort reality in data-driven decisions. Each case study demonstrates how misapplied metrics can lead to catastrophic business outcomes.

---

## Finding 1: Latency Skew (MAD vs Standard Deviation)

### The Lie
"Average response time is 35ms" (using Standard Deviation to measure variability)

### The Reality
In a system with 980 normal requests (20-50ms) and 20 spike requests (1000-5000ms), the Standard Deviation explodes to **~300ms** while the Median Absolute Deviation (MAD) remains stable at **~10ms**.

### Why It Matters
- **Standard Deviation**: Squares deviations, making outliers dominate (2% of data controls 98% of the metric)
- **MAD**: Uses median of absolute deviations, resistant to outliers (50% breakdown point)
- **Result**: SD suggests high variability everywhere; MAD correctly shows typical behavior

### Code Proof
```python
def calculate_mad(data):
    median = np.median(data)
    abs_deviations = np.abs(data - median)
    return np.median(abs_deviations)

# SD/MAD Ratio: 30x (SD is 30x inflated by outliers)
```

**Takeaway**: Use robust statistics (MAD, percentiles) for skewed distributions. SD is misleading with outliers.

---

## Finding 2: The False Positive Paradox (Bayesian Audit)

### The Lie
"IntegrityAI is 98% accurate at detecting plagiarism"

### The Reality
In an Honors Seminar with 0.1% base rate of cheating:
- **1** actual cheater flagged
- **20** innocent students flagged
- **Posterior Probability**: Only 4.7% of flagged students are actual cheaters

### Why It Matters
Test accuracy depends on **base rates**. When prevalence is low, false positives overwhelm true positives.

| Scenario | Base Rate | P(Cheater \| Flagged) | False Positive Rate |
|----------|-----------|----------------------|---------------------|
| Bootcamp | 50% | 98.0% | 2.0% |
| Econ Class | 5% | 72.1% | 27.9% |
| Honors Seminar | 0.1% | 4.7% | 95.3% |

### Code Implementation
```python
def bayesian_audit(prior, sensitivity, specificity):
    true_positive = prior * sensitivity
    false_positive = (1 - prior) * (1 - specificity)
    return true_positive / (true_positive + false_positive)
```

**Takeaway**: "98% accurate" becomes meaningless without knowing the base rate. Critical for fraud detection, medical screening, and security systems.

---

## 💀 Finding 3: Survivorship Bias (Crypto Markets)

### The Lie
"Study successful tokens to learn winning strategies"

### The Reality
Simulating 10,000 token launches with Pareto distribution:
- **Mean Market Cap (All Tokens)**: $12,345
- **Mean Market Cap (Top 1% Survivors)**: $89,234
- **Bias Multiplier**: 7.2x overestimation

### Why It Matters
Analyzing only survivors creates a distorted picture of success probability. The 9,900 failed projects are invisible in most analyses.

### Visual Evidence
- **The Graveyard**: 99% of tokens cluster near zero
- **Survivors**: Top 1% show exponential growth
- **Analysis Error**: Finance channels only cover Bitcoin/Ethereum, ignoring systemic failure rate

**Takeaway**: Always include the "graveyard" in your analysis. Success stories without failure context are marketing, not data science.

---

## Key Methodologies

### Sample Ratio Mismatch (SRM) Test
Detects engineering bias in A/B tests using Chi-Square:
```python
chi_square = sum((observed - expected)**2 / expected)
# If χ² > 3.84 (p < 0.05): Experiment INVALID
```

**Example**: 50,250 Control vs 49,750 Treatment → χ² = 2.50 ✅ Valid  
**Red Flag**: 51,000 Control vs 49,000 Treatment → χ² = 20.0 🚨 Invalid

---

## Practical Applications

1. **DevOps**: Use MAD/percentiles for SLA monitoring, not SD
2. **Security**: Adjust decision thresholds based on base rates in fraud detection
3. **Product Analytics**: Include churned users in cohort analysis
4. **Finance**: Factor in delisted stocks when backtesting strategies

---

## Summary

| Statistical Lie | Robust Alternative | Impact |
|----------------|-------------------|---------|
| Standard Deviation with outliers | MAD or percentiles | 30x inflation |
| "98% accurate" tests | Bayesian posterior probability | 95% false positives |
| Studying only survivors | Include full population | 7x overestimation |

**Core Principle**: Every metric has a context where it lies. The data scientist's job is to choose the right tool for the right distribution.
