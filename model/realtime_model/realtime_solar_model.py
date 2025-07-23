# Real-time Solar GHI Prediction Model
import numpy as np
import pandas as pd
import joblib

# Load pre-trained model and scaler
xgb_model = joblib.load("model/realtime_model/xgboost_model_realtime.pkl")
scaler = joblib.load("model/realtime_model/scaler_realtime.pkl")

def predict_realtime_ghi(lat, lon, start_date, temperature, wind_speed):
    """
    Predict GHI for 30 days starting from the given date using real-time temperature and wind speed.
    Args:
        lat (float): Latitude
        lon (float): Longitude
        start_date (str): Start date in format 'YYYY-MM-DD'
        temperature (float): Current temperature
        wind_speed (float): Current wind speed
    Returns:
        tuple: (daily_predictions, monthly_total)
    """
    from datetime import datetime, timedelta
    # For inference, use typical/average values for other features
    # These values should be set based on your training data statistics
    # Here, we use reasonable defaults for demonstration
    avg_pw = 2.0
    avg_tau5 = 0.5
    avg_diff = 1.0
    pw_std = 0.5
    tau5_std = 0.1
    diff_std = 0.2

    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    month = start_dt.month
    inputs = []
    current_date = start_dt
    for day in range(30):
        day_variation = np.sin(2 * np.pi * day / 30) * 0.1
        temp_variation = temperature + day_variation * 2 + np.random.normal(0, 1)
        ws_variation = wind_speed + day_variation + np.random.normal(0, 0.5)
        pw_value = avg_pw + day_variation * pw_std * 0.2 + np.random.normal(0, pw_std * 0.3)
        tau5_value = avg_tau5 + np.random.normal(0, tau5_std * 0.3)
        diff_value = avg_diff + np.random.normal(0, diff_std * 0.3)
        inputs.append([
            lat, lon,
            current_date.month,
            current_date.day,
            temp_variation,
            ws_variation,
            pw_value,
            tau5_value,
            diff_value
        ])
        current_date += timedelta(days=1)
    input_df = pd.DataFrame(inputs, columns=["lat", "lon", "month", "day", "AT", "WS", "PW", "Tau5", "DIFF"])
    input_scaled = scaler.transform(input_df)
    predictions = xgb_model.predict(input_scaled)
    for i in range(len(predictions)):
        daily_factor = 1 + np.random.normal(0, 0.05)
        predictions[i] *= daily_factor
        predictions[i] = np.clip(predictions[i], 3.0, 7.0)
        if month in [4, 5, 6]:
            predictions[i] = min(predictions[i] * 1.1, 7.0)
        elif month in [11, 12, 1, 2]:
            predictions[i] = max(predictions[i] * 0.85, 3.0)
    return predictions.tolist(), float(sum(predictions)) 