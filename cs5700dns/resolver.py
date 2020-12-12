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
    Uses the free ip_geo_location server: https://ip-api.com/docs/api:json
    '''
    
    error = None
    try:
        ip_api = 'http://ip-api.com/json/' + ip
        response = requests.get(ip_api).json()
        lat = response["lat"]
        lon = response["lon"]
    except:
        print("Error getting coordinates of "+ ip)
        error = "IP Geolocation Error"
    # print("For ip " + ip+ ", Lat is " + str(lat) + " and lon is " + str(lon))
    # print(calculate_distance(lat, 37.7749, lon, -122.4194))
    # print(calculate_distance(lat, 35.6895, lon, 139.6917))
    return lat, lon, error

def find_closest_replica_server(ip):
    '''
    Given the an ip address (ip), determines the closest replica server
    Returns the ip address of the closest replica server
    '''

    best_ip = ''
    min_dist = 100000000.00  # large min distance to initialize

    lat, lon, error = get_coordinates(ip)
    replicas = config['replicas']
    if error == None:
        for replica_ip in replicas.keys():
            print("Checking " + replica_ip)
            dist = calculate_distance(lat, replicas[replica_ip][0], lon, replicas[replica_ip][1])
            if dist < min_dist:
                best_ip = replica_ip
                min_dist = dist
    
    return best_ip


def resolve(name, ip):
    if config['domain'] != name:
        return None
    return find_closest_replica_server(ip)
 

