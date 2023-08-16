import os
import requests, json
import uuid

spira_api_base_url = os.environ["SPIRA_API_BASE_URL"]
user = os.environ["SPIRA_USER"]
password = os.environ["SPIRA_PASSWORD"]

def main():
    (user_id, token, token_type) = get_token()
    print(user_id, token)
    register_inference(user_id, token)

def get_token():
    
    url = '{}/v1/users/auth'.format(spira_api_base_url)
    
    try:
        response = requests.post(
            url, 
            data = {
                "username": user,
                "password": password
            },
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }            
        )

        json_response = json.loads(response.content)

        return (json_response["id"], json_response["access_token"], json_response["token_type"])

        if response.status_code != 200:
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise(e)

def register_inference(user_id, token):
    url = '{}/v1/users/{}/inferences'.format(spira_api_base_url, user_id)
    print(create_inference_files())
    try:
        response = requests.post(
            url, 
            data = create_inference_data(user_id),
            files = create_inference_files(),
            headers = {
                "Authorization": "bearer {}".format(token)
            }            
        )

        print(response.content)

        if response.status_code != 200:
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise(e)



def create_inference_data(user_id):
    return {
        "gender": "M",
        "age": 23,
        "rgh": "fake_rgh",
        "covid_status": "Sim",
        "mask_type": "None",
        "user_id": user_id,
        "model_id": "648006eea6872f9412fb2c60",
        "status": "processing",
        "local": "hospital_1",
        "cid": "fake_cid",
        "bpm": "fake_bpm",
        "created_in": "2022-07-18 17:07:16.954632",
        "respiratory_frequency": "123",
        "respiratory_insufficiency_status": "Sim",
        "location": "h1",
        "last_positive_diagnose_date": "",
        "hospitalized": "TRUE",
        "hospitalization_start": "2022-07-18 17:07:16.954632",
        "hospitalization_end": "2022-07-18 17:07:16.954632",
        "spo2": "123"
    }

def create_inference_files():
    return {
        "aceite": open("./mock_data_1.txt", "rb"),
        "sustentada": open("./mock_data_2.txt", "rb"),
        "parlenda": open("./mock_data_3.txt", "rb"),
        "frase": open("./mock_data_4.txt", "rb"),
    }

main()