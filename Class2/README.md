# Lab 2: The Illusion of Growth & The Composition Effect

## Objective

Built a Python pipeline to analyze wage stagnation using live Federal Reserve Economic Data (FRED) API. Demonstrated the "Money Illusion" between nominal and real wages, and corrected for the "Composition Effect"—a statistical bias that distorted 2020 wage data during the pandemic.

## Methodology

### Technical Stack
Python | fredapi | pandas | matplotlib

### Analysis Pipeline

**Real Wage Calculation**
- Fetched nominal wages (`AHETPI`) and CPI (`CPIAUCSL`) from FRED API
- Calculated inflation-adjusted wages: `Real Wage = (Nominal / CPI) × CPI_today`
- Generated 50+ year comparison (1964-present)

**Anomaly Detection**
- Identified suspicious spike in real wages during 2020
- Recognized potential composition bias in labor force data

**Composition Effect Correction**
- Fetched Employment Cost Index (`ECIWAG`) as composition-fixed measure
- Rebased both series to 2015 = 100 for direct comparison
- Isolated artificial components of 2020 wage increase

## Key Findings

### The Money Illusion (1964-Present)
Nominal wages increased dramatically over 50 years, but **real purchasing power remained flat**. Workers' paychecks grew in dollars but failed to keep pace with inflation.

### The Pandemic Paradox (2020)
The 2020 "wage boom" was a **statistical artifact, not genuine economic growth**:

- Standard wage metrics showed a sharp spike
- Employment Cost Index (controlling for composition) showed stable growth
- **Root cause**: Low-wage workers disproportionately left the labor force during lockdowns, artificially inflating average wages

The spike reflected *who was working* rather than *how much workers were paid*—demonstrating the dangers of misinterpreting aggregate statistics without understanding data composition.

## Impact

This project demonstrates critical principles in economic analysis: adjust for inflation, question anomalies, and understand data composition. The methodology provides a reproducible framework for detecting statistical biases in economic indicators.
