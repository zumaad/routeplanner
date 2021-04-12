import requests
import pymongo

class Overpass():
    """ Interact with the Overpass API """
    
    def __init__(self):
        self.url = 'http://overpass-api.de/api/interpreter'
        
        self.amenities = {'car_parking': ['parking','parking_entrance','parking_space'],
            'bike': ['bicycle_parking','bicycle_repair_station','bicycle_rental'],
            'bevs': ['bar','biergarten','pub'],
            'food': ['fast_food','food_court','ice_cream','cafe','restaurant','marketplace','vending_machine'],
            'entertainment': ['cinema','planetarium','theatre','dive_centre','internet_cafe'],
            'entertainment_21+': ['casino','nightclub'],
            'culture': ['arts_centre','fountain'],
            'emergency': ['fire_station','police','ranger_station'],
            'facilities': ['telephone','shower','toilets','drinking_water'],
            'mail': ['post_box','post_depot','post_office'],
            'dog': ['dog_toilet','animal_boarding'],
            'waste': ['sanitary_dump_station','recycling','waste_basket','waste_disposal','waste_transfer_station'],
            'religious': ['monastery','place_of_worship']}
        
        self.leisures = {'indoors':['amusement_arcade','bandstand','bowling_alley','dance','escape_game','ice_rink','sports_centre','sports_hall','trampoline_park'],
            'accomodations': ['sauna','resort'],
            'spectating': ['stadium','track'],
            'outdoors': ['disc_golf_course','fishing','golf_course','miniature_golf','horse_riding','pitch','playground','swimming_area','swimming_pool','water_park'],
            'nature': ['garden','firepit','nature_reserve','park','picnic_table','wildlife_hide'],
            'dog': ['dog_park'],
            '21+' :['adult_gaming_center']}
        
        self.known_cities = {'boston': {'id': 2315704,'bounds': {'minlat': 42.2279112, 'minlon': -71.1912491, 'maxlat': 42.3969775, 'maxlon': -70.8044881}}, 
                            'nyc': {'id': 175905,'bounds': {'minlat': 40.477399, 'minlon': -74.25909, 'maxlat': 40.9161785, 'maxlon': -73.7001809}}}
        
        self.client = pymongo.MongoClient()
        
    def getCityBBox(self, cityName):
        """ Search for cities matching the given name. Once the correct relation ID has been found, use getCityBBoxFromID to get city BBox """
        
        query = '[out:json];(relation["name"="{}"][boundary=administrative];);out skel bb qt;'.format(cityName)
        response = requests.get(self.url, params={'data':query})
        data = response.json()
        
        if len(data['elements']) > 1:
            query = '[out:json];(' 
            for element in data['elements']:
                query += '\nrelation({});'.format(element['id'])
            query += ');out skel bb qt;'
                
            print('\nSeveral locations returned. Open: https://overpass-turbo.eu/ and paste this command into the console: \n\n{}\n\nScroll over to the desired location and click the highlighted region to get the correct ID.'.format(query))
            
        elif len(data['elements']) == 0:
            print('No city found. Syntax is "New York" or "Los Angeles".')
            
        else:
            bbox = data['elements'][0]['bounds']
            return bbox
    
    def getCityBBoxFromID(self, id_):
        """ Get Bounding Box from city ID """
        query = '[out:json];(relation({}););out skel bb qt;'.format(id_)
        response = requests.get(self.url, params={'data':query})
        data = response.json()
        bbox = data['elements'][0]['bounds']
        return bbox
    
    def getAmenity(self, bbox, amenity):
        """ Get locations of the amenity within the bounding box """
        
        query = '[out:json];(node({},{},{},{})["amenity" = "{}"];);out geom;'.format(bbox['minlat'],bbox['minlon'],bbox['maxlat'],bbox['maxlon'],amenity)
        response = requests.get(self.url, params={'data':query})
        data = response.json()
        for element in data['elements']:
            element['geometry'] = {'type': 'Point', 'coordinates': [element['lon'],element['lat']]}
            del element['lat']
            del element['lon']
        return data['elements']
    
    def getLeisure(self, bbox, leisure):
        """ Get locations of the leisure activity within the bounding box """
        
        query = '[out:json];(node({},{},{},{})["leisure" = "{}"];);out geom;'.format(bbox['minlat'],bbox['minlon'],bbox['maxlat'],bbox['maxlon'],leisure)
        response = requests.get(self.url, params={'data':query})
        data = response.json()
        for element in data['elements']:
            element['geometry'] = {'type': 'Point', 'coordinates': [element['lon'],element['lat']]}
            del element['lat']
            del element['lon']
        return data['elements']
    
    def getAllAmenities(self, bbox):
        """ Get all locations of all amenities in the bounding box """
        
        rslt = []
        for amenityType in self.amenities.keys():
            for amenity in self.amenities[amenityType]:
                try:
                    for location in self.getAmenity(bbox, amenity):
                        rslt.append(location)
                except:
                    print(amenity)
        return rslt

    def getAllLeisures(self, bbox):
        """ Get all locations of all leisure activities in the bounding box """
        
        rslt = []
        for leisureType in self.leisures.keys():
            for leisure in self.leisures[leisureType]:
                try:
                    for location in self.getLeisure(bbox, leisure):
                        rslt.append(location)
                except:
                    print(leisure)
        return rslt

    def insertDataByCity(self, cityName, data):
        """ Sample mongo insert for new or existing city with geospatial index check """
        
        db = self.client[cityName]
        posts = db.posts
        posts.create_index([('geometry',pymongo.GEOSPHERE)])
        for point in data:
            posts.insert_one(point)
            
    def pullDataInRadius(self, cityName, center, radius):
        """ Sample geospatial mongo query: radius is in meters """
        
        db = self.client[cityName]
        posts = db.posts
        pulls = [record for record in posts.find({'geometry':{'$near':{'$geometry':{'type': 'Point','coordinates': center},'$maxDistance':radius}}})]
        return pulls