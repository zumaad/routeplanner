from pprint import pprint
import ast

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['test-database_route']
collection = db['test-collection']




f = open("boston.txt")

docs = ast.literal_eval(f.read())

#
# # Grab a reference to the collection, and clear it out. Then insert the sample data.
posts = db.posts
posts.delete_many({})
posts.insert_many(docs)

# for post in posts.find({"tags.amenity" : "cafe"}):
#     print(post['id'], " ", end="")
#     pprint(post['tags'].get("amenity", "None"))

amenities = set()

for post in posts.find({}):
    amenities.add(post['tags'].get("amenity", "None"))
    #pprint(post)
    
print(amenities)