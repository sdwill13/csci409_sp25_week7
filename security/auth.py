from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

"""
    NOTE: This is for demonstration purposes only.
    Typically you would be connecting to a database to check for a username and password
"""
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "secret"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """Basic authentication dependency"""
    if credentials.username in USER_CREDENTIALS: # Check if username in "database"
        correct_password = USER_CREDENTIALS[credentials.username] # Get provided password
        if secrets.compare_digest(credentials.password, correct_password): # Check if passwords are the same
            return {"username": credentials.username}
    raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"}) # If any checks failed return a 401 status code