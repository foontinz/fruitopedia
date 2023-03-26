from fastapi import status
from fastapi.exceptions import RequestValidationError

from app import schemas
from app.schemas import Message

RESPONSES = {
    "GET": {
        status.HTTP_200_OK: {
            "model": schemas.FruitResponse,
            "description": "Resource found"
            },
        status.HTTP_404_NOT_FOUND: {
            "model": schemas.FruitResponse,
            "description": "Requested resource not found"
            },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.FruitResponse,
            "description": "Not authorized, please provide Authorization header"
            },
        status.HTTP_403_FORBIDDEN: {
            "model": schemas.FruitResponse,
            "description": "Not enough permissions to access resource"
            },
        },
    "MULTI_GET": { 
        status.HTTP_200_OK: {
            "model": schemas.FruitMultiResponse,
            "description": "Resource found"
            },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.FruitResponse,
            "description": "Not authorized, please provide Authorization header"
            },
        status.HTTP_403_FORBIDDEN: {
            "model": schemas.FruitResponse,
            "description": "Not enough permissions to access resource"
            }   
        },
    "POST": {
        status.HTTP_201_CREATED: {
            "model": schemas.FruitResponse,
            "description": "Resource created"
            },
        status.HTTP_400_BAD_REQUEST: {
            "model": schemas.FruitResponse,
            "description": "Resource not created, due to reasons clarified in FruitResponse"
            },
        status.HTTP_403_FORBIDDEN: {
            "model": schemas.FruitResponse, 
            "description": "Not enough permissions to access resource"
            },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.FruitResponse,
            "description": "Not authorized, please provide Authorization header"
            },
        },
    "PUT": {
        status.HTTP_200_OK: {
            "model": schemas.FruitResponse,
            "description": "Resource updated"
            },
        status.HTTP_400_BAD_REQUEST: {
            "model": schemas.FruitResponse,
            "description": "Resource not created, due to reasons clarified in message"
            },
        status.HTTP_404_NOT_FOUND: {
            "model": schemas.FruitResponse,
            "description": "Requested resource not found"
            },
        status.HTTP_403_FORBIDDEN: {
            "model": schemas.FruitResponse,
            "description": "Not enough permissions to access resource"
            },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.FruitResponse,
            "description": "Not authorized, please provide Authorization header"
            },
        },
    "DELETE": {
        status.HTTP_204_NO_CONTENT: {
            "description": "Resource deleted"
            },
        status.HTTP_400_BAD_REQUEST: {
            "model": schemas.FruitResponse,
            "description": "Resource not deleted, due to reasons clarified in message"
            },
        status.HTTP_404_NOT_FOUND: {
            "model": schemas.FruitResponse,
            "description": "Requested resource not found"
            },
        status.HTTP_403_FORBIDDEN: {
            "model": schemas.FruitResponse,
            "description": "Not enough permissions to access resource"
            },
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.FruitResponse,
            "description": "Not authorized, please provide Authorization header"
            }
        }
    }
