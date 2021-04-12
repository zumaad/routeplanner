import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import uvicorn
from fastapi import FastAPI
from typing import List, Dict, Tuple
from database.mongo_client import MongoClient
from pydantic import BaseModel

mongo_client = MongoClient()
app = FastAPI()


class LocationsRequest(BaseModel):
    start_lon: float
    start_lat: float
    radius: int
    preferences: List[str]


class Location(BaseModel):
    tags: Dict
    geometry: Dict


@app.post("/locations", response_model=List[Location])
def location_handler(locations_request: LocationsRequest) -> List[Location]:
    """
    Returns a list of locations that a user would want to visit given a user's preferences, their starting location,
    and how far they'd like to explore.
    """
    print(f"location request: {locations_request}")
    start = [locations_request.start_lon, locations_request.start_lat]
    query_result = mongo_client.pullDataInRadius("Boston", start, locations_request.radius)
    locations = []
    for document in query_result:
        locations.append(Location(tags=document["tags"], geometry=document["geometry"]))
    return locations


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
