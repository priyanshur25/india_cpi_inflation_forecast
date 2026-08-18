"""India CPI Inflation Forecasting Dashboard."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_prep import load_raw, clean_sector, calc_yoy_inflation, CATEGORY_COLS
from train_models import time_based_split, naive_forecast, fit_sarima, evaluate_forecast

st.set_page_config(page_title="India CPI Inflation Forecast", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'india_cpi_raw.csv')

# --- Cached data loading & cleaning (reruns only if the underlying function/file changes) ---
@st.cache_data
def get_clean_data():
    raw = load_raw(DATA_PATH)
    combined = clean_sector(raw, 'Rural+Urban')
    rural = clean_sector(raw, 'Rural', cols=['General index'])
    urban = clean_sector(raw, 'Urban', cols=['General index'])
    return combined, rural, urban

@st.cache_resource
def get_sarima_model(_series):
    return fit_sarima(_series)

combined, rural, urban = get_clean_data()
cpi_indexed = combined.set_index('date')['General index']

# --- Sidebar controls ---
st.sidebar.title("Settings")
horizon = st.sidebar.selectbox("Forecast horizon (months)", [3, 6, 12], index=1)

# --- Header ---
st.title("🇮🇳 India CPI Inflation Forecast")
st.caption("Source: MOSPI (Ministry of Statistics), General Index, Rural+Urban Combined, Base 2012=100")

st.markdown("""
This dashboard forecasts India's CPI inflation using SARIMA time series modeling, 
trained on 10 years of official MOSPI data. It also breaks down which spending 
categories (food, fuel, housing, etc.) are driving inflation trends.
""")
# --- Section 1: Historical CPI + Forecast ---
st.header("CPI Forecast")

model = get_sarima_model(cpi_indexed)
forecast, conf_int = model.predict(n_periods=horizon, return_conf_int=True)
future_dates = pd.date_range(cpi_indexed.index[-1] + pd.DateOffset(months=1), periods=horizon, freq='MS')

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(cpi_indexed.index, cpi_indexed, label='Historical CPI', color='#2563eb')
ax.plot(future_dates, forecast, label=f'Forecast (next {horizon} months)',
        color='#dc2626', linestyle='--', marker='o')
ax.fill_between(future_dates, conf_int[:, 0], conf_int[:, 1], color='#dc2626', alpha=0.15, label='95% CI')
ax.legend()
ax.set_ylabel('CPI (Base 2012=100)')
ax.grid(alpha=0.3)
st.pyplot(fig)

# Show forecast table with implied inflation
last_year = cpi_indexed[-12:].values
implied_inflation = ((forecast - last_year[:horizon]) / last_year[:horizon]) * 100
forecast_table = pd.DataFrame({
    'Date': future_dates.strftime('%Y-%m'),
    'Forecast CPI': forecast.round(2),
    'Implied YoY Inflation (%)': implied_inflation.round(2)
})
st.dataframe(forecast_table, use_container_width=True)

# --- Section 2: Model comparison ---
st.header("Model Performance (on 2022-2023 held-out test data)")

train, test = time_based_split(cpi_indexed, test_months=12)
naive_preds = naive_forecast(train, len(test))
naive_metrics = evaluate_forecast(test, naive_preds)

test_model = get_sarima_model(train)
sarima_test_preds, _ = test_model.predict(n_periods=len(test), return_conf_int=True)
sarima_metrics = evaluate_forecast(test, sarima_test_preds)

comparison_df = pd.DataFrame([
    {'Model': 'Naive Baseline', **naive_metrics},
    {'Model': 'SARIMA', **sarima_metrics},
])
st.dataframe(comparison_df, use_container_width=True)
st.caption(f"SARIMA reduced MAE by {(1 - sarima_metrics['MAE']/naive_metrics['MAE'])*100:.0f}% vs the naive baseline.")

# --- Section 3: Rural vs Urban ---
st.header("Rural vs Urban Inflation")

rural_yoy = calc_yoy_inflation(rural, ['General index']).rename(columns={'General index': 'Rural'})
urban_yoy = calc_yoy_inflation(urban, ['General index']).rename(columns={'General index': 'Urban'})
sector_compare = rural_yoy.merge(urban_yoy, on='date')

fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.plot(sector_compare['date'], sector_compare['Rural'], label='Rural', color='#059669')
ax2.plot(sector_compare['date'], sector_compare['Urban'], label='Urban', color='#7c3aed')
ax2.axhline(0, color='gray', linewidth=0.6)
ax2.legend()
ax2.set_ylabel('YoY Inflation (%)')
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# --- Section 4: Category breakdown ---
st.header("Inflation by Category")

cat_clean = clean_sector(load_raw(DATA_PATH), 'Rural+Urban', cols=CATEGORY_COLS)
cat_yoy = calc_yoy_inflation(cat_clean, CATEGORY_COLS)

selected_categories = st.multiselect(
    "Select categories to display",
    [c for c in CATEGORY_COLS if c != 'General index'],
    default=['Food and beverages', 'Fuel and light', 'Transport and communication']
)

fig3, ax3 = plt.subplots(figsize=(12, 5))
for col in selected_categories:
    ax3.plot(cat_yoy['date'], cat_yoy[col], label=col, linewidth=1.5)
ax3.plot(cat_yoy['date'], cat_yoy['General index'], label='General Index', color='black', linestyle='--', linewidth=2)
ax3.axhline(0, color='gray', linewidth=0.6)
ax3.legend(fontsize=8)
ax3.set_ylabel('YoY Inflation (%)')
ax3.grid(alpha=0.3)
st.pyplot(fig3)

st.markdown("---")
st.caption("Built by [Your Name] | Data: MOSPI, Government of India | Model: SARIMA(0,1,1)(0,1,1)[12]")