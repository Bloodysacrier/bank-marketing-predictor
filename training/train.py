from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "bank.csv"
MODEL_PATH = BASE_DIR / "models" / "bank_marketing_pipeline.joblib"
METRICS_PATH = BASE_DIR / "models" / "metrics.json"

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

NUMERIC_COLUMNS = ["age", "balance", "campaign"]
CATEGORICAL_COLUMNS = ["job", "marital", "education", "housing", "loan"]


def main():
    # El archivo usa punto y coma como separador.
    data = pd.read_csv(DATA_PATH, sep=";")

    x = data[FEATURES]
    y = data["y"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocessing = ColumnTransformer(
        [
            ("numeric", StandardScaler(), NUMERIC_COLUMNS),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLUMNS,
            ),
        ]
    )

    pipeline = Pipeline(
        [
            ("preprocessing", preprocessing),
            (
                "model",
                LogisticRegression(max_iter=1000, class_weight="balanced"),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, pos_label="yes"),
        "recall": recall_score(y_test, predictions, pos_label="yes"),
        "f1_score": f1_score(y_test, predictions, pos_label="yes"),
    }

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    with open(METRICS_PATH, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print("Modelo guardado en:", MODEL_PATH)
    print("Accuracy:", round(metrics["accuracy"], 4))
    print("Precision:", round(metrics["precision"], 4))
    print("Recall:", round(metrics["recall"], 4))
    print("F1-score:", round(metrics["f1_score"], 4))


if __name__ == "__main__":
    main()

