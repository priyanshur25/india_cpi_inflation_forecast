"""Model training and evaluation utilities for India CPI forecasting project."""
import numpy as np
import pandas as pd
import pmdarima as pm
from sklearn.metrics import mean_absolute_error, mean_squared_error


def time_based_split(series: pd.Series, test_months: int = 12):
    """Split a time series into train/test, keeping the last `test_months` as test."""
    train = series[:-test_months]
    test = series[-test_months:]
    return train, test


def naive_forecast(train: pd.Series, n_periods: int) -> np.ndarray:
    """Baseline: repeat the last known training value for every future period."""
    return np.full(n_periods, train.iloc[-1])


def fit_sarima(train: pd.Series, seasonal_period: int = 12, d: int = 1, D: int = 1):
    """Fit a SARIMA model using auto_arima to find the best (p,q)(P,Q)."""
    model = pm.auto_arima(
        train, seasonal=True, m=seasonal_period, d=d, D=D,
        suppress_warnings=True, stepwise=True, trace=False
    )
    return model


def evaluate_forecast(actual: pd.Series, predicted: np.ndarray) -> dict:
    """Compute MAE, RMSE, MAPE for a forecast against actuals."""
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual.values - predicted) / actual.values)) * 100
    return {'MAE': round(mae, 2), 'RMSE': round(rmse, 2), 'MAPE': round(mape, 2)}