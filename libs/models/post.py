from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from libs.models.author import Author
from libs.models.tag import Tag
from utils.custom_enums import PostStatus, Visibility
from libs.models.base import CreationAt, CodeInjection


@dataclass
class FeatureImage:
    image: str = None
    alt: str = None
    caption: str = None

@dataclass
class PublishedAt:
    published_at: datetime = None
    
@dataclass
class OtherInfo:
    newsletter: str = None
    codeinjection: CodeInjection = None

@dataclass
class Post:
    title: str = None
    slug: str = None
    excerpt: str = None
    feature_image: FeatureImage = None
    featured: bool = False
    status: PostStatus = field(default=PostStatus.DRAFT.value)
    creation: CreationAt = None
    published_at: PublishedAt = None
    visibility: Visibility = field(default=Visibility.PUBLIC.value)
    tags: List[Tag] = None
    authors: List[Author] = None
    other_info: OtherInfo = None



