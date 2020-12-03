import requests

def get(host, path):
    try:
        resp = requests.get('http://' + host + path)
    except Exception as e:
        status_code = 500
        content = ''
        error = e
    else:
        status_code = resp.status_code
        content = resp.content
        error = None

    return status_code, content, error