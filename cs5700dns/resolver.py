from math import radians, cos, sin, asin, sqrt
import requests 

config = {
    'domain': None,
    'replicas': {
        '34.238.192.84': [36.7978, -76.1759], # N. Virgina
        '13.231.206.182': [35.6895, 139.6917], # Tokyo
        '13.239.22.188': [-33.8678, 151.2073], # Sydney
        '34.248.209.79': [53.3331, -6.2489], # Ireland
        '18.231.122.62': [-23.5475, -46.6361], # Sao Paulo
        '3.101.37.125': [37.7749, -122.4194] # San Fransisco
    }
}

def set_domain(name):
    config['domain'] = name

def calculate_distance(lat1, lat2, lon1, lon2):
    '''
    Calculated distance in KM between two points on the earth
    Used calculation from: https://www.geeksforgeeks.org/program-distance-two-points-earth/
    '''
    
    # Converts from degrees to radians
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. 
    r = 6371
       
    # calculate the result 
    return(c * r)

def get_coordinates(ip):
    '''
    Returns the estimated latitude and longtitude of an IP address
    '''
    print("Looking up location of ip address: " + ip)
    ip_api = 'http://ip-api.com/json/' + ip
    response = requests.get(ip_api).json()
    lat = response["lat"]
    lon = response["lon"]
    print("Lat is" + str(lat) + " and lon is " + str(lon))
    return lat, lon

def resolve(name, ip):
    if config['domain'] != name:
        return None
    # TODO return IP address based on measurement
    print(ip)
    #get_coordinates(ip)
    return '34.23.192.84'
 

