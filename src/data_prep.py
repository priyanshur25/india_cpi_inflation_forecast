"""Data loading and cleaning utilities for India CPI forecasting project."""
import pandas as pd

MONTH_MAP = {m: i+1 for i, m in enumerate([
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
])}

CATEGORY_COLS = [
    'Food and beverages', 'Housing', 'Fuel and light', 'Clothing and footwear',
    'Transport and communication', 'Health', 'Education', 'Miscellaneous', 'General index'
]

def load_raw(path: str) -> pd.DataFrame:
    """Load the raw MOSPI CPI CSV."""
    return pd.read_csv(path)

def clean_sector(df: pd.DataFrame, sector: str, cols: list[str] = None) -> pd.DataFrame:
    """
    Filter to a given sector (Rural / Urban / Rural+Urban), fix known data issues,
    build a proper date index, and return a clean continuous monthly time series.
    """
    if cols is None:
        cols = CATEGORY_COLS

    d = df[df['Sector'] == sector].copy()
    d['Month'] = d['Month'].replace('Marcrh', 'March')  # known typo in source data
    d['month_num'] = d['Month'].map(MONTH_MAP)
    d['date'] = pd.to_datetime(dict(year=d['Year'], month=d['month_num'], day=1))
    d = d.sort_values('date').reset_index(drop=True)

    result = d[['date'] + cols].copy()

    full_range = pd.date_range(result['date'].min(), result['date'].max(), freq='MS')
    result = result.set_index('date').reindex(full_range).rename_axis('date').reset_index()

    for col in cols:
        result[col] = pd.to_numeric(result[col], errors='coerce')
        result[col] = result[col].interpolate(method='linear')

    return result

def calc_yoy_inflation(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Calculate year-over-year % change for given columns."""
    result = df[['date']].copy()
    for col in cols:
        result[col] = df[col].pct_change(12) * 100
    return result.dropna().reset_index(drop=True)