import requests

config = {
    'origin': None
}

def set_origin(origin):
    config['origin'] = origin

def get(path):
    try:
        # hard code to 8080 per requirement
        url = 'http://' + config['origin'] + ':8080' + path
        print('GET - URL:', url)
        resp = requests.get(url)
    except Exception as e:
        status_code = 500
        content = ''
        error = e
    else:
        status_code = resp.status_code
        content = resp.content
        error = None

    return status_code, content, error