import allure

from libs.assertions import Assertions
from libs.api.content.tag_client import TagClient
from text_resources.tag_error import *
from text_resources.common_error import *

from utils.helpers import get_first_item_of_list, get_random_item_of_list, get_value_of_key_in_dict


TagAPI = TagClient()


@allure.epic('CD - Tags')
@allure.story('CD: GET - Allowed customer to get tags')
class TestGetTag:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_all_published_tags_should_be_returned_when_get_list_tags(self):
        # Act
        get_tags_res = TagAPI.list_tags(params={'limit': 'all'})

        # Assert
        Assertions.ok(get_tags_res)
        Assertions.each_item_is_valid_schema(get_tags_res, 'tag.json')
        Assertions.response_contains_meta_obj(get_tags_res)
    
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_tag_should_be_returned_when_get_tag_by_id(self):
        # Arrange
        get_list_tags_res = TagAPI.list_tags()
        Assertions.ok(get_list_tags_res)
        Assertions.not_empty(get_list_tags_res)
        get_first_tag_res = get_first_item_of_list(get_list_tags_res)
        tag_id = get_value_of_key_in_dict('id', get_first_tag_res)

        # Act
        get_tag_res = TagAPI.get_tag_by_id(tag_id)

        # Assert
        Assertions.ok(get_tag_res)
        Assertions.valid_schema(get_tag_res, 'tag.json')
    
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_tag_should_be_returned_when_get_tag_by_slug(self):
        # Arrange
        get_list_tags_res = TagAPI.list_tags()
        Assertions.ok(get_list_tags_res)
        Assertions.not_empty(get_list_tags_res)
        get_first_tag_res = get_first_item_of_list(get_list_tags_res)
        tag_slug = get_value_of_key_in_dict('slug', get_first_tag_res)

        # Act
        get_tag_res = TagAPI.get_tag_by_slug(tag_slug)

        # Assert
        Assertions.ok(get_tag_res)

    @allure.severity(allure.severity_level.NORMAL)
    def test_no_tag_should_be_returned_when_get_tag_by_random_slug(self, random_slug):
        # Act
        get_tag_res = TagAPI.get_tag_by_slug(random_slug)

        # Arrange
        Assertions.not_found(get_tag_res,
                                message=not_found_cannot_read_tag_msg,
                                context=not_found_tag_context,
                                type=not_found_error_type)
        
    @allure.severity(allure.severity_level.NORMAL)
    def test_one_tag_should_be_returned_when_get_tag_include_count_posts(self):
        # Arrange
        get_list_tags_res = TagAPI.list_tags()
        Assertions.ok(get_list_tags_res)
        Assertions.not_empty(get_list_tags_res)
        get_first_tag_res = get_first_item_of_list(get_list_tags_res)
        tag_id = get_value_of_key_in_dict('id', get_first_tag_res)
        params = {'include': 'count.posts'}

        # Act
        get_tag_res = TagAPI.get_tag_by_id(tag_id, params=params)

        # Assert
        Assertions.ok(get_tag_res)
        count_posts = get_tag_res.json()['tags'][0]['count']['posts']
        Assertions.greater_than_zero(count_posts)

