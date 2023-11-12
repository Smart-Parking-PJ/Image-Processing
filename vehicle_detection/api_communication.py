import requests
from api_server import api_add

def api_patch(id, currentcar, image):
    
    totalspace = requests.get(api_add + str(id) + "/")[totalspace]

    update_data = {
        "currentcar": currentcar,
        "emptyspace" : totalspace - currentcar,
        "image": image,
        }
    #patch요청
    requests.patch(api_add + str(id) + "/", update_data)