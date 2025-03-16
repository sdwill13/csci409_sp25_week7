from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth(username='admin', password='password123') # Creates a HTTPBasicAuth login
bad_auth = HTTPBasicAuth(username='admin', password='badpassword')

#Testing Unauthorized lines no login
def test_read_main_line_unauthorized_nologin():
    response = client.get("/lines")
    assert response.status_code == 401 # Checks for authorized status code

#Testing Unauthorized line but bad credentials
def test_read_main_line_unauthorized_bad_credentials():
    response = client.get("/lines", auth=bad_auth)
    assert response.status_code == 401
#Testing Authorized line
def test_read_main_line_authorized():
    response = client.get("/lines", auth=auth)
    assert response.status_code == 200 # Checks for authorized status
#Reading line content
def test_read_line_content():
    response = client.get("/lines/line-Mattapan", auth=auth)
    line = response.json().get("line")
    assert response.status_code == 200
    #verify line details
    assert line.get("id") == "line-Mattapan"
    assert line.get("color") == "DA291C"
    assert line.get("text_color") == "FFFFFF"
    assert line.get("short_name") == ""
    assert line.get("long_name") == "Mattapan Trolley"

#Line not found
def test_read_line_not_found():
    line_id = "Chauncey"
    response = client.get(f"/lines/{line_id}",auth=auth)
    assert response.status_code == 404
    print(response.json())
    assert response.json().get("message") == f"Line {line_id} not found"