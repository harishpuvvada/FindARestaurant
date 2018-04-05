import httplib2
import json

def getGeocodeLocation(inputString): #function to get lat&long of any given city
    try:
        google_api_key = "YOUR GOOGLE MAPS API KEY"
        locationString = inputString.replace(" ","+") #to convert spaces to "+"
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'%(locationString,google_api_key))
        h = httplib2.Http()
        response,content = h.request(url,'GET')
        result = json.loads(content)
        latitude = result['results'][0]['geometry']['location']['lat']
        longitude = result['results'][0]['geometry']['location']['lng']
        return (latitude,longitude)
    except:
        print("problem with GeoCode file")
