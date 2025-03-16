from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth(username='admin', password='password123') # Creates a HTTPBasicAuth login
bad_auth = HTTPBasicAuth(username='admin', password='badpassword')

#Testing Unauthorized alert no login
def test_read_main_alert_unauthorized_nologin():
    response = client.get("/alerts")
    assert response.status_code == 401 # Checks for authorized status code

#Testing Unauthorized alert but bad credentials
def test_read_main_alert_unauthorized_bad_credentials():
    response = client.get("/alerts", auth=bad_auth)
    assert response.status_code == 401
#Testing Authorized alert
def test_read_main_alert_authorized():
    response = client.get("/alerts", auth=auth)
    assert response.status_code == 200 # Checks for authorized status
