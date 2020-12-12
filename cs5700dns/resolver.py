
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

def set_domain(name):
    config['domain'] = name

def resolve(name, ip):
    if config['domain'] != name:
        return None
    # TODO return IP address based on measurement
    return '34.23.192.84'
 

