import pytest
import allure

from libs.assertions import Assertions
from libs.api.admin.tag_admin import TagAdmin
from libs.models.tag import Tag
from text_resources.tag_error import *
from text_resources.common_error import *
from utils.helpers import get_key


TagAPI = TagAdmin()


@allure.epic('CMA - Tags')
@allure.story('CMA: GET - Allowed customer to get tags')
class TestGetTag:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_all_tags_should_be_returned_when_get_list_tags(self):
        # Act
        params = {'limit': 'all'}
        get_tags_res = TagAPI.list_tags(params=params)

        # Assert
        Assertions.ok(get_tags_res)
        Assertions.each_item_is_valid_schema(get_tags_res, 'tag.json')
        Assertions.response_contains_meta_obj(get_tags_res)

    @allure.severity(allure.severity_level.NORMAL)
    def test_matches_tags_should_be_returned_when_filter_by_visibility(self, visibility):
        # Arrange
        params = {'filter': 'visibility:' + visibility}

        # Act
        get_tags_res = TagAPI.list_tags(params=params)

        # Assert
        Assertions.ok(get_tags_res)
        Assertions.each_item_is_valid_schema(get_tags_res, 'tag.json')

    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_tag_should_be_returned_when_get_tag_by_id(self, make_tag):
        # Arrange
        tag = Tag(name=TagAPI.fake.name())
        create_tag_res, id = make_tag(tag)
        Assertions.created(create_tag_res)

        # Act
        get_tag_res = TagAPI.get_tag_by_id(id)

        # Assert
        Assertions.ok(get_tag_res)
        Assertions.valid_schema(get_tag_res, 'tag.json')

    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_tag_should_be_returned_when_get_tag_by_slug(self, make_tag):
        # Arrange
        tag = Tag(name=TagAPI.fake.name())
        create_tag_res, id = make_tag(tag)
        Assertions.created(create_tag_res)
        tag_slug = get_key('slug', create_tag_res)

        # Act
        get_tag_res = TagAPI.get_tag_by_slug(tag_slug)

        # Arrange
        Assertions.ok(get_tag_res)
        Assertions.valid_schema(get_tag_res, 'tag.json')

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('random_tag_id', [-1, 0, 9999999])
    def test_no_tag_should_be_returned_when_get_tag_by_random_id(self, random_tag_id):
        # Act
        get_tag_res = TagAPI.get_tag_by_id(random_tag_id)

        # Assert
        Assertions.unprocessable_entity(get_tag_res, 
                                            message=validation_cannot_read_tag_msg,
                                            context=validation_cannot_read_source_by_id_context,
                                            type=validation_error_type)
        
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('random_slug', ["str1-str2", "random", "1", "page1-2", "a_b"])
    def test_no_tag_should_be_returned_when_get_tag_by_random_slug(self, random_slug):
        # Act
        get_tag_res = TagAPI.get_tag_by_slug(random_slug)

        # Assert
        Assertions.not_found(get_tag_res, 
                                message=not_found_cannot_read_tag_msg,
                                context=not_found_tag_context,
                                type=not_found_error_type)


