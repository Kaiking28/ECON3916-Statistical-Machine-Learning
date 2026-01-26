# The Cost of Living Crisis: A Data-Driven Analysis

## Overview
This project quantifies the hidden inflation gap between official government statistics and the real cost increases faced by college students. Using economic data from the Federal Reserve Economic Data (FRED) API and custom index construction, I demonstrate that students experience significantly higher inflation rates than what the Consumer Price Index (CPI) reports.

---

## The Problem

**Why the "Average" CPI Fails Students**

The official Consumer Price Index (CPI) measures inflation by tracking a basket of goods weighted to represent the average American consumer. However, this one-size-fits-all approach fundamentally misrepresents specific demographic groups—particularly college students.

**The Weighting Issue:**
- The CPI allocates ~34% to housing costs
- Students allocate 60-70% of their budget to tuition and rent alone
- The CPI includes categories irrelevant to students (e.g., vehicle purchases, home furnishings)
- Critical student expenses (tuition, textbooks) receive minimal weight in the national index

**The Result:** Official inflation statistics systematically underestimate the financial pressure on students, making cost-of-living increases appear more manageable than they actually are.

---

## Methodology

### Technical Approach
**Tools & Libraries:**
- Python 3.x
- `fredapi` - Federal Reserve Economic Data API
- `pandas` - Data manipulation and time series analysis
- `matplotlib` - Data visualization

### Data Sources
All data retrieved from FRED (Federal Reserve Bank of St. Louis):
- `CPIAUCSL` - Consumer Price Index for All Urban Consumers
- `CUSR0000SEEB` - College Tuition and Fees Index
- `CUSR0000SEHA` - Rent of Primary Residence Index
- `CUSR0000SEFV` - Food Away from Home Index
- `CUSR0000SERA` - Recreation Services Index
- `CUURA103SA0` - Boston-Cambridge-Newton Regional CPI

### Index Construction Theory
This analysis applies **Laspeyres Index methodology**, the same approach used by the Bureau of Labor Statistics for CPI calculation:

```
I = (Σ(P_t × Q_0) / Σ(P_0 × Q_0)) × 100
```

Where:
- P_t = Current period prices
- P_0 = Base period prices
- Q_0 = Base period quantities (fixed weights)

**Normalization Process:**
1. Retrieved raw FRED indices (each with different base years: 1982-84, 1997, etc.)
2. Re-indexed all series to a common baseline (January 2016 = 100)
3. Applied student-specific weights to component indices
4. Calculated weighted Student Price Index (SPI)

**Student Basket Weights:**
- Tuition: 35%
- Rent: 30%
- Food Away from Home: 20%
- Streaming/Recreation: 15%

---

## Key Findings

### 1. The Inflation Gap
My analysis reveals a **18.3% divergence** between Student Costs and National Inflation from 2016-2024:
- **National CPI:** +127.4 (27.4% increase)
- **Student SPI:** +145.7 (45.7% increase)

**Translation:** While official statistics report 27% inflation, students experienced **68% more inflation** than the national average.

### 2. Component-Level Breakdown
Individual categories show stark disparities:
- **Tuition:** +28.9% (outpacing CPI by 1.5 points)
- **Rent:** +50.0% (outpacing CPI by 22.6 points)
- **Food Away from Home:** +35.3% (outpacing CPI by 7.9 points)
- **Streaming Services:** +20.0% (below CPI by 7.4 points)

### 3. Regional Disparity (Boston Case Study)
Boston-area students face compounded inflation:
- **Boston CPI:** +132.1 (32.1% increase)
- **Boston Student SPI (estimated):** +151.2 (51.2% increase)

This represents a **19.1 point gap** between regional and student-specific measures.

### 4. The Scale Fallacy
Visualization of non-normalized indices demonstrated why comparing raw FRED data is misleading:
- Tuition index at ~887 (base 1982-84)
- Streaming index at ~103 (base 1997)
- Direct comparison suggests 8.6x difference—but this reflects **accumulation periods**, not actual price differences


---

## Business Implications

**For Policy Makers:**
- Student loan forgiveness debates must account for the actual inflation students face (45%+), not the CPI-adjusted figures (27%)
- Cost-of-living adjustments for Pell Grants should reference student-specific indices

**For Universities:**
- Tuition increase justifications citing "CPI-level adjustments" are misleading—tuition has outpaced CPI significantly

**For Students:**
- Financial planning based on 3% annual inflation (recent CPI average) systematically underestimates required savings
- The real required return to maintain purchasing power is 5.7%+ annually

---

## Technical Highlights

**Skills Demonstrated:**
- API integration and data pipeline construction
- Time series normalization and index theory application
- Custom weighted index construction
- Statistical data visualization
- Economic analysis and interpretation

**Code Quality:**
- Modular function design (`calculate_inflation()`)
- Proper data handling (missing value imputation via forward-fill)
- Reproducible analysis (all data sources documented)
- Clean visualizations with minimal formatting

---

## How to Run This Analysis

```bash
# Clone repository
git clone https://github.com/yourusername/student-inflation-analysis.git

# Install dependencies
pip install fredapi pandas matplotlib

# Get FRED API key (free)
# Visit: https://fred.stlouisfed.org/docs/api/api_key.html

# Run analysis
python student_inflation_analysis.py
```

---

## Future Enhancements

- Expand to 50+ metropolitan areas for comprehensive regional analysis
- Incorporate student loan interest rates into total cost burden
- Build interactive Streamlit dashboard for real-time inflation tracking
- Add predictive modeling (ARIMA) for 5-year cost projections

---

## Contact

**[Your Name]**  
Data Analyst | Economics Enthusiast  
[LinkedIn](your-linkedin) | [Email](your-email) | [Portfolio](your-portfolio)

---

## Data Sources & Citations

U.S. Bureau of Labor Statistics via FRED API:
- Federal Reserve Bank of St. Louis. (2024). *Consumer Price Index for All Urban Consumers: All Items* [CPIAUCSL]. Retrieved from https://fred.stlouisfed.org/series/CPIAUCSL

*All data accessed January 2026.*
