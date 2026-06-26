import joblib
from sklearn.ensemble import IsolationForest
from src.hybrid_waf.utils.feature_extractor import extract_features

normal_requests = [
    "GET /home",
    "GET /products?id=1",
    "POST /login user=admin pass=1234",
    "GET /about",
]

X = [extract_features(r) for r in normal_requests]

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

joblib.dump(model, "waf_model.pkl")

print("Model trained successfully!")
