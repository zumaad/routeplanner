import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import uvicorn
from fastapi import FastAPI
from typing import List, Dict, Tuple, Set
from database.mongo_client import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

mongo_client = MongoClient()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationsRequest(BaseModel):
    start_lon: float
    start_lat: float
    radius: int
    preferences: List[str]


class Location(BaseModel):
    tags: Dict
    geometry: Dict


def get_only_preferred_locations(locations: List[Location], preferences: Set[str]) -> List[Location]:
    preferred_locations = []
    for location in locations:
        maybe_leisure = location.tags.get("leisure")
        maybe_amenity = location.tags.get("amenity")
        place = maybe_amenity if maybe_amenity else maybe_leisure
        if place in preferences:
            preferred_locations.append(location)
    return preferred_locations


@app.post("/locations", response_model=List[Location])
def location_handler(locations_request: LocationsRequest) -> List[Location]:
    """
    Returns a list of locations that a user would want to visit given a user's preferences, their starting location,
    and how far they'd like to explore.
    """
    print(f"location request: {locations_request}")
    start = [locations_request.start_lon, locations_request.start_lat]
    query_result = mongo_client.pullDataInRadius("Boston", start, locations_request.radius)
    preferences = set(locations_request.preferences)
    locations = [Location(tags=document["tags"], geometry=document["geometry"]) for document in query_result]
    locs = locations
    if preferences:
        locs = get_only_preferred_locations(locations, preferences)
    print(locs)
    return locs


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
