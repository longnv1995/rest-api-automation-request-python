import pytest
import allure

from libs.assertions import *
from libs.api.admin.post_admin import PostAdmin
from libs.models.post import Post
from text_resources.post_error import *
from text_resources.common_error import *
from utils.helpers import get_key
from utils.times import passed_time, current_time, future_time


PostAPI = PostAdmin()


@allure.epic('CMA - Posts')
@allure.story('CMA: PUT - Allowed customer to modify posts')
class TestUpdatePost:
    @pytest.mark.skip("Not allowed to create new resource with PUT method")
    def test_post_should_not_be_saved_when_update_post_by_valid_title(self):
        pass

    def test_post_should_be_saved_when_update_post_by_valid_title(self, make_post):
        # Arrange: Create a post
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        new_title = PostAPI.fake.sentence()
        update_post_payload = {
            "posts": [
                {
                    "title": new_title,
                    "updated_at": updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.ok(update_post_res)
        Assertions.valid_schema(update_post_res, 'post.json')
        Assertions.response_contains_entry(update_post_res, {'title': new_title})

    def test_post_should_be_saved_when_update_post_from_draft_to_published_status(self, make_post, published_status):
        # Arrange: create post in draft status by default
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            "posts": [
                {
                    "status": published_status,
                    "updated_at": updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.ok(update_post_res)
        Assertions.response_contains_entry(update_post_res, {'status': published_status})

    def test_post_should_be_saved_when_update_post_from_draft_to_scheduled_status(self, make_post, scheduled_status):
        # Arrange: create post in draft status by default
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        updated_at = get_key('updated_at', create_post_res)
        published_at = future_time()
        update_post_payload = {
            "posts": [
                {
                    "status": scheduled_status,
                    "updated_at": updated_at,
                    "published_at": published_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.ok(update_post_res)
        Assertions.response_contains_entry(update_post_res, {'status': scheduled_status})
        Assertions.response_contains_entry(update_post_res, {'published_at': published_at})

    @pytest.mark.parametrize(
        'updated_at', 
        [
            '07/05/2023',
            'str',
            1,
            ''
        ],
        ids = ['not a valid datetime format', 'string', 'number', 'empty']
    )
    def test_post_should_not_be_saved_when_update_post_with_invalid_updated_at(self, make_post, updated_at):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        update_post_payload = {
            "posts": [
                {
                    "title": PostAPI.fake.sentence(),
                    "updated_at": updated_at
                }
            ]
        }
        
        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)
        
        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_updated_at_context,
                                                     type=validation_error_type)

    def test_post_should_not_be_save_when_update_post_with_update_at_is_less_than_created_at(self, make_post):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        update_post_payload = {
            "posts": [
                {
                    "title": PostAPI.fake.sentence(),
                    "updated_at": passed_time()
                }
            ]
        }
        
        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.conflict(update_post_res, 
                                                     message=failed_cannot_save_post_msg,
                                                     context=failed_cannot_save_post_msg,
                                                     type=update_collision_error_type)

    def test_post_should_not_be_saved_when_update_post_without_updated_at_field(self, make_post):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        update_post_payload = {
            "posts": [
                {
                    "title": PostAPI.fake.sentence()
                }
            ]
        }
        
        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_post_context,
                                                     type=validation_error_type)

    def test_post_should_not_be_saved_when_update_non_existing_post_with_valid_title(self, random_guid):
        # Arrange
        update_post_payload = {
            "posts": [
                {
                    'title': PostAPI.fake.sentence(),
                    'updated_at': current_time()
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(random_guid, json=update_post_payload)

        # Assert
        Assertions.not_found(update_post_res, 
                                          message=not_found_cannot_edit_post_msg,
                                          context=not_found_post_context,
                                          type=not_found_error_type)

    @pytest.mark.parametrize('featured', [1, 'true'])
    def test_post_should_not_be_saved_when_update_post_with_invalid_featured(self, make_post, featured):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'featured': featured,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_featured_context,
                                                     type=validation_error_type)

    @pytest.mark.parametrize('status', [1, 'true'])
    def test_post_should_not_be_saved_when_update_post_with_invalid_status(self, make_post, status):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'status': status,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_status_context,
                                                     type=validation_error_type)

    def test_post_should_not_be_saved_when_update_post_with_visibility_is_number(self, make_post):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'visibility': 1,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_visibility_context,
                                                     type=validation_error_type)

    def test_post_should_not_be_saved_when_update_post_with_visibility_is_string(self, make_post):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'visibility': 'str',
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.internal_server_error(update_post_res, 
                                                      message=server_error_cannot_edit_post_msg,
                                                      context=unexpected_error_context,
                                                      type=server_error_type)

    @pytest.mark.parametrize(
        'tags', 
        [
            {'key': 'value'},
            [{'key': 'value'}]
        ],
        ids=['a dictionary', 'array of dict']
    )
    def test_post_should_not_be_saved_when_update_post_with_invalid_tags(self, make_post, tags):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'tags': tags,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_tags_context,
                                                     type=validation_error_type)

    @pytest.mark.parametrize(
        'author',
        [
            {'key': 'value'},
            [{'key': 'value'}]
        ],
        ids=['a dictionary', 'array of dict']
    )
    def test_post_should_not_be_saved_when_update_post_with_invalid_authors(self, make_post, author):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'authors': author,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_authors_context,
                                                     type=validation_error_type)

    @pytest.mark.parametrize('tiers', 
        [
            1,
            "str"
        ],
        ids=['a number', 'a string']
    )
    def test_post_should_not_be_saved_when_update_post_with_invalid_tiers(self, make_post, tiers):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'tiers': tiers,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_tiers_context,
                                                     type=validation_error_type)

    def test_post_should_not_be_saved_when_update_post_with_invalid_featured_and_status(self, make_post):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'status': False,
                    'featured': 1,
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_featured_context,
                                                     type=validation_error_type)

    def test_post_should_not_be_saved_when_update_post_with_invalid_featured_status_and_tags(self, make_post):
        # Arrange
        post = Post(title=PostAPI.fake.sentence())
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        updated_at = get_key('updated_at', create_post_res)
        update_post_payload = {
            'posts': [
                {
                    'featured': 1,
                    'status': True,
                    'tags': {'key': 'value'},
                    'updated_at': updated_at
                }
            ]
        }

        # Act
        update_post_res = PostAPI.put_post(id, json=update_post_payload)

        # Assert
        Assertions.unprocessable_entity(update_post_res, 
                                                     message=validation_cannot_edit_post_msg,
                                                     context=validation_failed_for_featured_context,
                                                     type=validation_error_type)







