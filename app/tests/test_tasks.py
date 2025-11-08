from fastapi.testclient import TestClient
from app.main import app
import pytest


client = TestClient(app)

@pytest.fixture(scope="session")
def auth_token():
    # Login into account
    payload = {
        "email": "alice@abc.com",
        "password": "abcd1234"
    }
    login_response = client.post(url="/auth/login", json=payload)
    assert login_response.status_code == 200
    data = login_response.json()
    return data["access_token"]

@pytest.fixture(scope='session')
def task_id():
    return {
    "id":0#Initialization
    }

def test_create_task(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {
        "title": "Test task"
    }
    response = client.post(url="/tasks/", json=payload, headers=headers)
    assert response.status_code == 200, f"Create task test failed: {response.text}"

def test_get_tasks(auth_token,task_id):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = client.get(url="/tasks/", headers=headers)
    data =response.json()
    for each in data:
        if each['title']=="Test task":
            task_id["id"]=each['id']
    assert response.status_code == 200, f"Create task test failed: {response.text}"

def test_update_task(auth_token,task_id):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    url = "/tasks/{task_id}".format(task_id=task_id["id"])
    payload={
        "title":"Test Task",
        "description":"For testing",
        "status":"completed"
    }
    response = client.patch(url=url,json=payload,headers=headers)
    print(response.json())
    assert response.status_code==200,"Updation failure"

def test_delete_task(auth_token,task_id):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    url = "/tasks/{task_id}".format(task_id=task_id["id"])
    response = client.delete(url=url,headers=headers)
    assert response.status_code==204,"Deletion  failure"