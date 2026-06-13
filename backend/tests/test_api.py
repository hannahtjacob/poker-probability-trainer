import os

import pytest
from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import get_db
from app.main import app


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: object()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_root_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_simulate_returns_200_for_valid_input(client):
    response = client.post(
        "/api/simulate",
        json={
            "hero_cards": ["As", "Kh"],
            "community_cards": ["Qd", "Jc", "2h"],
            "num_opponents": 2,
            "simulations": 100,
            "seed": 42,
        },
    )

    assert response.status_code == 200
    assert "win_probability" in response.json()


def test_analyze_returns_simulation_and_recommendation(client):
    response = client.post(
        "/api/analyze",
        json={
            "hero_cards": ["As", "Kh"],
            "community_cards": ["Qd", "Jc", "2h"],
            "num_opponents": 2,
            "simulations": 100,
            "seed": 42,
            "save_result": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "simulation" in body
    assert "recommendation" in body
    assert body["saved_id"] is None


def test_invalid_cards_return_400(client):
    response = client.post(
        "/api/simulate",
        json={
            "hero_cards": ["As", "Ax"],
            "community_cards": [],
            "simulations": 100,
        },
    )

    assert response.status_code == 400
    assert "Invalid card" in response.json()["detail"]
