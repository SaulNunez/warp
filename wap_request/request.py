_headers = {'Accept', 'text/vnd.wap.wml'}

def request_wap(path: str):
    return requests.get(path, headers=_headers)