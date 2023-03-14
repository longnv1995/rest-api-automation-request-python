from libs.api.admin.base_admin import BaseAdminApi
from libs.models.tag import Tag
from utils.helpers import get_key


class TagAdmin(BaseAdminApi):
    def __init__(self):
        super().__init__()
    
    def list_tags(self, params: dict=None, **kwargs):
        return self.get('/tags', params=params, **kwargs)

    def get_tag_by_id(self, id, params: dict=None, **kwargs):
        return self.get(f'/tags/{id}', params=params, **kwargs)

    def get_tag_by_slug(self, slug, **kwargs):
        return self.get(f'/tags/slug/{slug}', **kwargs)

    def create_tag(self, tag: Tag):
        content = dict()

        content['name'] = tag.name
        if tag.slug is not None:
            content['slug'] = tag.slug

        content['description'] = tag.description
        content['feature_image'] = tag.feature_image

        if tag.creation is not None:
            creation_time = tag.creation
            content['created_at'] = creation_time.created_at
            content['updated_at'] = creation_time.updated_at

        payload = {'tags': [content]}
        response = self.post('/tags', json=payload)
        id = get_key('id', response)

        return response, id
    
    def put_tag(self, id: str, json=None, data=None, params: dict=None, **kwargs):
        return self.put(f'/tags/{id}', json=json, data=data, params=params, **kwargs)
    
    def delete_tag_by_id(self, id: str, params: dict=None, **kwargs):
        return self.delete(f'/tags/{id}', params=params, **kwargs)
    
    def delete_tag_by_slug(self, slug: str, params=None, **kwargs):
        return self.delete(f'/tags/{slug}', params=params, **kwargs)