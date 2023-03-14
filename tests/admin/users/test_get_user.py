import allure

from libs.api.admin.user_admin import UserAdmin
from libs.assertions import Assertions
from text_resources.user import *
from text_resources.common_error import *
from utils.helpers import get_first_item_of_list, get_value_of_key_in_dict


UserAPI = UserAdmin()


@allure.epic('CMA - Users')
@allure.story('CMA: GET - Allowed customer to get users')
class TestGetUser:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_all_users_should_be_returned_when_get_list_users(self):
        # Act
        get_users_res = UserAPI.list_users()

        # Assert
        Assertions.ok(get_users_res)
        Assertions.each_item_is_valid_schema(get_users_res, 'user.json')
        Assertions.response_contains_meta_obj(get_users_res)

    @allure.severity(allure.severity_level.CRITICAL)    
    def test_one_user_should_be_returned_when_get_user_by_id(self):
        # Arrange:
        get_users_res = UserAPI.list_users()
        Assertions.not_empty(get_users_res)
        first_user_in_list = get_first_item_of_list(get_users_res)
        user_id = get_value_of_key_in_dict('id', first_user_in_list)

        # Act
        get_user_res = UserAPI.get_user_by_id(user_id)

        # Assert
        Assertions.ok(get_user_res)
        Assertions.response_contains_entry(get_user_res, {'id': str(user_id)})
    
    @allure.severity(allure.severity_level.NORMAL)
    def test_one_user_should_be_returned_when_get_user_by_slug(self):
        # Arrange:
        get_users_res = UserAPI.list_users()
        Assertions.not_empty(get_users_res)
        first_user_in_list = get_first_item_of_list(get_users_res)
        user_slug = get_value_of_key_in_dict('slug', first_user_in_list)

        # Act
        get_user_res = UserAPI.get_user_by_slug(user_slug)

        # Assert
        Assertions.ok(get_user_res)
        Assertions.valid_schema(get_users_res, 'user.json')
    
    @allure.severity(allure.severity_level.NORMAL)
    def test_matches_users_should_be_returned_when_filter_users_by_status(self, user_status):
        # Act
        params = {'filter': 'status:' + user_status}
        get_users_res = UserAPI.list_users(params=params)

        # Assert
        Assertions.ok(get_users_res)
        Assertions.each_item_contains_entry(get_users_res, {'status': user_status})

    @allure.severity(allure.severity_level.NORMAL)
    def test_no_user_should_be_returned_when_get_user_by_random_id(self, invalid_id):
        # Act
        get_user_res = UserAPI.get_user_by_id(invalid_id)

        # Assert
        Assertions.unprocessable_entity(get_user_res, 
                                            message=validation_cannot_read_user_msg, 
                                            context=validation_cannot_read_source_by_id_context,
                                            type=validation_error_type)

    
