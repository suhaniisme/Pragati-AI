import pandas as pd
import numpy as np
import joblib
import os

class PragatiMLEngine:
    def __init__(self, model_path="models/sales_model.pkl", data_path="data/merchant_data.csv"):
        self.model = joblib.load(model_path) if os.path.exists(model_path) else None
        self.df = pd.read_csv(data_path) if os.path.exists(data_path) else None

    def get_kpis(self):
        """Returns high-level business stats for the dashboard."""
        if self.df is None:
            return {
                "total_sales": 0,
                "avg_daily_sales": 0,
                "total_footfall": 0,
                "recent_7_days_revenue": 0
            }
        
        total_sales = round(self.df["total_revenue"].sum(), 2)
        avg_daily = round(self.df["total_revenue"].mean(), 2)
        total_footfall = int(self.df["footfall"].sum())
        recent_revenue = round(self.df.tail(7)["total_revenue"].sum(), 2)
        
        return {
            "total_sales": total_sales,
            "avg_daily_sales": avg_daily,
            "total_footfall": total_footfall,
            "recent_7_days_revenue": recent_revenue
        }

    def predict_next_7_days(self):
        """Predicts sales for the upcoming week based on synthetic patterns."""
        if self.model is None:
            return pd.DataFrame()

        future_dates = pd.date_range(start=pd.Timestamp.today(), periods=7, freq="D")
        predictions = []

        for date in future_dates:
            day_of_week = date.dayofweek
            is_weekend = 1 if day_of_week in [5, 6] else 0
            month = date.month
            est_footfall = np.random.randint(60, 160) + (40 if is_weekend else 0)
            qr_ratio = round(np.random.uniform(0.6, 0.95), 2)

            features = pd.DataFrame([{
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "month": month,
                "footfall": est_footfall,
                "qr_ratio": qr_ratio
            }])

            pred_rev = round(self.model.predict(features)[0], 2)
            predictions.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Day": date.strftime("%A"),
                "Predicted_Revenue": pred_rev
            })

        return pd.DataFrame(predictions)