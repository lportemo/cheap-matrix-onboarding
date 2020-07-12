from django.conf import settings
import requests


def get_access_token():
    payload = {
        "type": "m.login.password",
        "user": settings.MATRIX_USERNAME,
        "password": settings.MATRIX_PASSWORD,
    }
    r = requests.post(
        f"https://{settings.MATRIX_HOMESERVER}/_matrix/client/r0/login", json=payload,
    )
    access_token = r.json().get("access_token")

    if not access_token:
        return False

    return access_token
