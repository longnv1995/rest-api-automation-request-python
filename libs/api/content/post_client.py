from libs.api.content.base_content import BaseContentApi


class PostClient(BaseContentApi):
    def __init__(self):
        super().__init__()
    
    def list_posts(self, params: dict=None, **kwargs):
        return self.get('/posts', params=params, **kwargs)
    
    def get_post_by_id(self, id: str, params: dict=None, **kwargs):
        return self.get(f'/posts/{id}', params=params, **kwargs)
    
    def get_post_by_slug(self, slug: str, params: dict=None, **kwargs):
        return self.get(f'/posts/slug/{slug}', params=params, **kwargs)
