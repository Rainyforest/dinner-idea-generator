import responses
import googlemaps
from datetime import datetime
class Place():
    def __init__(self,place):
        # vicinity
        self.fomatted_address = place['formatted_address']
        self.geometry = Geometry(place['geometry'])
        self.name = place['name']
        self.opening_hours = OpeningHours(place['opening_hours'])
        # self.photos = Photo(place['photos'])
        self.rating = place['rating']
class Geometry():
    def __init__(self,geometry):
        self.location = Pos(geometry['location'])
        viewports = geometry['viewport']
        dir_names = viewports.keys()
        self.viewports = []
        for dir_name in dir_names:
            self.viewports.append(Viewport(viewports[dir_name],dir_name))
class Pos():
    def __init__(self,pos):
        self.lat = pos['lat']
        self.lng = pos['lng']
class Viewport(Pos):
    def __init__(self,pos,dir_name):
        super().__init__(pos)
        self.dir_name = dir_name

class OpeningHours():
    def __init__(self,opening_hours):
        self.open_now = opening_hours['open_now']
    

class PlaceAPI():

    def __init__(self):
        self.key = "" # add your google api token here
        self.client = googlemaps.Client(self.key)
        self.location = (48.460930, -123.334244)
        self.type = 'restaurant'
        self.language = 'en'
        self.region = 'CA'
        self.radius = 6000
        self.open_now = True

    def test_places_text_search(self):
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        responses.add(responses.GET, url,
                      body='{"status": "OK", "results": [], "html_attributions": []}',
                      status=200, content_type='application/json')

        json_result = self.client.places('restaurant', location=self.location,
                           radius=self.radius, region=self.region, language=self.language,
                           min_price=0, max_price=4, #open_now=self.open_now,
                           type=self.type)
        return self.parse_json_result(json_result['results'])

    def parse_json_result(self,json_result):
        place_result = []
        for place in json_result:
            place_result.append(Place(place))
        return place_result




placeapi = PlaceAPI()
result = placeapi.test_places_text_search()
name_list = []
for r in result:
    name_list.append(r.name)
    print(r.name)

