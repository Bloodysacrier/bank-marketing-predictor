import joblib
import pandas as pd


def test_dataset_has_the_needed_columns():
    data = pd.read_csv("data/bank.csv", sep=";")
    columns = [
        "age",
        "job",
        "marital",
        "education",
        "balance",
        "housing",
        "loan",
        "campaign",
        "y",
    ]

    assert all(column in data.columns for column in columns)


def test_saved_model_can_be_loaded():
    model = joblib.load("models/bank_marketing_pipeline.joblib")

    assert "preprocessing" in model.named_steps
    assert "model" in model.named_steps

