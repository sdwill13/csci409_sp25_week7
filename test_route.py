from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth(username='admin', password='password123') # Creates a HTTPBasicAuth login
bad_auth = HTTPBasicAuth(username='admin', password='badpassword')

#Testing Unauthorized route no login
def test_read_main_route_unauthorized_nologin():
    response = client.get("/routes")
    assert response.status_code == 401 # Checks for authorized status code

#Testing Unauthorized route but bad credentials
def test_read_main_route_unauthorized_bad_credentials():
    response = client.get("/routes", auth=bad_auth)
    assert response.status_code == 401
#Testing Authorized route
def test_read_main_route_authorized():
    response = client.get("/routes", auth=auth)
    assert response.status_code == 200 # Checks for authorized status
#Reading route content
def test_read_route_content():
    response = client.get("/routes/Red", auth=auth)
    route = response.json().get("route")
    assert response.status_code == 200
    #verify route details
    assert route.get("id") == 'Red'
    assert route.get("type") == 1
    assert route.get("color") == 'DA291C'
    assert route.get("text_color") == 'FFFFFF'
    assert route.get("description") == 'Rapid Transit'
    assert route.get("long_name") == 'Red Line'

#Route not found
def test_read_route_not_found():
    route_id = "Chauncey"
    response = client.get(f"/routes/{route_id}",auth=auth)
    assert response.status_code == 404
    print(response.json())
    assert response.json().get("message") == f"Route {route_id} not found"