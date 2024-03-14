import requests
from app.config import get_secret

async def api_patch(id, car, image_path):
    api_url = get_secret["API_SERVER"]
    ts = requests.get(api_url + str(id) + "/").json()["totalspace"]

    async with open(image_path, 'rb') as file:
        update_data = {
        "currentcar": car,
        "emptyspace" : ts - car,
        }
        files = {"image": (image_path, file, 'image/jpeg')}

        #patch요청
        response = requests.patch(api_url + str(id) + "/", data = update_data, files=files)
    print(response.status_code)