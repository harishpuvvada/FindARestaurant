from GeoCode import getGeocodeLocation #This will communicate with other GeoCode.py
import json
import httplib2

import sys
import codecs

#sys.stdout = codecs.getwriter('utf8')(sys.stdout) #To deal with Non-English words
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "YOUR FOURSQUARE CLIENT ID"
foursquare_client_secret = "YOUR FOURSQUARE CLIENT SECRET"



def findARestaurant(mealType,location):
	#Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	print("Meal Type:",mealType,"\n","Location:",location)

	latitude,longitude = getGeocodeLocation(location)
	print("Latitude:", latitude,"\n","Longitude:", longitude)

	#Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.

	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])

	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20180404&ll=%s,%s&query=%s' % (foursquare_client_id,foursquare_client_secret,latitude,longitude,mealType))
	ht = httplib2.Http()
	response,content = ht.request(url,'GET')
	result = json.loads(content) #content = [response, content]

	if result['response']['venues']:
		firstRest = result['response']['venues'][0]    	#3. Grab the first restaurant
		Rest_ID = firstRest['id']
		Rest_Name = firstRest['name']
		try:
			Rest_Addr = firstRest['location']['address']
		except:
			Rest_Addr = "Address not found"
			print("Address not found")

		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20180404&client_secret=%s' % ((Rest_ID,foursquare_client_id,foursquare_client_secret)))
		ht = httplib2.Http()
		response,content = ht.request(url,'GET')
		result = json.loads(content)

		if result['response']['photos']['items']:
			firstpic = result['response']['photos']['items'][0] #First image
			prefix = firstpic['prefix']
			suffix = firstpic['suffix']
			imageURL = prefix + "300x300" + suffix   #300x300 picture

		else:                                       #default a image url
			imageURL = "https://vignette.wikia.nocookie.net/simpsons/images/6/60/No_Image_Available.png/revision/latest?cb=20170219125728"


		restaurantInfo = {'name':Rest_Name, 'image':imageURL, 'address':Rest_Addr }
		print("Restaurant Name: %s" % restaurantInfo['name'])
		print("Restaurant Address: %s" % restaurantInfo['address'])
		print("Image: %s \n" % restaurantInfo['image'])
		return restaurantInfo
	else:
		print("No Restaurants Found for %s" % location)
		return "No Restaurants Found"


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
