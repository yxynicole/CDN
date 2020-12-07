import requests

def get(host, path):
    try:
        # url = 'http://' + host + path
        # print("about to try " + url)
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