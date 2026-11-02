import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib
import os

print("Generating high-dimensional Paytm merchant dataset...")

np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=365, freq="D")

data = []
for date in dates:
    day_of_week = date.dayofweek
    is_weekend = 1 if day_of_week in [5, 6] else 0
    month = date.month
    
    footfall = np.random.randint(40, 180) + (40 if is_weekend else 0)
    avg_ticket = np.random.uniform(90, 300)
    revenue = round(footfall * avg_ticket, 2)
    qr_payments_ratio = round(np.random.uniform(0.6, 0.95), 2)
    inventory_health = np.random.randint(50, 100)
    
    data.append({
        "date": date.strftime("%Y-%m-%d"),
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "month": month,
        "footfall": footfall,
        "avg_ticket": round(avg_ticket, 2),
        "qr_ratio": qr_payments_ratio,
        "inventory_health": inventory_health,
        "total_revenue": revenue
    })

df = pd.DataFrame(data)
os.makedirs("data", exist_ok=True)
df.to_csv("data/merchant_data.csv", index=False)

# Train Revenue Predictor
X = df[["day_of_week", "is_weekend", "month", "footfall", "qr_ratio"]]
y = df["total_revenue"]
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/sales_model.pkl")
print("✅ Advanced ML Models trained & saved successfully!")