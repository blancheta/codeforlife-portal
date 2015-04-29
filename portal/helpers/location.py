import urllib3
import json

http = urllib3.PoolManager()

def is_GB(component):
    return 'country' in component['types'] and component['short_name'] == 'GB'

def extract_locality(components):
    for component in components:
        if 'locality' in component['types']:
            return component['long_name']

        if 'postal_town' in component['types']:
            return component['long_name']
    
    return None

def extract_location_data(results):
    for result in results:
        for component in result['address_components']:

            locality = extract_locality(result['address_components'])

            location = result['geometry']['location']
            return locality, location['lat'], location['lng']

    return None, None, None

# Uses Google Maps API to lookup postcode + country(ISO 3166-1 alpha-2) and returns location data
# By using country, it can return a more accurate location as the same postcode may exist in multiple countries
# Coordinates of the country will be returned if postcode is invalid
# Return format is:
#     error, town, latitude, longitude
# If error is None then all went well,
# else error is not None and town, lat, lng = '0'
def lookup_postcode(postcode, country):

    res = http.request('GET', 'http://maps.googleapis.com/maps/api/geocode/json',
                      fields={'address': postcode, 'components': 'country:' + country})

    data = json.loads(res.data)

    if not res.status == 200:
        return 'Request error: %s' % res.status, '0', '0', '0'

    if not (data.get('status', '') == 'OK' and len(data.get('results', [])) > 0):
        return 'API error: %s' % data.get('status', 'No status'), '0', '0', '0'

    town, lat, lng = extract_location_data(data['results'])

    if town is None:
        return 'No town', '0', lat, lng

    return None, town, lat, lng
