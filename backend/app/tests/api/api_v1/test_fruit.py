from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import Depends, status

from app.schemas.fruit import FruitRequest
from app.core.config import settings

def test_create_fruit_without_description(client: TestClient, override_dep_db, test_db: Session) -> None:
    fruit = FruitRequest(
        name="Apple").dict()

    response = client.post(f"{settings.API_V1_STR}/fruit/", json=fruit)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == fruit["name"]
    assert response.json()["description"] == fruit["description"]

def test_create_fruit_with_description(client: TestClient, override_dep_db, test_db: Session) -> None:
    fruit = FruitRequest(
        name="Banana", 
        description="An yellow fruit").dict()

    response = client.post(f"{settings.API_V1_STR}/fruit/", json=fruit)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == fruit["name"]
    assert response.json()["description"] == fruit["description"]
    
def test_create_fruit_duplicate_name(client: TestClient, override_dep_db, test_db: Session) -> None:
    fruit = FruitRequest(
        name="Banana", 
        description="An yellow fruit").dict()

    fruit_dublicate = FruitRequest(
        name="Banana",
        description="An yellow fruit").dict()
    
    client.post(f"{settings.API_V1_STR}/fruit/", json=fruit)п
    response = client.post(f"{settings.API_V1_STR}/fruit/", json=fruit_dublicate)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
