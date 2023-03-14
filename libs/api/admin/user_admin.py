from libs.api.admin.base_admin import BaseAdminApi


class UserAdmin(BaseAdminApi):
    def __init__(self):
        super().__init__()
    
    def list_users(self, params: dict=None, **kwargs):
        return self.get('/users', params=params, **kwargs)
        
    def get_user_by_id(self, id: int, **kwargs):
        return self.get(f'/users/{id}', **kwargs)

    def get_user_by_slug(self, slug: str, **kwargs):
        return self.get(f'/users/slug/{slug}', **kwargs)