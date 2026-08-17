# india_cpi_inflation_forecast
# India CPI Inflation Forecasting

## Problem Statement
Inflation trends directly affect RBI monetary policy, household budgeting, and business 
pricing decisions in India. This project analyzes historical Indian CPI data (2013-2023) 
to identify trends and seasonality, then forecasts CPI/inflation for the next 6 months.

## Data
- Source: Ministry of Statistics and Programme Implementation (MOSPI), Government of India
- Series: Consumer Price Index (General Index), Rural+Urban combined, base year 2012=100
- Period: January 2013 – May 2023 (124 months)

## Data Cleaning
- Corrected a typo in the raw source ("Marcrh" → "March")
- Identified 3 missing months: April 2019 (data gap in source), April & May 2020 
  (CPI data collection was suspended in India during COVID-19 lockdown)
- Imputed missing values using linear interpolation

## Methodology
1. Exploratory analysis: trend, YoY inflation rate, seasonal decomposition
2. Stationarity testing (ADF): raw series non-stationary (p=0.998); achieved 
   stationarity via first-order + seasonal differencing (p=0.0005)
3. Time-based train/test split (train: 2013-2022, test: last 12 months)
4. Models compared: Naive baseline, SARIMA (auto-tuned), Prophet

## Results

| Model   | MAE  | RMSE | MAPE  |
|---------|------|------|-------|
| Naive   | 4.35 | 4.71 | 2.46% |
| Prophet | 0.81 | 0.96 | 0.46% |
| SARIMA  | 0.65 | 0.87 | 0.37% |

**SARIMA(0,1,1)(0,1,1)[12]** was selected as the final model — it outperformed both 
the naive baseline (85% lower MAE) and Prophet on the held-out test set.

## Forecast
Using the full dataset, SARIMA forecasts CPI inflation holding in the 4.0-4.6% range 
for June-November 2023, indicating continued moderation from the 2022 inflation peak.

## Repo Structure

├── data/ # raw and cleaned CPI data
├── notebooks/ # analysis notebook
├── reports/ # saved plots
└── README.md


## Tools
Python, pandas, statsmodels, pmdarima, Prophet, matplotlib