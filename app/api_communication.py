import requests
from app.config import get_secret

async def api_patch(id, car, file):
    api_url = get_secret["API_SERVER"]
    ts = await requests.get(api_url + str(id) + "/").json()["totalspace"]

    update_data = {
    "currentcar": car,
    "emptyspace" : ts - car,
    }

    #patch요청
    response = await requests.patch(api_url + str(id) + "/", data = update_data, files=file)
    print(response.status_code)