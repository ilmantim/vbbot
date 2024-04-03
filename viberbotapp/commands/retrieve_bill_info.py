import requests
from environs import Env

env = Env()
env.read_env()

API_BASE_URL = env.str('API_BASE_URL')


def retrieve_bill_info(bill_id: str):
    url_for_id = (
        f"https://{API_BASE_URL}/api/v0/cabinet/terminal/"
        f"getAccounts/{bill_id}"
    )

    response = requests.get(url_for_id)
    response.raise_for_status()
    response_id = response.json()
    if response_id and "id_PA" in response_id[0]:
        id_PA = str(response_id[0]["id_PA"])
        url_for_bill = (
            f"https://{API_BASE_URL}/api/v0/cabinet/terminal/"
            f"getAccountInfo/{id_PA}"
        )
        response = requests.get(url_for_bill)
        response.raise_for_status()
        response_bill = response.json()
        return response_bill
    else:
        return False
