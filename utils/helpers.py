from random import randint
from requests import Response
from pprint import pprint
from constants import RESOURCE_KEYS


def is_valid_json(response: Response):
        if not response.json():
            raise TypeError(f"Response is not a valid JSON format. Response text: {response.text}")
        
        return True

def is_valid_dict(obj: dict):
        if not isinstance(obj, dict):
            raise TypeError(f"Not a valid dictionary. Object is: {obj}")
        
        return True

def pprint_format(response: Response):
    is_valid_json(response)
    print('\n')
    return pprint(response.json(), indent=4)

def array_items(response: Response):
    is_valid_json(response)
    res_as_dict = response.json()
    # Get a source type: posts, tiers, users...
    source_type = list(res_as_dict.keys())[0] 
    if source_type not in RESOURCE_KEYS:
        raise ValueError(f'Resource not found. Available resources: {RESOURCE_KEYS}')
    
    return res_as_dict[source_type]

def get_key(key: str, response: Response):
    items = array_items(response)
    if items is None:
        assert False, f'Not found key: {key} in response. Response is {response.text}'
    
    assert len(items) == 1
    return items[len(items)-1][key]

    # is_valid_json(response)
    # res_as_dict = response.json()
    # # Get first key in dict is the resource such as: posts, tiers, users...
    # source_type = list(res_as_dict.keys())[0] 
    # print(source_type)

    # if key not in res_as_dict[source_type][0].keys():
    #     raise KeyError(f"Not found key: '{key}' in response. Resource is: {source_type}")
    
def get_value_of_key_in_dict(key: str, obj: dict):
    is_valid_dict(obj)

    if key not in list(obj.keys()):
        raise KeyError(f"Not found key: '{key}' in {obj}")

    return obj[key]

def get_first_item_of_list(reponse: Response):
    items = array_items(reponse)
    if items is None:
        assert False, 'Empty list'
    
    return items[0]

def get_random_item_of_list(response: Response):
    items = array_items(response)

    if items is None:
        assert False, 'Empty list'
    
    if len(items) == 1:
        return items[len(items)-1]
    else:
        random_order = randint(0, len(items))
        return items[random_order]

     
