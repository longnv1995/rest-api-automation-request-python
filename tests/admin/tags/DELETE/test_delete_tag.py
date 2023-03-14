import pytest
import allure

from libs.assertions import Assertions
from libs.api.admin.tag_admin import TagAdmin
from libs.models.post import Post
from libs.models.tag import Tag
from text_resources.tag_error import *
from text_resources.common_error import *
from utils.helpers import get_key


TagAPI = TagAdmin()


@allure.epic('CMA - Tags')
@allure.story('CMA: DELETE - Allowed customer to delete tags')
class TestDeleteTag:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tag_should_be_deleted_when_delete_tag_by_id(self, make_tag):
        # Arrange: Create a tag
        tag = Tag(name=TagAPI.fake.sentence())
        create_tag_res, id = make_tag(tag)
        Assertions.created(create_tag_res)

        # Act
        del_tag_res = TagAPI.delete_tag_by_id(id)

        # Assert
        Assertions.no_content(del_tag_res)
        get_deleted_tag_res = TagAPI.get_tag_by_id(id)
        Assertions.not_found(get_deleted_tag_res, 
                                          message=not_found_cannot_read_tag_msg,
                                          context=not_found_tag_context, 
                                          type=not_found_error_type)

    @allure.severity(allure.severity_level.NORMAL)
    def test_tag_should_be_deleted_when_delete_tag_by_slug(self, make_tag):
        # Arrange: Create a tag
        tag = Tag(name=TagAPI.fake.name())
        create_tag_res, id = make_tag(tag)
        Assertions.created(create_tag_res)
        tag_slug = get_key('slug', create_tag_res)

        # Act
        del_tag_res = TagAPI.delete_tag_by_slug(tag_slug)

        # Assert
        Assertions.unprocessable_entity(del_tag_res, 
                                                     message=validation_cannot_delete_tag_msg,
                                                     context=validation_cannot_read_source_by_id_context,
                                                     type=validation_error_type)
        
        get_deleted_tag_res = TagAPI.get_tag_by_slug(tag_slug)
        Assertions.ok(get_deleted_tag_res)

    @allure.severity(allure.severity_level.NORMAL)
    def test_no_tag_should_be_deleted_when_delete_tag_by_random_id(self, invalid_id):
        # Act
        del_tag_res = TagAPI.delete_tag_by_id(invalid_id)

        # Assert
        Assertions.unprocessable_entity(del_tag_res, 
                                                     message=validation_cannot_delete_tag_msg,
                                                     context=validation_cannot_read_source_by_id_context,
                                                     type=validation_error_type)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('random_slug', ["str1-str2", "random", "1-2", "page1-2", "a_b"])
    def test_no_tag_should_be_deleted_when_delete_tag_by_random_slug(self, random_slug):
        # Act
        del_tag_res = TagAPI.delete_tag_by_slug(random_slug)

        # Assert
        Assertions.unprocessable_entity(del_tag_res, 
                                                     message=validation_cannot_delete_tag_msg,
                                                     context=validation_cannot_read_source_by_id_context,
                                                     type=validation_error_type)

    @allure.severity(allure.severity_level.CRITICAL)    
    def test_tag_should_be_deleted_when_delete_tag_is_being_used_by_post(self, make_post):
        # Arrange
        post = Post(title='a nice post', tags=['one-tag'])
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        
        tags = get_key('tags', create_post_res)
        tag_id = tags[0]['id']

        # Act
        del_tag_res = TagAPI.delete_tag_by_id(tag_id)

        # Assert
        Assertions.no_content(del_tag_res)
        get_deleted_tag_res = TagAPI.get_tag_by_id(tag_id)
        Assertions.not_found(get_deleted_tag_res, 
                                          message=not_found_cannot_read_tag_msg,
                                          context=not_found_tag_context, 
                                          type=not_found_error_type)


