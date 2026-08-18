# 🇮🇳 India CPI Inflation Forecasting

**Live Dashboard → https://indiacpiinflationforecast-hcpcldy6vd9xajbkfax5lw.streamlit.app/**

Forecasting India's Consumer Price Index using SARIMA time series modeling on 
10 years of official government data, with a breakdown of what's actually driving 
inflation trends.

**[Forecast Chart]**
<img width="704" height="340" alt="cpi_main_forecast" src="https://github.com/user-attachments/assets/ad67b7a4-4a6a-494a-9230-b9575f0f6d3d" />


## Problem Statement
Inflation trends directly affect RBI monetary policy, household budgeting, and 
business pricing decisions in India. This project analyzes historical CPI data 
(2013–2023) to identify trends and seasonality, forecasts CPI/inflation for the 
next 6 months, and investigates which spending categories are driving inflation.

## Key Findings
- **SARIMA(0,1,1)(0,1,1)[12]** forecasts CPI inflation holding in the 4.0–4.6% 
  range for June–November 2023, indicating continued moderation from the 2022 peak
- **Fuel & Light** drove the 2022 inflation spike (peaked 11.76% YoY, July 2022), 
  followed by Transport (10.91%, April 2022) — consistent with the global energy 
  price shock following Russia's invasion of Ukraine
- Food inflation followed with a lag, peaking later (8.41%, September 2022)
- **Rural India experienced higher inflation than urban India** through early 2023 
  (6.85% vs 6.0% in Jan 2023), likely due to rural households' heavier food-basket 
  weighting — the gap narrowed by mid-2023

**[Category Breakdown]**
<img width="716" height="389" alt="dashboard_categories" src="https://github.com/user-attachments/assets/468fd19e-8f8d-4804-bbeb-e02340cc7cab" />


## Data
- **Source:** Ministry of Statistics and Programme Implementation (MOSPI), 
  Government of India
- **Series:** Consumer Price Index (General Index), Rural / Urban / Combined, 
  base year 2012=100
- **Period:** January 2013 – May 2023 (124 months)

### Data Quality Issues Found & Handled
- Corrected a typo in the raw source (`"Marcrh"` → `"March"`)
- Identified 3 missing months: April 2019 (data gap in source), April & May 2020 
  (CPI data collection was suspended in India during COVID-19 lockdown)
- Imputed missing values using linear interpolation; flagged imputed points 
  separately for transparency

## Methodology
1. **EDA:** trend analysis, YoY inflation rate, seasonal decomposition
2. **Stationarity testing (ADF):** raw series non-stationary (p=0.998); achieved 
   stationarity via first-order + seasonal differencing (p=0.0005), informing the 
   SARIMA(p,1,q)(P,1,Q,12) parameter search
3. **Time-based train/test split** (train: 2013–2022, test: last 12 months) — 
   not random, to simulate genuine forecasting conditions
4. **Models compared:** Naive baseline, SARIMA (auto-tuned via `pmdarima`), Prophet

## Results

| Model   | MAE  | RMSE | MAPE  |
|---------|------|------|-------|
| Naive   | 4.35 | 4.71 | 2.46% |
| Prophet | 0.81 | 0.96 | 0.46% |
| SARIMA  | 0.65 | 0.87 | 0.37% |

SARIMA reduced forecast error by 85% versus the naive baseline and outperformed 
Prophet on the held-out test set.

## Dashboard
An interactive Streamlit app lets you explore the forecast at different horizons, 
compare rural vs urban trends, and toggle category-level inflation breakdowns.

**[Try it live →](https://indiacpiinflationforecast-hcpcldy6vd9xajbkfax5lw.streamlit.app/)**

## Repo Structure

├── app/ # Streamlit dashboard
├── data/ # raw and cleaned CPI data
├── notebooks/ # exploratory analysis
├── src/ # reusable data cleaning & modeling functions
├── reports/ # saved plots
└── README.md


## Tools
Python · pandas · statsmodels · pmdarima · Prophet · scikit-learn · Streamlit

## Author
Priyanshu Raj 
