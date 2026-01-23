from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# load model & features
model = joblib.load("key_risk_model.pkl")
feature_cols = joblib.load("feature_cols.pkl")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    try:
        df = pd.DataFrame(payload["rows"])

        print("Incoming columns:", df.columns.tolist())
        print("Expected features:", feature_cols)

        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0

        X = df[feature_cols].fillna(0)

        print("Final X dtypes:", X.dtypes)

        probs = model.predict_proba(X)[:, 1]
        df["risk_probability"] = probs

        return df[["userId", "char", "risk_probability"]].to_dict(
            orient="records"
        )

    except Exception as e:
        print("PREDICT ERROR:", str(e))
        raise e
