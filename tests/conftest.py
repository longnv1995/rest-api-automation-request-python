import pytest
from uuid import uuid4
import allure
from datetime import datetime as dt

from libs.api.admin.user_admin import UserAdmin
from libs.api.admin.post_admin import PostAdmin
from libs.api.admin.tag_admin import TagAdmin
from libs.models.post import Post
from utils.custom_enums import PostStatus, UserStatus, Visibility, TierType
from utils.times import report_time


"""
session scope
"""
@pytest.fixture(scope="session")
def random_guid():
    return '63f21fc3d8bfb835f4496ef2'

@pytest.fixture(scope="session", params=["str1-str2", "random", "1", "page1-2", "a_b"])
def random_string(request):
    return request.param

@pytest.fixture(scope="session", params=["str1-str2", "randomabc", "1", "a_b"])
def random_slug(request):
    return request.param

@pytest.fixture(scope="session")
def user():
    return UserAdmin()

@pytest.fixture(scope="session")
def post():
    return PostAdmin()

@pytest.fixture(scope="session")
def tag():
    return TagAdmin()

# Invalid data
@pytest.fixture(scope="session", params=[-1, 0, 99999, "str", "1str", uuid4().hex])
def invalid_id(request):
    return request.param

@pytest.fixture(scope="session", params=[-1, "str"])
def invalid_page_no(request):
    return request.param
0
@pytest.fixture(scope="session", params=[-1, "1"])
def invalid_number(request):
    return request.param

@pytest.fixture(scope="session", params=[-0.1, 1.1, 0.1, 0.01, 10.01, 99.99])
def invalid_integer(request):
    return request.param

@pytest.fixture(scope="session", 
    params=["  ", "", None], 
    ids=["only spaces", "empty string", "null"]
)
def invalid_string(request):
    return request.param

# Valid data

@pytest.fixture(scope="session", params=[e.value for e in UserStatus])
def user_status(request):
    return request.param

@pytest.fixture(scope="session", params=[e.value for e in PostStatus])
def post_status(request):
    return request.param

@pytest.fixture(scope="session")
def published_status():
    return PostStatus.PUBLISHED.value

@pytest.fixture(scope="session")
def draft_status():
    return PostStatus.DRAFT.value

@pytest.fixture(scope="session")
def scheduled_status():
    return PostStatus.SCHEDULED.value

@pytest.fixture(scope="session", params=[e.value for e in Visibility])
def visibility(request):
    return request.param

@pytest.fixture(scope="session", params=[e.value for e in TierType])
def tier_type(request):
    return request.param

@pytest.fixture(scope="session", params=[True, False])
def boolean(request):
    return request.param

"""
function scope
"""
@pytest.fixture(scope="function")
def make_post(post):
    _result = []
    def _make_post(post_data: Post):
        res, id = post.create_post(post_data)
        _result.append(id)
        return res, id

    yield _make_post

    for id in _result:
        post.delete_post_by_id(id)

@pytest.fixture(scope="function")
def make_tag(tag):
    _result = []
    def _make_tag(tag_data):
        res, id = tag.create_tag(tag_data)
        _result.append(id)
        return res, id

    yield _make_tag

    for id in _result:
        tag.delete_tag_by_id(id)
