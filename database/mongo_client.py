import pymongo

class MongoClient:
    """ responsible for interacting with mongo """
    def __init__(self):
        self.client = pymongo.MongoClient()

    def insertDataByCity(self, cityName, data):
        """ Sample mongo insert for new or existing city with geospatial index check """

        db = self.client[cityName]
        posts = db.posts
        posts.create_index([('geometry', pymongo.GEOSPHERE)])
        for point in data:
            posts.insert_one(point)

    def pullDataInRadius(self, cityName, center, radius):
        """ Sample geospatial mongo query: radius is in meters """

        db = self.client[cityName]
        posts = db.posts
        pulls = [record for record in posts.find(
            {'geometry': {'$near': {'$geometry': {'type': 'Point', 'coordinates': center}, '$maxDistance': radius}}})]
        return pulls
