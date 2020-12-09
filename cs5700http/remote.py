import requests

def get(host, path):
    try:
        # hard code to 8080 per requirement
        resp = requests.get('http://' + host + ':8080' + path)
    except Exception as e:
        status_code = 500
        content = ''
        error = e
    else:
        status_code = resp.status_code
        content = resp.content
        error = None

    return status_code, content, error