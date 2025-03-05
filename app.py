from fastapi import FastAPI

from route_mgt import route_main
from line_mgt import line_main
from alert_mgt import alert_main
from vehicle_mgt import vehicle_main
app = FastAPI() # Initialize the end point


app.mount("/routes", route_main.route_app)
app.mount("/lines", line_main.line_app)
app.mount("/alerts", alert_main.alert_app)
app.mount("/vehicles", vehicle_main.vehicle_app)

@app.get("/") # Create a default route
def read_root():
    return {"message": "Welcome to my FastAPI Application!"}