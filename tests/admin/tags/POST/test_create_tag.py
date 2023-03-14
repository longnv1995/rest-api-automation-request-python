import pytest
import allure

from libs.assertions import Assertions
from libs.api.admin.tag_admin import TagAdmin
from libs.models.tag import Tag
from text_resources.tag_error import *
from text_resources.common_error import *
from utils.custom_enums import TagVisibility
from utils.helpers import get_key


TagApi = TagAdmin()

@allure.epic('CMA - Tags')
@allure.story('CMA: GET - Allowed customer to create tags')
class TestCreateTag:
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('tag_name, visibility',
        [
            ('public-tag', TagVisibility.PUBLIC.value),
            ('#internal-tag', TagVisibility.INTERNAL.value)
        ]
    )
    def test_tag_should_be_saved_when_create_tag_with_valid_name(self, make_tag, tag_name, visibility):
        # Arrange
        tag = Tag(name=tag_name)

        # Act
        create_tag_res, id = make_tag(tag)

        # Assert
        Assertions.created(create_tag_res)
        get_created_tag_res = TagApi.get_tag_by_id(id)
        Assertions.ok(get_created_tag_res)
        Assertions.response_contains_entry(get_created_tag_res, {'name': tag_name})
        Assertions.response_contains_entry(get_created_tag_res, {'visibility': visibility})

    @allure.severity(allure.severity_level.CRITICAL)
    def test_tag_should_be_saved_when_create_tag_by_valid_name_and_description(self, make_tag):
        # Arrange
        tag_name = TagApi.fake.name()
        tag_desc = TagApi.fake.sentence()
        tag = Tag(name=tag_name, description=tag_desc)

        # Act
        create_tag_res, id = make_tag(tag)

        # Assert
        Assertions.created(create_tag_res)
        get_created_tag_res = TagApi.get_tag_by_id(id)
        Assertions.ok(get_created_tag_res)
        Assertions.response_contains_entry(get_created_tag_res, {'name': tag_name})
        Assertions.response_contains_entry(get_created_tag_res, {'description': tag_desc})

    @allure.severity(allure.severity_level.NORMAL)
    def test_tag_should_be_saved_when_create_tag_by_existent_tag_name(self, make_tag):
        # Arrange
        tag = Tag(name=TagApi.fake.name())
        
        create_first_tag_res, first_tag_id = make_tag(tag)
        Assertions.created(create_first_tag_res)
        first_slug_tag = get_key('slug', create_first_tag_res)

        # Act
        create_second_tag_res, second_tag_id = make_tag(tag)

        # Assert
        Assertions.created(create_second_tag_res)
        second_slug_tag = get_key('slug', create_second_tag_res)
        Assertions.not_equal(second_slug_tag, first_slug_tag)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_tag_should_be_saved_when_create_tag_by_existent_slug_tag(self, make_tag):
        # Arrange
        tag_name = TagApi.fake.name()
        tag = Tag(name=tag_name)
        create_first_tag_res, first_tag_id = make_tag(tag)
        Assertions.created(create_first_tag_res)
        first_tag_slug = get_key('slug', create_first_tag_res)

        # Act
        create_second_tag_res, second_tag_id = make_tag(tag)

        # Assert
        Assertions.created(create_second_tag_res)
        second_tag_slug = get_key('slug', create_second_tag_res)
        second_tag_name = get_key('name', create_second_tag_res)
        Assertions.equal(second_tag_name, tag_name)
        Assertions.not_equal(second_tag_slug, first_tag_slug)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        'tag_name', 
        ["", None],
        ids=["empty", "null"])
    def test_no_tag_should_be_saved_when_create_tag_with_invalid_tag_name(self, make_tag, tag_name):
        # Arrange
        tag = Tag(name=tag_name)

        # Act
        create_tag_res, id = make_tag(tag)

        # Assert
        Assertions.unprocessable_entity(create_tag_res, 
                                            message=validation_cannot_save_tag_msg,
                                            context=validation_failed_for_name_context,
                                            type=validation_error_type)        

        
