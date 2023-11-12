import requests
from api_server import api_add

def api_patch(id, car, image):
    
    ts = requests.get(api_add + str(1) + "/").json()["totalspace"]
    update_data = {
        "currentcar": car,
        "emptyspace" : ts - car,
        "image": image,
        }
    #patch요청
    requests.patch(api_add + str(id) + "/", update_data)