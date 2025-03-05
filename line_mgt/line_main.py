from fastapi import FastAPI, Depends
import requests
from configuration.config import ServerSettings
from security.auth import authenticate
from configuration.config import Message
from fastapi.responses import JSONResponse
line_app = FastAPI()

def build_server_config():
    return ServerSettings()

@line_app.get("/",
               responses= {400:{"model":Message},
                            403:{"model": Message},
                            429:{"model": Message}
                            })
def get_routes(sconfig:ServerSettings = Depends(build_server_config), user: dict = Depends(authenticate)):
    lines_list = list()
    response = requests.get(sconfig.endpoint+f"/lines?&api_key={sconfig.api_key}") # Send a request to the endpoint
    if response.status_code == 400:
        return JSONResponse(status_code=400, content={"message":f"Bad Request"})
    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message":f"API Request Forbidden"})
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message":f"Too Many Requesti"})

    # Convert the response to json and extract the data key
    lines = response.json()["data"]
    for line in lines:
        # Loop through all routes extracting relevant information
        lines_list.append({
            "id": line["id"],
            "color": line["attributes"]["color"],
            "text_color": line["attributes"]["text_color"],
            "short_name": line["attributes"]["short_name"],
            "long_name": line["attributes"]["long_name"],
        })
    # Return the routes_list in JSON format
    return {"lines": lines_list}

@line_app.get("/{line_id}",
responses = {400: {"model": Message},
             403: {"model": Message},
             404: {"model": Message},
             406: {"model": Message},
             429: {"model": Message}})
def get_route(line_id: str, sconfig:ServerSettings = Depends(build_server_config), user: dict = Depends(authenticate)):
    response = requests.get(sconfig.endpoint + f"/lines/{line_id}?api_key={sconfig.api_key}") # Send a request to the endpoint
    if response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": f"Bad Request"})
    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"})
    elif response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": f"Line {line_id} not found"})
    elif response.status_code == 406:
        return JSONResponse(status_code=406, content={"message": f"Not Acceptable"})
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": f"Too Many Requests"})

    # Convert the response to json and extract the data key
    line_data = response.json()["data"]
    # Extract the relevant data
    line = {
            "id": line_data["id"],
            "color": line_data["attributes"]["color"],
            "text_color": line_data["attributes"]["text_color"],
            "short_name": line_data["attributes"]["short_name"],
            "long_name": line_data["attributes"]["long_name"],
        }
    # Return the data to the user
    return {"line": line}