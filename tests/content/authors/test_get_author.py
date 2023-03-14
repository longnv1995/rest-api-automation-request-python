import allure

from libs.assertions import Assertions
from libs.api.content.author_client import AuthorClient
from text_resources.author_error import *
from text_resources.common_error import *

from utils.helpers import get_first_item_of_list, get_value_of_key_in_dict


AuthorAPI = AuthorClient()


@allure.epic('CD - Authors')
@allure.story('CD: GET - Allowed customer to get authors')
class TestGetAuthor:
    @allure.severity(allure.severity_level.NORMAL)
    def test_list_authors_should_be_returned_when_get_list_authors(self):
        # Act
        get_authors_res = AuthorAPI.list_authors(params={'limit': 'all'})

        # Assert
        Assertions.ok(get_authors_res)
        Assertions.each_item_is_valid_schema(get_authors_res, 'author.json')
        Assertions.response_contains_meta_obj(get_authors_res)
    
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_author_should_be_returned_when_get_author_by_id(self):
        # Arrange
        get_list_authors_res = AuthorAPI.list_authors()
        Assertions.ok(get_list_authors_res)
        Assertions.not_empty(get_list_authors_res)
        get_first_author_res = get_first_item_of_list(get_list_authors_res)
        author_id = get_value_of_key_in_dict('id', get_first_author_res)

        # Act
        get_author_res = AuthorAPI.get_author_by_id(author_id)

        # Assert
        Assertions.ok(get_author_res)
        Assertions.valid_schema(get_author_res, 'author.json')

    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_author_should_be_returned_when_get_author_by_slug(self):
        # Arrange
        get_list_authors_res = AuthorAPI.list_authors()
        Assertions.ok(get_list_authors_res)
        Assertions.not_empty(get_list_authors_res)
        get_first_author_res = get_first_item_of_list(get_list_authors_res)
        author_slug = get_value_of_key_in_dict('slug', get_first_author_res)

        # Act
        get_author_res = AuthorAPI.get_author_by_slug(author_slug)

        # Assert
        Assertions.ok(get_author_res)
        # Assertions.valid_schema(get_author_res, 'author.json')

    @allure.severity(allure.severity_level.NORMAL)
    def test_no_author_should_be_returned_when_get_author_by_random_slug(self, random_slug):
        # Act
        get_author_res = AuthorAPI.get_author_by_slug(random_slug)

        # Arrange
        Assertions.not_found(get_author_res,
                                message=not_found_cannot_read_author_msg,
                                context=not_found_author_context,
                                type=not_found_error_type)
        
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_author_should_be_returned_when_get_author_includes_count_posts(self):
        # Arrange
        get_list_authors_res = AuthorAPI.list_authors()
        Assertions.ok(get_list_authors_res)
        Assertions.not_empty(get_list_authors_res)
        get_first_author_res = get_first_item_of_list(get_list_authors_res)
        author_id = get_value_of_key_in_dict('id', get_first_author_res)
        params = {'include': 'count.posts'}

        # Act
        get_author_res = AuthorAPI.get_author_by_id(author_id, params=params)

        # Assert
        Assertions.ok(get_author_res)
        count_posts = get_author_res.json()['authors'][0]['count']['posts']
        Assertions.greater_than_zero(count_posts)

