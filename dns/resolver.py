
config = {
    'domain': None
}

def set_domain(name):
    config['domain'] = name

def resolve(name, ip):
    if config['domain'] != name:
        return None
    # TODO return IP address based on measurement
    return '124.5.123.43'
 
