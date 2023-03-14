import requests
import os
from faker import Faker

from utils.custom_enums import HttpMethod
from utils.file_handlers import load_env_file
from constants import ADMIN_PATH


load_env_file()
API_ROOT = os.getenv('DEV_BASE_URL')
BASE_URL = API_ROOT + ADMIN_PATH
ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')
MAX_TIMEOUT_IN_SEC = int(os.getenv('TIMEOUT'))


class BaseApi:
    def __init__(self) -> None:
        self._base_url = self.get_url()
        self._headers = self.create_headers()
        self.fake = Faker()

    def get_url(self, uri: str=None):
        if uri is None:
            self._base_url = API_ROOT
        else:
            self._base_url = API_ROOT + uri
        
        return self._base_url

    def create_headers(self):
        self._headers = None

    # GET
    def get(self, endpoint, headers=None, params=None, **kwargs):
        return self.__handle_request(endpoint=endpoint, method=HttpMethod.GET, headers=headers, params=params, **kwargs)
    
    # POST
    def post(self, endpoint, headers=None, data=None, json=None, **kwargs):
        return self.__handle_request(endpoint=endpoint, method=HttpMethod.POST, headers=headers, data=data, json=json, **kwargs)

    # PUT
    def put(self, endpoint, headers=None, data=None, json=None, **kwargs):
        return self.__handle_request(endpoint=endpoint, method=HttpMethod.PUT, headers=headers, data=data, json=json, **kwargs)

    # PATCH
    def patch(self, endpoint, headers=None, data=None, json=None, **kwargs):
        return self.__handle_request(endpoint=endpoint, method=HttpMethod.PATCH, headers=headers, data=data, json=json, **kwargs)

    # DELETE
    def delete(self, endpoint, headers=None, **kwargs):
        return self.__handle_request(endpoint=endpoint, method=HttpMethod.DELETE, headers=headers, **kwargs)

    # Handle request
    def __handle_request(self, endpoint, method, headers=None, params=None, data=None, json=None, **kwargs):
        url = self._base_url + endpoint
        
        if headers is None:
            headers = self._headers
        
        cookies = dict(**kwargs).get('cookies')
        timeout = dict(**kwargs).get('timeout')

        if cookies is None:
            cookies = {}
        
        if timeout is None:
            timeout = MAX_TIMEOUT_IN_SEC
        
        if method == HttpMethod.GET:
            return requests.get(url=url, headers=headers, params=params, cookies=cookies, timeout=timeout)
        
        if method == HttpMethod.POST:
            return requests.post(url=url, headers=headers, data=data, json=json, cookies=cookies, timeout=timeout)

        if method == HttpMethod.PUT:
            return requests.put(url=url, headers=headers, data=data, json=json, cookies=cookies, timeout=timeout)

        if method == HttpMethod.PATCH:
            return requests.patch(url=url, headers=headers, data=data, json=json, cookies=cookies, timeout=timeout)

        if method == HttpMethod.DELETE:
            return requests.delete(url=url, headers=headers, data=data, json=json, cookies=cookies, timeout=timeout)
