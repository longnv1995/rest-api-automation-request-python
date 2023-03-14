from http import HTTPStatus
import json
from jsonschema import validate
from requests import Response
from assertpy import assert_that
from pathlib import Path

from utils.helpers import is_valid_json, array_items


class Assertions:
    @classmethod
    def __verify_status_code(cls, response: Response, expected_code: HTTPStatus):
        is_valid_json(response)

        assert expected_code == response.status_code, \
            f"Expected result: {expected_code}, but actual: {response.status_code}"
        
    @classmethod
    def __verify_error_object(cls, response: Response, message: str, 
            context: str=None, type: str=None, code: int=None, **kwargs):

        res_as_dict = response.json()['errors'][0]

        if message in res_as_dict['message']:
            assert True
        else:
            assert False, f"Expected result: {message}, but actual: {res_as_dict['message']}"

        if context is not None:
            if context in res_as_dict['context']:
                assert True
            else:
                assert False, f"Expected result: {context}, but actual: {res_as_dict['context']}"

        if type is not None:
            assert type == res_as_dict['type'], \
            f"Expected result: {type}, but actual: {res_as_dict['type']}"

        if code is not None:
            assert code == res_as_dict['code'], \
            f"Expected result: {code}, but actual: {res_as_dict['code']}"

    @classmethod
    def __load_schema_file(cls, source_file):
        absolute_path = Path.joinpath(Path.cwd(), 'schemas', source_file)
        
        with open(absolute_path) as src_file:
            return json.load(src_file)
        
    # Status code: OK - 200
    @staticmethod
    def ok(response):
        Assertions.__verify_status_code(response, HTTPStatus.OK)

    # Status code: CREATED - 201
    @staticmethod
    def created(response: Response):
        Assertions.__verify_status_code(response, HTTPStatus.CREATED)

    # Status code: NO CONTENT - 204
    @staticmethod
    def no_content(response: Response):
        assert HTTPStatus.NO_CONTENT == response.status_code, \
            f"Expected result: {HTTPStatus.NO_CONTENT}, but actual: {response.status_code}"
    
    # Status code: BAD REQUEST - 400
    @staticmethod
    def bad_request(response: Response, 
                                message: str=None, context: str=None, type: str=None, code: int=None, **kwargs):
        Assertions.__verify_status_code(response, HTTPStatus.BAD_REQUEST)
        if message is not None:
            Assertions.__verify_error_object(response, message=message, context=context, type=type, code=code, **kwargs)
    
    # Status code: NOT FOUND - 404
    @staticmethod
    def not_found(response: Response, 
                                message: str=None, context: str=None, type: str=None, code: int=None, **kwargs):
        Assertions.__verify_status_code(response, HTTPStatus.NOT_FOUND)
        if message is not None:
            Assertions.__verify_error_object(response, message=message, context=context, type=type, code=code, **kwargs)

    # Status code: FORBIDDEN - 403
    @staticmethod
    def forbidden(response: Response, 
                                message: str=None, context: str=None, type: str=None, code: int=None, **kwargs):
        Assertions.__verify_status_code(response, HTTPStatus.FORBIDDEN)
        if message is not None:
            Assertions.__verify_error_object(response, message=message, context=context, type=type, code=code, **kwargs)

    # Status code: UNPROCESSABLE_ENTITY - 422
    @staticmethod
    def unprocessable_entity(response: Response, 
                                message: str=None, context: str=None, type: str=None, code: int=None, **kwargs):
        Assertions.__verify_status_code(response, HTTPStatus.UNPROCESSABLE_ENTITY)
        if message is not None:
            Assertions.__verify_error_object(response, message=message, context=context, type=type, code=code, **kwargs)

    # Status code: CONFLICT - 409
    @staticmethod
    def conflict(response: Response, 
                            message: str=None, context: str=None, type: str=None, code: int=None, **kwargs):
        Assertions.__verify_status_code(response, HTTPStatus.CONFLICT)
        if message is not None:
            Assertions.__verify_error_object(response, message=message, context=context, type=type, code=code, **kwargs)

    # Status code: INTERNAL SERVER ERROR - 500
    def internal_server_error(response: Response, 
                            message: str=None, context: str=None, type: str=None, code: int=None, **kwargs):
        Assertions.__verify_status_code(response, HTTPStatus.INTERNAL_SERVER_ERROR)
        if message is not None:
            Assertions.__verify_error_object(response, message=message, context=context, type=type, code=code, **kwargs)

    # Value assertion
    @staticmethod
    def response_contains_entry(response: Response, entry):
        items = array_items(response)
        if items is None:
            assert False, f"No item found in the response. Response is: {response}"
        
        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items) - 1]).contains_entry(entry)

    @staticmethod
    def each_item_contains_entry(response: Response, entry):
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            assert_that(item).contains_entry(entry)

    @staticmethod
    def response_contains_key(response: Response, key):
        items = array_items(response)
        if items is None:
            assert True

        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items) - 1]).contains_key(key)

    @staticmethod
    def response_contains_keys(response: Response, keys):
        items = array_items(response)
        if items is None:
            assert True

        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items)-1]).contains_key(*keys)

    @staticmethod
    def response_contains_meta_obj(response: Response):
        is_valid_json(response)
        res_as_dict = response.json()
        
        if 'meta' not in list(res_as_dict.keys()):
            raise KeyError(f"Not found key: 'meta' in response. Response is {res_as_dict}")
        
        meta_obj = res_as_dict['meta']
        meta_schema = Assertions.__load_schema_file('meta.json')
        validate(meta_obj, meta_schema)
        # also need to check 'pages' is greater than or equal to 'page' value
        # ex: total = 2 pages, if http://localhost/posts?page=2 -> page = 2 == pages

    @staticmethod
    def each_item_contains_key(response: Response, key):
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            assert_that(item).contains_key(key)

    @staticmethod
    def each_item_contains_keys(response: Response, keys):
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            assert_that(item).contains_key(*keys)

    @staticmethod
    def response_contains_value(response: Response, value):
        items = array_items(response)
        if items is None:
            assert True

        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items)-1]).contains_value(value)
    
    @staticmethod
    def each_item_contains_value(response: Response, value):
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            assert_that(item).contains_value(value)

    @staticmethod
    def response_does_not_contain_entry(response: Response, entry):
        items = array_items(response)
        if items is None:
            assert True
        
        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items)-1]).does_not_contain_entry(entry)
            
    @staticmethod
    def each_item_does_not_contain_entry(response: Response, entry):
        items = array_items(response)
        if items is None:
            assert True
        
        for item in items:
            assert_that(item).does_not_contain_entry(entry)

    @staticmethod
    def response_does_not_contain_key(response: Response, key):
        items = array_items(response)
        if items is None:
            assert True
        
        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items)-1]).does_not_contain_key(key)
            
    @staticmethod
    def each_item_does_not_contain_key(response: Response, key):
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            assert_that(item).does_not_contain_key(key)

    @staticmethod
    def response_does_not_contain_value(response: Response, value):
        items = array_items(response)
        if items is None:
            assert True
        
        assert_that(len(items)).is_equal_to(1)
        assert_that(items[len(items)-1]).does_not_contain_value(value)
    
    @staticmethod
    def each_item_does_not_contain_value(response: Response, value):
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            assert_that(item).does_not_contain_value(value)
            
    @staticmethod
    def valid_schema(response: Response, schema_file):
        schema = Assertions.__load_schema_file(schema_file)
        items = array_items(response)
        if items is None:
            assert True

        assert_that(len(items)).is_equal_to(1)
        validate(items[len(items)-1], schema)

    @staticmethod
    def each_item_is_valid_schema(response: Response, schema_file):
        schema = Assertions.__load_schema_file(schema_file)
        items = array_items(response)
        if items is None:
            assert True

        for item in items:
            validate(item, schema)

    @staticmethod
    def empty_list(response: Response):
        items = array_items(response)
        assert_that(len(items)).is_equal_to(0)

    @staticmethod
    def total_items(response: Response, expected_value):
        list_items = array_items(response)
        assert_that(len(list_items)).is_equal_to(expected_value)
        
    @staticmethod
    def not_empty(response: Response):
        items = array_items(response)
        assert_that(items).is_not_empty()

    @staticmethod
    def equal(expected_result, actual_result):
        assert_that(expected_result).is_equal_to(actual_result)

    @staticmethod
    def not_equal(expected_result, actual_result):
        assert_that(expected_result).is_not_equal_to(actual_result)

    @staticmethod
    def number(value):
        assert_that(value).is_instance_of(int)

    @staticmethod
    def greater_than_zero(value):
        assert_that(value).is_instance_of(int).is_greater_than(0)

    @staticmethod
    def string(value):
        assert_that(value).is_instance_of(str)