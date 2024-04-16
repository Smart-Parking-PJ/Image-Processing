import requests
from app.config import get_secret

def api_patch(id, car):
    api_url = get_secret("API_SERVER")
    with open('pred.jpg', 'rb') as file:
        img = file.read()
        upload = {'image':img}
        update_data = {
        "currentCar": car,
        }
        #patch요청
        requests.patch(api_url + str(id), data = update_data, files = upload)

if __name__ == "__main__":
    api_url = "https://93c4-223-194-160-130.ngrok-free.app/parking/1"
    with open('predicted/pred_0.jpg', 'rb') as file:
        #patch요청
        img = file.read()
        upload = {'image':img}
        update_data = {
        "image" : img
        }
        response = requests.patch(api_url, files = upload)
        print(response.status_code)