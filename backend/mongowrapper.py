import uvicorn
from fastapi import FastAPI
import pymongo
from typing import List, Dict
import json

MONGO_DB_NAME = "test"
MONGO_COLLECTION_NAME = "testcollection"
mongo_client = pymongo.MongoClient()
app = FastAPI()


@app.get("/mongo")
def mongo_query(query: str) -> List[Dict]:
    mongo_compatible_query = json.loads(query)
    col = mongo_client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]
    query_result = col.find(mongo_compatible_query)
    sanitized_results = []
    for result in query_result:
        result['_id'] = str(result['_id'])
        sanitized_results.append(result)
    return sanitized_results

if __name__ == "__main__":
    uvicorn.run("mongowrapper:app", reload=True)