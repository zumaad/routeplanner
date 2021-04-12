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


class LocationRequest(BaseModel):
    start_lon: float
    start_lat: float
    radius: int
    preferences: List[str]


@app.post("/locations")
def location_handler(location_request: LocationRequest) -> List[Dict]:
    """
    Returns a list of locations that a user would want to visit given a user's preferences, their starting location,
    and how far they'd like to explore.

    :param location_request:
    :return: a list of locations that the user would want to visit
    """
    print(f"location request: {location_request}")
    start = [location_request.start_lon, location_request.start_lat]
    query_result = mongo_client.pullDataInRadius("Boston", start, location_request.radius)
    print(f"query result len is {len(query_result)}")
    sanitized_results = []
    for result in query_result:
        result['_id'] = str(result['_id'])
        sanitized_results.append(result)
    return sanitized_results


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
