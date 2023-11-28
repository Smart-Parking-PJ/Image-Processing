import requests
from api_server import api_add

def api_patch(id, car, image_path):
    ts = requests.get(api_add + str(1) + "/").json()["totalspace"]

    with open(image_path, 'rb') as file:
        update_data = {
        "currentcar": car,
        "emptyspace" : ts - car,
        }
        files = {"image": (image_path, file, 'image/jpeg')}

        #patch요청
        response = requests.patch(api_add + str(id) + "/", data = update_data, files=files)
    print(response.status_code)