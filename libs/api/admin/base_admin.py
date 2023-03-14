import jwt
import os
from datetime import datetime as dt
from libs.api.base_api import BaseApi

from utils.file_handlers import load_env_file
from constants import ADMIN_PATH

load_env_file()
ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')


class BaseAdminApi(BaseApi):
    def __init__(self) -> None:
        super().__init__()

    def get_url(self, uri: str = ADMIN_PATH):
        return super().get_url(uri)

    def __generate_token(self):
        id, secret = ADMIN_SECRET_KEY.split(':')
        iat = int(dt.now().timestamp())
        header = {
            'alg': 'HS256', 
            'typ': 'JWT', 
            'kid': id
        }
        payload = {
            'iat': iat, 
            'exp': iat + (5 * 60), # Expires after 5 minutes at maximum
            'aud': '/admin/'
        }
        token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

        return token

    def create_headers(self):
        token = self.__generate_token()
        headers = {'Authorization': 'Ghost {}'.format(token)}
        return headers

    