from fastapi import FastAPI, Depends
import httpx
from configuration.config import ServerSettings
from security.auth import authenticate
from configuration.config import Message
from fastapi.responses import JSONResponse

vehicle_app = FastAPI()#

def build_server_config():
    return ServerSettings()

# Dependency to fetch all alerts
async def get_all_vehicles(route: str = None, revenue: str = None, sconfig:ServerSettings = Depends(build_server_config)):
    params = {}
    if route:
        params["filter[route]"] = route
    if revenue:
        params["filter[revenue]"] = revenue

    async with httpx.AsyncClient() as client: # Define client
        response = await client.get(f"{sconfig.endpoint}/vehicles?api_key={sconfig.api_key}", params=params)
        if response.status_code == 400:
            return JSONResponse(status_code=400, content={"message": f"Bad Request"})
        elif response.status_code == 403:
            return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"})
        elif response.status_code == 429:
            return JSONResponse(status_code=429, content={"message": f"Too Many Requesti"})
        response.raise_for_status()
        return response.json()

async def get_vehicle_by_id(vehicle_id:str, sconfig:ServerSettings = Depends(build_server_config)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{sconfig.endpoint}/vehicles/{vehicle_id}?api_key={sconfig.api_key}")
        if response.status_code == 400:
            return JSONResponse(status_code=400, content={"message": f"Bad Request"})
        elif response.status_code == 403:
            return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"})
        elif response.status_code == 404:
            return JSONResponse(status_code=404, content={"message": f"Vehicle {vehicle_id} not found"})
        elif response.status_code == 406:
            return JSONResponse(status_code=406, content={"message": f"Not Acceptable"})
        elif response.status_code == 429:
            return JSONResponse(status_code=429, content={"message": f"Too Many Requests"})

        response.raise_for_status()
        return response.json()

@vehicle_app.get("/",
               responses= {400:{"model":Message},
                            403:{"model": Message},
                            429:{"model": Message}
                            })
async def read_vehicles(vehicles=Depends(get_all_vehicles), user: dict = Depends(authenticate)):
    return vehicles

@vehicle_app.get("/{vehicle_id}",
responses = {400: {"model": Message},
             403: {"model": Message},
             404: {"model": Message},
             406: {"model": Message},
             429: {"model": Message}})
async def read_vehicle(vehicle_id:str, vehicle=Depends(get_vehicle_by_id), user: dict = Depends(authenticate)):
    return vehicle