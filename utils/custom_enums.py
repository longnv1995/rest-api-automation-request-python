from enum import Enum

class BaseEnum(Enum):
    pass

class HttpMethod(str, BaseEnum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

class PostStatus(str, BaseEnum):
    DRAFT = 'draft'
    SCHEDULED = 'scheduled'
    PUBLISHED = 'published'

class UserStatus(str, BaseEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class Visibility(str, BaseEnum):
    PUBLIC = 'public'
    PAID = 'paid'
    MEMBERS = 'members'

class Gender(BaseEnum):
    MALE = 'male'
    FEMALE = 'female'

class Format(BaseEnum):
    HTML = 'html'
    MARKDOWN = 'markdown'

class TierType(BaseEnum):
    FREE = 'free'
    PAID = 'paid'

class TierVisibility(BaseEnum):
    PUBLIC = 'public'
    NONE = 'none'

class TagVisibility(BaseEnum):
    PUBLIC = 'public'
    INTERNAL = 'internal'