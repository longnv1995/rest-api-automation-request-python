import pytest
import allure

from libs.assertions import Assertions
from libs.api.admin.post_admin import PostAdmin
from libs.models.post import Post, FeatureImage
from text_resources.post_error import *
from text_resources.common_error import *
from utils.helpers import get_key
from utils.times import future_time


PostAPI = PostAdmin()

@allure.epic('CMA - Posts')
@allure.story('CMA: POST - Allowed customer to create posts')
class TestCreatePost:
    def test_post_should_be_saved_when_all_fields_are_populated(self, make_post):
        # Arrange
        feature_image = FeatureImage(image='https://picsum.photos/200/300', 
                                     alt='nice picsum', 
                                     caption='nice picsum')
        
        post = Post(title=PostAPI.fake.sentence(), slug='custom-slug',
            excerpt=PostAPI.fake.text(), feature_image=feature_image, tags=['one-tag'])
        
        # Act
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        Assertions.valid_schema(get_created_post_res, 'post.json')

    def test_post_should_be_saved_when_valid_title_and_tag_are_provided(self, make_post):
        # Arrange
        title = PostAPI.fake.sentence()
        tags = ['one-tag']
        post = Post(title=title, tags=tags)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        list_tags = get_key('tags', get_created_post_res)
        Assertions.equal(1, len(list_tags))
        Assertions.response_contains_entry(get_created_post_res, {'title': title})

    def test_post_should_be_saved_when_valid_title_and_some_tags_are_provided(self, make_post):
        # Arrange
        title = PostAPI.fake.sentence()
        tags = ['first-tag', 'second-tag']
        post = Post(title=title, tags=tags)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        list_tags = get_key('tags', get_created_post_res)
        Assertions.equal(2, len(list_tags))
        Assertions.response_contains_entry(get_created_post_res, {'title': title})

    def test_post_should_be_saved_as_draft_version_when_valid_title_is_provided(self, make_post):
        # Arrange 
        title = PostAPI.fake.sentence()
        post = Post(title=title, tags=['first-tag', 'second-tag'])

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        Assertions.response_contains_entry(get_created_post_res, {'title': title})
        Assertions.response_contains_entry(get_created_post_res, {'status': 'draft'})
    
    def test_post_should_be_saved_when_valid_title_and_draft_status_are_provided(self, make_post, draft_status):
        # Arrange 
        title = PostAPI.fake.sentence()
        post = Post(title=title, status=draft_status)
        
        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        Assertions.response_contains_entry(get_created_post_res, {'title': title})
        Assertions.response_contains_entry(get_created_post_res, {'status': draft_status})

    def test_post_should_be_saved_when_valid_title_and_published_status_are_provided(self, make_post, published_status):
        # Arrange
        title = PostAPI.fake.sentence()
        post = Post(title=title, status=published_status)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        Assertions.response_contains_entry(get_created_post_res, {'title': title})
        Assertions.response_contains_entry(get_created_post_res, {'status': published_status})

    def test_post_should_be_saved_when_valid_title_and_scheduled_status_are_provided(self, make_post, scheduled_status):
        # Arrange
        title = PostAPI.fake.sentence()
        published_at = future_time()
        post = Post(title=title, status=scheduled_status, published_at=published_at)

        # Act
        create_post_res, id = make_post(post)
        
        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        Assertions.response_contains_entry(get_created_post_res, {'title': title})
        Assertions.response_contains_entry(get_created_post_res, {'published_at': published_at})
        Assertions.response_contains_entry(get_created_post_res, {'status': scheduled_status})
        
    @pytest.mark.parametrize('featured', [True, False])
    def test_post_should_be_saved_when_valid_title_and_featured_type_are_provided(self, make_post, featured):
        # Arrange
        title = PostAPI.fake.sentence()
        post = Post(title=title, featured=featured)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.created(create_post_res)
        get_created_post_res = PostAPI.get_post_by_id(id)
        Assertions.ok(get_created_post_res)
        Assertions.response_contains_entry(get_created_post_res, {'title': title})
        Assertions.response_contains_entry(get_created_post_res, {'featured': featured})
    
    def test_post_should_not_be_saved_when_title_is_null(self, make_post):
        # Arrange
        post = Post(title=None)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res, 
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_title_context,
                                                     type=validation_error_type)
        
    def test_post_should_not_be_saved_when_title_contains_only_spaces(self, make_post):
        # Arrange
        post = Post(title=" ")

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res, 
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_cannot_be_blank_for_title_context,
                                                     type=validation_error_type)

    
    def test_post_should_not_be_saved_when_status_is_invalid(self, make_post, invalid_string):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), status=invalid_string)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res, 
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_status_context,
                                                     type=validation_error_type)

    @pytest.mark.parametrize('invalid_visibility', 
        ["  ", None],
        ids=['contains only spaces', 'is null']
    )
    def test_post_should_not_be_saved_when_visibility_is_invalid(self, make_post, invalid_visibility):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), visibility=invalid_visibility)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.internal_server_error(create_post_res, 
                                                      message=server_error_cannot_save_post_msg,
                                                      type=server_error_type, code=unexpected_error_code)

    @pytest.mark.parametrize('invalid_featured', 
        ["  ", None, 1, 0],
        ids=['contains only spaces', 'is null', 'number_one', 'number_zero']
    )
    def test_post_should_not_be_saved_when_featured_is_invalid(self, make_post, invalid_featured):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), featured=invalid_featured)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res, 
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_featured_context,
                                                     type=validation_error_type)

    @pytest.mark.parametrize('invalid_tags', 
        [
            {'key': 'value'},
            [{'key': 'value'}]
        ],
        ids=['a dictionary', 'array of dicts']
    )
    def test_post_should_not_be_saved_when_tags_are_invalid(self, make_post, invalid_tags):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), tags=invalid_tags)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res,
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_tags_context,
                                                     type=validation_error_type)

    @pytest.mark.parametrize('invalid_authors', 
        [
            {'key': 'value'},
            [{'key': 'value'}]
        ],
        ids=['a dictionary', 'array of dicts']
    )
    def test_post_should_not_be_saved_when_authors_are_invalid(self, make_post, invalid_authors):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), authors=invalid_authors)

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res,
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_authors_context,
                                                     type=validation_error_type)
    
    def test_post_should_not_be_saved_when_title_and_status_are_invalid(self, make_post):
        # Arrange
        post = Post(title=' ', status='abc')

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res,
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_status_context,
                                                     type=validation_error_type)
    
    def test_post_should_not_be_saved_when_title_featured_and_status_are_invalid(self, make_post):
        # Arrange
        post = Post(title=' ', featured=1, status='abc')

        # Act
        create_post_res, id = make_post(post)

        # Assert
        Assertions.unprocessable_entity(create_post_res,
                                                     message=validation_cannot_save_post_error_msg,
                                                     context=validation_failed_for_featured_context,
                                                     type=validation_error_type)

