from libs.api.admin.base_admin import BaseAdminApi
from libs.models.post import Post
from utils.helpers import get_key


class PostAdmin(BaseAdminApi):
    def __init__(self):
        super().__init__()

    def list_posts(self, params: dict=None, **kwargs):
        return self.get('/posts', params=params, **kwargs)
    
    def get_post_by_id(self, id: str, **kwargs):
        return self.get(f'/posts/{id}', **kwargs)

    def get_post_by_slug(self, slug: str, **kwargs):
        return self.get(f'/posts/slug/{slug}', **kwargs)
    
    def create_post(self, post: Post):
        content = dict()

        if post.feature_image is not None:
            feature_image = post.feature_image
            content['feature_image'] = feature_image.image
            content['feature_image_alt'] = feature_image.alt
            content['feature_image_caption'] = feature_image.caption

        content['title'] = post.title
        if post.slug is not None:
            content['slug'] = post.slug

        content['excerpt'] = post.excerpt
        content['status'] = post.status
        content['featured'] = post.featured

        if post.tags is not None:
            content['tags'] = post.tags

        if post.authors is not None:
            content['authors'] = post.authors

        if post.creation is not None:
            creation_time = post.creation
            content['created_at'] = creation_time.created_at
            content['updated_at'] = creation_time.updated_at

        content['visibility'] = post.visibility

        content['published_at'] = post.published_at
        
        payload = {'posts': [content]}
        response = self.post('/posts', json=payload)
        id = get_key('id', response)

        return response, id
    
    def put_post(self, id: str, json=None, data=None, params: dict=None, **kwargs):
        return self.put(f'/posts/{id}', json=json, data=data, params=params, **kwargs)

    def delete_post_by_id(self, id: str, params: dict=None, **kwargs):
        return self.delete(f'/posts/{id}', params=params, **kwargs)
    
    def delete_post_by_slug(self, slug: str, params=None, **kwargs):
        return self.delete(f'/posts/{slug}', params=params, **kwargs)


    