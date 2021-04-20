import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import uvicorn
from fastapi import FastAPI
from typing import List, Dict, Tuple, Set
from database.mongo_client import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from geopy.distance import distance

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


def get_all_locations(origin_lon: float, origin_lat: float, radius: int) -> List[Location]:
    """
    Fetches all the locations within a radius using the mongo client and returns them in the format we want.
    """
    origin = [origin_lon, origin_lat]
    query_result = mongo_client.pullDataInRadius("Boston", origin, radius)
    for result in query_result:
        result["tags"]["type"] = result["tags"].get("leisure", result["tags"].get("amenity"))
    locations = [Location(tags=result["tags"], geometry=result["geometry"]) for result in query_result]
    return locations


@app.post("/locations", response_model=List[Location])
def location_handler(locations_request: LocationsRequest) -> List[Location]:
    """
    Returns a list of locations that a user would want to visit given a user's preferences, their starting location,
    and how far they'd like to explore.
    """
    locations = get_all_locations(locations_request.start_lon, locations_request.start_lat, locations_request.radius)
    preferences = set(locations_request.preferences)
    if preferences:
        return [l for l in locations if l.tags.get("type") in preferences]
    return locations


@app.post("/route", response_model=List[Location])
def route_handler(locations_request: LocationsRequest) -> List[Location]:
    """
    Returns a route which is simply a list of locations, one of each type that the user had a preference for, in order
    of which one was closest to the user - taking into account that the user would go to one location
    """
    locations = get_all_locations(locations_request.start_lon, locations_request.start_lat, locations_request.radius)
    types_of_places_to_visit = set(locations_request.preferences)
    built_route = []
    origin = [locations_request.start_lat, locations_request.start_lon]
    while types_of_places_to_visit:
        possible_locations = [l for l in locations if l.tags.get("type") in types_of_places_to_visit]
        if not possible_locations:
            break
        closest_location = min(possible_locations, key=lambda l: distance(origin, [l.geometry["coordinates"][1],
                                                                                   l.geometry["coordinates"][0]]))
        built_route.append(closest_location)
        origin = [closest_location.geometry["coordinates"][1], closest_location.geometry["coordinates"][0]]
        type_of_place = closest_location.tags.get("type")
        types_of_places_to_visit.remove(type_of_place)
    return built_route


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host="0.0.0.0")
