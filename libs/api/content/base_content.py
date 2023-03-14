import requests
from faker import Faker
import os
from libs.api.base_api import BaseApi

from utils.file_handlers import load_env_file
from constants import CONTENT_PATH


load_env_file()
CONTENT_API_KEY = os.getenv('CONTENT_API_KEY')
MAX_TIMEOUT_IN_SEC = int(os.getenv('TIMEOUT'))


class BaseContentApi(BaseApi):    
    def __init__(self) -> None:
        super().__init__()

    def get_url(self, uri: str = CONTENT_PATH):
        return super().get_url(uri)
    
    def create_headers(self):
        headers = {"Accept-Verson": "v5.0"}
        return headers

    def get(self, 
            endpoint: str, 
            headers: dict = None, 
            params = None, 
            content_api_key: dict = {'key': CONTENT_API_KEY},
            cookies: dict = None, 
            timeout: dict = None,  **kwargs):
        
        url = self._base_url + endpoint

        _params = dict()

        if headers is None:
            headers = self._headers

        if cookies is None:
            cookies = {}
        
        if timeout is None:
            timeout = MAX_TIMEOUT_IN_SEC

        if content_api_key is not None:
            _params.update(content_api_key)
        
        if params is not None:
            _params.update(params)

        return requests.get(url=url, headers=headers, params=_params, cookies=cookies, timeout=timeout)
