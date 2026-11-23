from flask import request

def wants_json():
    if request.is_json:
        return True

    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return (
        best == "application/json"
        and request.accept_mimetypes[best] > request.accept_mimetypes["text/html"]
    )