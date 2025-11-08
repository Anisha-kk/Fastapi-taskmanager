from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_invalid_login():
    payload = {
    "email": "cathy@abc.com",
    "password": "a12b3c4d"
    }
    response = client.post(url="/auth/login",json=payload)
    assert response.status_code!=200,"Login verification test failed"
    

def test_valid_login():
    payload = {
    "email": "alice@abc.com",
    "password": "abcd1234"
    }
    response = client.post(url="/auth/login",json=payload)
    assert response.status_code==200,"Login verification test failed"

    
    
