from libs.api.content.base_content import BaseContentApi


class TagClient(BaseContentApi):
    def __init__(self):
        super().__init__()
    
    def list_tags(self, params: dict=None, **kwargs):
        return self.get('/tags', params=params, **kwargs)

    def get_tag_by_id(self, id, params: dict=None, **kwargs):
        return self.get(f'/tags/{id}', params=params, **kwargs)

    def get_tag_by_slug(self, slug, **kwargs):
        return self.get(f'/tags/slug/{slug}', **kwargs)

    