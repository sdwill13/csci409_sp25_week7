from pydantic_settings import BaseSettings
from pydantic import BaseModel

class ServerSettings(BaseSettings):
    api_key:str = '9a7bf8bccf9841f085539c5421466861'
    endpoint:str = 'https://api-v3.mbta.com/'

class Message(BaseModel):
    message: str # A string to store that message