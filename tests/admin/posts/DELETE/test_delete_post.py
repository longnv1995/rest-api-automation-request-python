import allure

from libs.assertions import Assertions
from libs.api.admin.post_admin import PostAdmin
from libs.models.post import Post
from text_resources.post_error import *
from text_resources.common_error import *
from utils.helpers import get_key


PostAPI = PostAdmin()

@allure.epic('CMA - Posts')
@allure.story('CMA: DELETE - Allowed customer to delete posts')
class TestDeletePost:
    def test_post_should_be_deleted_when_delete_post_by_id(self, make_post):
        # Arrange: Create a post
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        del_post_res = PostAPI.delete_post_by_id(id)

        # Assertion
        Assertions.no_content(del_post_res)
        get_deleted_post_res = PostAPI.get_post_by_id(id)
        Assertions.not_found(get_deleted_post_res, 
                                          message=not_found_cannot_read_post_msg, 
                                          context=not_found_post_context, 
                                          type=not_found_error_type)

    def test_post_should_be_deleted_when_delete_post_by_slug(self, make_post):
        # Arrange: Create a post
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        post_slug = get_key('slug', create_post_res)

        # Act
        del_post_res = PostAPI.delete_post_by_slug(post_slug)

        # Assert
        Assertions.unprocessable_entity(del_post_res, 
                                                     message=validation_cannot_delete_post_msg, 
                                                     context=validation_cannot_read_source_by_id_context, 
                                                     type=validation_error_type)
        
        get_deleted_post_res = PostAPI.get_post_by_slug(post_slug)
        Assertions.ok(get_deleted_post_res)

    def test_post_should_not_be_deleted_when_delete_post_by_random_id(self, invalid_id):
        # Act
        del_post_res = PostAPI.delete_post_by_id(invalid_id)

        # Assert
        Assertions.unprocessable_entity(del_post_res, 
                                                     message=validation_cannot_delete_post_msg, 
                                                     context=validation_cannot_read_source_by_id_context, 
                                                     type=validation_error_type)
       

    