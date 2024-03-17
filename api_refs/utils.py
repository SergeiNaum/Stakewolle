import json
import requests
from requests.exceptions import RequestException

from config.settings import apikey


def check_email(email):

    try:
        email_verify = requests.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key={apikey}&email={email}")
        email_verify.raise_for_status()
        email_data = email_verify.content
        data_json = json.loads(email_data)
        if data_json['deliverability'] == 'DELIVERABLE':
            return True
        else:
            return False
    except RequestException as e:
        print(f"Ошибка при проверке email: {e}")
        return False
    except (KeyError, ValueError):
        print("Ошибка при разборе ответа сервера.")
        return False
