from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth(username='admin',password='password123')
bad_auth = HTTPBasicAuth(username='admin', password='badpassword')

def test_read_main_vehicle_unauthorized_nologin():
    response = client.get("/vehicles")
    assert response.status_code == 401

def test_read_main_vehicle_unauthorized_bad_credentials():
    response = client.get("/vehicles", auth=bad_auth)
    assert response.status_code == 401

def test_read_main_vehicle_authorized():
    response = client.get("/vehicles", auth=auth)
    assert response.status_code == 200


def test_read_vehicle_content():
    response = client.get("/vehicles/y3103", auth=auth)
    vehicle = response.json().get("vehicle")
    assert response.status_code == 200
    #verify details
    assert vehicle.get("id") == 'y3103'
    assert vehicle.get("type") == 'vehicle'


def test_read_vehicle_not_found():
    vehicle_id = "Chauncey"
    response = client.get(f"/vehicles/{vehicle_id}", auth=auth)
    assert response.status_code == 404
    print(response.json())
    assert response.json().get("message") == f"Vehicle {vehicle_id} not found"

