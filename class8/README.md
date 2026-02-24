## Hypothesis Testing & Causal Evidence Architecture
### *The Epistemology of Falsification: Adjudicating Causality on the Lalonde Dataset*

---

### Objective

Most applied data science workflows stop at **estimation** — producing a number and calling it insight. This project takes a deliberate step further, pivoting from estimation to **falsification**: the rigorous, philosophically grounded practice of trying to *break* your own findings before anyone else does.

Using the seminal Lalonde (1986) dataset — a canonical benchmark in causal inference — this lab operationalizes the scientific method as a decision-making framework. The central question is not merely *"What is the effect of job training on earnings?"* but rather *"Under what evidentiary standard are we justified in believing that effect is real?"* The answer lies in structured hypothesis testing architecture, where every claim must survive an explicit attempt at contradiction before it earns the right to influence a decision.

---

### Technical Approach

- **Parametric Inference via Welch's T-Test (SciPy `stats.ttest_ind`)**
  Estimated the **Average Treatment Effect (ATE)** of job-training program participation on real earnings by framing the comparison as a signal-to-noise problem. Welch's formulation was selected over Student's T-Test to relax the assumption of equal population variances between the treatment and control groups — a critical methodological choice given the heterogeneous nature of labor market outcomes. The resulting test statistic quantifies how many standard errors separate the observed lift from a world in which the treatment has no effect whatsoever.

- **Non-Parametric Validation via Permutation Test (SciPy `stats.permutation_test`, 10,000 resamples)**
  Earnings distributions in observational labor data are notoriously right-skewed and heavy-tailed — conditions under which parametric assumptions degrade. To stress-test the parametric result, a permutation test was conducted by repeatedly shuffling treatment labels across the observed pool and recomputing the ATE under each randomization. This empirically constructs the null distribution *from the data itself*, bypassing distributional assumptions entirely. Convergence across both methods materially strengthens the evidentiary claim.

- **Type I Error Control**
  The analysis was conducted under a pre-specified significance threshold (α = 0.05), enforced *before* observing results to guard against the most corrosive failure mode in applied statistics: selecting your threshold post-hoc to manufacture significance. This is not a procedural formality — it is the line between science and storytelling.

---

### Key Finding

The analysis identified a **statistically significant lift in real earnings of approximately $1,795** attributable to job-training participation. The null hypothesis — that the program produced zero effect on earnings — was **rejected via Proof by Statistical Contradiction**: the observed treatment effect is sufficiently improbable under the null distribution that chance-alone cannot serve as a credible explanation. This conclusion holds under both parametric and non-parametric testing regimes, lending the result methodological robustness that a single test approach cannot provide.

---

### Business Insight: Hypothesis Testing as the Safety Valve of the Algorithmic Economy

In production data science environments, the pressure to find signal is relentless. Dashboards need narratives. Stakeholders need numbers. Models need to justify their infrastructure costs. This creates a systematic incentive toward **data dredging** — the practice, often unconscious, of interrogating a dataset across enough dimensions that a spurious correlation eventually surfaces and gets promoted to a finding.

The consequences are not academic. Spurious correlations embedded in decision systems compound. A hiring algorithm trained on a noise artifact doesn't just make one bad decision — it makes that same bad decision at scale, millions of times, with institutional confidence behind it. A pricing model built on a confounded signal doesn't just misforecast once — it systematically misallocates resources until something expensive enough breaks to force a reexamination.

**Rigorous hypothesis testing is the safety valve that prevents this failure mode.** By forcing the analyst to commit to a falsifiable claim, specify a rejection threshold, and expose that claim to the most adversarial statistical environment possible, the framework creates accountability that ad-hoc "exploratory" analysis simply cannot provide. The permutation test, in particular, embodies this philosophy: it doesn't ask *"is my result big?"* — it asks *"how often would I see a result this big in a world where nothing is actually happening?"* That is the right question. It is also, frequently, the uncomfortable one.

In an economy where algorithmic decisions touch credit, employment, healthcare, and beyond, the willingness to ask that uncomfortable question — and to build the tooling to answer it honestly — is not a methodological nicety. It is a professional obligation.

---

*Dataset: Lalonde, R.J. (1986). "Evaluating the Econometric Evaluations of Training Programs with Experimental Data." American Economic Review.*
