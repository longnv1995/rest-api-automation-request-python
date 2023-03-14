from libs.api.content.base_content import BaseContentApi


class AuthorClient(BaseContentApi):
    def __init__(self):
        super().__init__()
    
    def list_authors(self, params: dict=None, **kwargs):
        return self.get('/authors', params=params, **kwargs)
    
    def get_author_by_id(self, id: str, params: dict=None, **kwargs):
        return self.get(f'/authors/{id}', params=params, **kwargs)

    def get_author_by_slug(self, slug: str, **kwargs):
        return self.get(f'/authors/slug/{slug}', **kwargs)