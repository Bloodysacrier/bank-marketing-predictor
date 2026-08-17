from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

VALID_DATA = {
    "age": 41,
    "job": "technician",
    "marital": "married",
    "education": "secondary",
    "balance": 3200,
    "housing": "yes",
    "loan": "no",
    "campaign": 2,
}


def test_valid_prediction():
    response = client.post("/predict", json=VALID_DATA)

    assert response.status_code == 200
    assert response.json()["prediction"] in ["yes", "no"]
    assert 0 <= response.json()["probability"] <= 1


def test_wrong_age_type():
    data = {**VALID_DATA, "age": "hola"}
    response = client.post("/predict", json=data)

    assert response.status_code == 422


def test_age_out_of_range():
    data = {**VALID_DATA, "age": -10}
    response = client.post("/predict", json=data)

    assert response.status_code == 422


def test_frontend_uses_predict_endpoint():
    html_response = client.get("/")
    css_response = client.get("/static/styles.css")
    js_response = client.get("/static/app.js")

    assert html_response.status_code == 200
    assert css_response.status_code == 200
    assert js_response.status_code == 200
    assert 'fetch("/predict"' in js_response.text
