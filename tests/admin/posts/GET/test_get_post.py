import allure
from libs.assertions import Assertions
from libs.api.admin.post_admin import PostAdmin
from libs.models.post import Post
from text_resources.post_error import *
from text_resources.common_error import *
from utils.helpers import get_key


PostAPI = PostAdmin()


@allure.epic('CMA - Posts')
@allure.story('CMA: PUT - Allowed customer to get posts')
class TestGetPost:
    def test_all_posts_should_be_returned_when_get_list_posts(self):
        # Act
        params = {'limit': 'all'}
        get_posts_res = PostAPI.list_posts(params=params)

        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_is_valid_schema(get_posts_res, 'post.json')
        Assertions.response_contains_meta_obj(get_posts_res)

    def test_post_should_be_return_when_get_post(self, make_post):
        # Arrange: Create a post
        title = PostAPI.fake.sentence()
        post = Post(title=title)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_id(id)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.valid_schema(get_post_res, 'post.json')
        Assertions.response_contains_entry(get_post_res, {'title': title})
        Assertions.response_contains_entry(get_post_res, {'status': 'draft'})

    def test_post_should_be_returned_when_get_post_by_valid_slug(self, make_post):
        # Arrange: Create a post
        title = PostAPI.fake.sentence()
        post = Post(title=title)
        create_post_res, id = make_post(post)
        Assertions.created(create_post_res)
        post_slug = get_key('slug', create_post_res)

        # Act
        get_post_res = PostAPI.get_post_by_slug(post_slug)

        # Assert
        Assertions.ok(get_post_res)
        Assertions.response_contains_entry(get_post_res, {'title': title})
        Assertions.response_contains_entry(get_post_res, {'slug': post_slug})

    def test_no_post_should_be_returned_when_get_post_by_random_slug(self, random_string):
        # Act
        get_post_res = PostAPI.get_post_by_slug(random_string)

        # Assert
        Assertions.not_found(get_post_res, 
                            message=not_found_cannot_read_post_msg,
                            context=not_found_post_context, type=not_found_error_type)

    def test_no_post_should_be_returned_when_get_posts_with_invalid_pagination(self, invalid_page_no):
        # Act
        params={'page': invalid_page_no}
        get_posts_res = PostAPI.list_posts(params=params)

        # Assert
        Assertions.unprocessable_entity(get_posts_res, 
                            message=validation_cannot_get_list_posts_error_msg,
                            context=validation_cannot_get_page_context, type=validation_error_type)

    def test_no_post_should_be_returned_when_get_posts_with_pagination_exceeds_total_pages(self):
        # Act
        params = {'page': 9999}
        get_posts_res = PostAPI.list_posts(params=params)

        # Assert
        Assertions.ok(get_posts_res)
        Assertions.empty_list(get_posts_res)

    def test_matches_posts_should_be_returned_when_filter_posts_by_status(self, post_status):
        # Act
        params = {'filter': 'status:' + post_status}
        get_posts_res = PostAPI.list_posts(params=params)
        
        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_contains_entry(get_posts_res, {'status': post_status})
    
    def test_matches_posts_should_be_returned_when_filter_posts_by_visibility(self, visibility):
        # Arrange
        params = {'filter': 'visibility:' + visibility}

        # Act
        get_posts_res = PostAPI.list_posts(params=params)
        
        # Assert
        Assertions.ok(get_posts_res)
        Assertions.each_item_contains_entry(get_posts_res, {'visibility': visibility})

    def test_no_post_should_be_returned_when_get_post_by_random_id(self, random_guid):
        # Act
        get_post_res = PostAPI.get_post_by_id(random_guid)

        # Assert
        Assertions.not_found(get_post_res, 
                            message=not_found_cannot_read_post_msg,
                            context=not_found_post_context, type=not_found_error_type)
        
    