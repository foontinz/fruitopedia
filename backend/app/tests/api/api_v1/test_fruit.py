from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import Depends, status

from app.core.config import settings

def test_read_created_fruit(client: TestClient, override_dep_db, get_test_db) -> None:
    fruit = {
        "name": "Apple",
    }
    response = client.post(f"{settings.API_V1_STR}/fruit/", json=fruit)
    
    assert response.status_code == status.HTTP_201_CREATED
    