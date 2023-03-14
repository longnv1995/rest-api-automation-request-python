import pytest
import allure

from libs.assertions import *
from libs.api.admin.tag_admin import TagAdmin
from libs.models.tag import Tag
from text_resources.tag_error import *
from text_resources.common_error import *
from utils.helpers import get_key


TagAPI = TagAdmin()


@allure.epic('CMA - Tags')
@allure.story('CMA: GET - Allowed customer to modify tags')
class TestUpdateTag:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tag_should_be_saved_when_update_tag_by_valid_name(self, make_tag):
        # Arrange
        tag = Tag(name=TagAPI.fake.name())
        create_tag_res, tag_id = make_tag(tag)
        Assertions.created(create_tag_res)

        # Act
        update_tag_name = 'newname'
        update_tag_payload = {
            'tags': [
                {
                    'name': update_tag_name,
                    'updated_at': '2023-06-05T20:52:37.000Z'
                }
            ]
        }
        update_tag_res = TagAPI.put_tag(tag_id, json=update_tag_payload)
        Assertions.ok(update_tag_res)
        get_new_tag_name = get_key('name', update_tag_res)
        Assertions.equal(update_tag_name, get_new_tag_name)
    
    @allure.severity(allure.severity_level.NORMAL)
    def test_tag_should_be_saved_when_update_tag_name_by_other_existing_tag_name(self, make_tag):
        # Arrange
        first_tag_name = 'first tag'
        tag_one = Tag(name=first_tag_name)
        create_first_tag_res, first_tag_id = make_tag(tag_one)
        Assertions.created(create_first_tag_res)

        second_tag_name = 'second tag'
        tag_two = Tag(name=second_tag_name)
        create_second_tag_res, second_tag_id = make_tag(tag_two)
        Assertions.created(create_second_tag_res)

        # Act
        update_second_tag_payload = {
            'tags': [
                {
                    'name': first_tag_name,
                    'updated_at': '2023-06-05T20:52:37.000Z'
                }
            ]
        }
        update_second_tag_res = TagAPI.put_tag(second_tag_id, json=update_second_tag_payload)

        # Assertion
        Assertions.ok(update_second_tag_res)
        get_second_tag_name = get_key('name', update_second_tag_res)
        Assertions.equal(get_second_tag_name, first_tag_name)

    @allure.severity(allure.severity_level.NORMAL)
    def test_tag_should_be_saved_when_update_slug_tag_by_other_existing_slug_tag(self, make_tag):
        # Arrange
        first_tag_name = 'first tag'
        tag_one = Tag(name=first_tag_name)
        create_first_tag_res, first_tag_id = make_tag(tag_one)
        Assertions.created(create_first_tag_res)
        first_tag_slug = get_key('slug', create_first_tag_res)

        second_tag_name = 'second tag'
        tag_two = Tag(name=second_tag_name)
        create_second_tag_res, second_tag_id = make_tag(tag_two)
        Assertions.created(create_second_tag_res)

        # Act
        update_second_tag_payload = {
            'tags': [
                {
                    'slug': first_tag_slug,
                    'updated_at': '2023-06-05T20:52:37.000Z'
                }
            ]
        }
        update_second_tag_res = TagAPI.put_tag(second_tag_id, json=update_second_tag_payload)

        # Assertion
        Assertions.ok(update_second_tag_res)
        get_second_tag_slug = get_key('slug', update_second_tag_res)
        Assertions.not_equal(get_second_tag_slug, first_tag_slug)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        'tag_name', 
        ["", None],
        ids=["empty", "null"])
    def test_tag_should_not_be_saved_when_update_tag_by_invalid_tag_name(self, make_tag, tag_name):
        # Arrange
        tag = Tag(name=TagAPI.fake.name())
        create_tag_res, id = make_tag(tag)
        Assertions.created(create_tag_res)

        # Act
        update_second_tag_payload = {
            'tags': [
                {
                    'name': tag_name,
                    'updated_at': '2023-06-05T20:52:37.000Z'
                }
            ]
        }

        update_tag_res = TagAPI.put_tag(id, json=update_second_tag_payload)

        # Assert
        Assertions.unprocessable_entity(update_tag_res, 
                                            message=validation_cannot_edit_tag_msg,
                                            context=validation_failed_for_name_context,
                                            type=validation_error_type)


