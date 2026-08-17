from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "bank_marketing_pipeline.joblib"

FEATURES = [
    "age",
    "job",
    "marital",
    "education",
    "balance",
    "housing",
    "loan",
    "campaign",
]

# El modelo se carga una vez cuando inicia la API.
model = joblib.load(MODEL_PATH)


def make_prediction(client_data):
    data_frame = pd.DataFrame([client_data], columns=FEATURES)

    prediction = model.predict(data_frame)[0]
    yes_position = list(model.classes_).index("yes")
    probability = model.predict_proba(data_frame)[0][yes_position]

    if prediction == "yes":
        classification = "Potencialmente interesado"
    else:
        classification = "Baja propensión"

    return {
        "prediction": prediction,
        "probability": round(float(probability), 4),
        "classification": classification,
    }

