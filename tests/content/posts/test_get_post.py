import allure

from libs.assertions import Assertions
from libs.api.content.post_client import PostClient
from libs.models.post import Post
from text_resources.post_error import *
from text_resources.common_error import *

from utils.helpers import get_key
from utils.times import future_time


PostAPI = PostClient()


@allure.epic('CD - Posts')
@allure.story('CD: GET - Allowed customer to get posts')
class TestGetPost:
    # Browse
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_published_posts_should_be_returned_when_get_list_posts(self):
        # Act
        get_posts_res = PostAPI.list_posts()

        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_is_valid_schema(get_posts_res, 'post.json')
        Assertions.each_item_contains_entry(get_posts_res, {'access': True})
        Assertions.response_contains_meta_obj(get_posts_res)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_posts_should_be_returned_when_get_list_posts_include_tags(self):
        # Arrange
        params = {'include': 'tags'}
        
        # Act
        get_posts_res = PostAPI.list_posts(params=params)

        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_is_valid_schema(get_posts_res, 'post.json')
        Assertions.each_item_contains_keys(get_posts_res, keys=('tags', 'primary_tag'))

    @allure.severity(allure.severity_level.CRITICAL)
    def test_posts_should_be_returned_when_get_list_posts_include_authors(self):
        # Arrange
        params = {'include': 'authors'}
        
        # Act
        get_posts_res = PostAPI.list_posts(params=params)

        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_is_valid_schema(get_posts_res, 'post.json')
        Assertions.each_item_contains_keys(get_posts_res, keys=('authors', 'primary_author'))

    @allure.severity(allure.severity_level.CRITICAL)
    def test_posts_should_be_returned_when_get_list_posts_include_tags_and_authors(self):
        # Arrange
        params = {'include': 'tags,authors'}
        
        # Act
        get_posts_res = PostAPI.list_posts(params=params)

        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_is_valid_schema(get_posts_res, 'post.json')
        Assertions.each_item_contains_keys(get_posts_res, 
                                           keys=('authors', 'tags', 'primary_author', 'primary_tag'))
    
    # Read
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_post_should_be_returned_when_get_post_by_id(self, make_post, published_status):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), status=published_status)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.valid_schema(get_post_res, 'post.json')
        Assertions.response_contains_entry(get_post_res, {'access': True})

    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_post_should_be_returned_when_get_post_by_slug(self, make_post, published_status):
        # Arrange
        post = Post(title='a nice post', status=published_status)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        post_slug = get_key('slug', create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_slug(post_slug)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.response_contains_entry(get_post_res, {'slug': post_slug})
    
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_post_should_be_returned_when_get_post_include_tags(self, make_post, published_status):
        # Arrange
        params = {'include': 'tags'}
        post = Post(title=PostAPI.fake.sentence(), status=published_status, tags=['one-tag'])
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id, params=params)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.response_contains_keys(get_post_res, keys=('tags', 'primary_tag'))
        # Assertions.valid_schema(get_post_res, 'post.json')
        # Assertions.response_contains_entry(get_post_res, {'access': True})

    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_post_should_be_returned_when_get_post_include_authors(self, make_post, published_status):
        # Arrange
        params = {'include': 'authors'}
        post = Post(title=PostAPI.fake.sentence(), status=published_status)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id, params=params)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.response_contains_keys(get_post_res, keys=('authors', 'primary_author'))
        
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_post_should_be_returned_when_get_post_include_tags_and_authors(self, make_post, published_status):
        # Arrange
        params = {'include': 'authors,tags'}
        post = Post(title=PostAPI.fake.sentence(), status=published_status)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id, params=params)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.response_contains_keys(get_post_res, 
                                           keys=('authors', 'tags', 'primary_author', 'primary_tag'))
    
    @allure.severity(allure.severity_level.CRITICAL)
    def test_one_post_should_be_returned_when_get_post_by_slug_include_authors_and_tags(self, make_post, published_status):
        # Arrange
        params = {'include': 'authors,tags'}
        post = Post(title='a nice post', 
                    status=published_status, 
                    tags=['tag-one', 'tag-two'])
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        post_slug = get_key('slug', create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_slug(post_slug, params=params)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.response_contains_keys(get_post_res, 
                                           keys=('authors', 'tags', 'primary_author', 'primary_tag'))
        # Assertions.valid_schema(get_post_res, 'post.json')
        # Assertions.response_contains_entry(get_post_res, {'access': True})
        # Assertions.response_contains_entry(get_post_res, {'slug': post_slug})

    @allure.severity(allure.severity_level.CRITICAL)
    def test_no_post_should_be_returned_when_get_post_in_draft_status(self, make_post, draft_status):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), status=draft_status)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id)

        # Assert
        Assertions.not_found(get_post_res,
                                message=not_found_cannot_read_post_msg,
                                context=not_found_post_context,
                                type=not_found_error_type)
        
    @allure.severity(allure.severity_level.CRITICAL)
    def test_no_post_should_be_returned_when_get_post_in_scheduled_status(self, make_post, scheduled_status):
        # Arrange
        post = Post(title=PostAPI.fake.sentence(), 
                    status=scheduled_status,
                    published_at=future_time())
        
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id)

        # Assert
        Assertions.not_found(get_post_res,
                                message=not_found_cannot_read_post_msg,
                                context=not_found_post_context,
                                type=not_found_error_type)
