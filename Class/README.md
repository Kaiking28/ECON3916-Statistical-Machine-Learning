# Global Purchasing Power Parity Analysis via the Big Mac Index

## Objective
This project applies the Big Mac Index methodology to empirically test the **Law of One Price** and assess currency valuation across 19 countries relative to the US Dollar, using purchasing power parity (PPP) as the theoretical framework.

## Methodology

* **Data Ingestion**: Manually constructed a structured dataset from The Economist's January 2015 Big Mac Index, capturing local prices, exchange rates, and geographic identifiers across major economies
* **PPP Calculation**: Computed the implied purchasing power parity exchange rate for each currency by normalizing local Big Mac prices against the US benchmark price
* **Valuation Analysis**: Quantified currency misalignment by comparing implied PPP rates to actual market exchange rates, expressed as percentage deviation
* **Visualization**: Generated horizontal bar charts to illustrate the spectrum of currency over/undervaluation, with negative values indicating undervaluation and positive values indicating overvaluation

## Key Findings

Based on January 2015 data, the analysis revealed significant currency misalignments:

* **Most Overvalued**: The Norwegian Krone (NOK) exhibited the strongest overvaluation at approximately **+31.5%** relative to PPP, suggesting the Big Mac was substantially more expensive in Norway than fundamental purchasing power would predict
* **Most Undervalued**: The Russian Ruble (RUB) showed severe undervaluation at approximately **-71.6%**, reflecting currency depreciation and potential arbitrage opportunities
* **Near Fair Value**: The Euro area currencies (EUR) and Australian Dollar (AUD) traded close to their implied PPP values, indicating relative equilibrium
* **Emerging Market Pattern**: Most emerging market currencies (China, Indonesia, Egypt, South Africa) demonstrated undervaluation ranging from -40% to -55%, consistent with the Balassa-Samuelson effect

## Economic Interpretation

The results support the view that the Law of One Price holds imperfectly in the short run due to trade barriers, non-tradable components (labor, rent), and market frictions. Currency deviations from PPP may signal future exchange rate adjustments, though market forces, capital flows, and monetary policy can sustain misalignments for extended periods.

---

**Tools Used**: Python, Pandas, Matplotlib, Seaborn  
**Data Source**: The Economist Big Mac Index (January 2015)
