"""Integration tests for every endpoint in main.py using FastAPI's TestClient."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


# --- Page and health --------------------------------------------------------
def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FastAPI Calculator" in response.text


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- Successful operations --------------------------------------------------
@pytest.mark.parametrize(
    "endpoint, a, b, expected",
    [
        ("/add", 10, 5, 15),
        ("/add", -1.5, 2.5, 1.0),
        ("/subtract", 10, 5, 5),
        ("/subtract", 5, 10, -5),
        ("/multiply", 10, 5, 50),
        ("/multiply", -3, 2.5, -7.5),
        ("/divide", 10, 5, 2),
        ("/divide", 7, 2, 3.5),
    ],
)
def test_operations(client, endpoint, a, b, expected):
    response = client.post(endpoint, json={"a": a, "b": b})
    assert response.status_code == 200, response.text
    assert response.json()["result"] == pytest.approx(expected)


# --- Error handling ---------------------------------------------------------
def test_divide_by_zero(client):
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"error": "Cannot divide by zero!"}


@pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
def test_invalid_string_input(client, endpoint):
    response = client.post(endpoint, json={"a": "ten", "b": 5})
    assert response.status_code == 400
    assert "error" in response.json()


@pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
def test_missing_field(client, endpoint):
    response = client.post(endpoint, json={"a": 1})
    assert response.status_code == 400
    assert "b" in response.json()["error"]


def test_boolean_rejected(client):
    response = client.post("/add", json={"a": True, "b": 1})
    assert response.status_code == 400


def test_wrong_method_not_allowed(client):
    response = client.get("/add")
    assert response.status_code == 405


def test_unknown_route(client):
    response = client.post("/power", json={"a": 2, "b": 3})
    assert response.status_code == 404
