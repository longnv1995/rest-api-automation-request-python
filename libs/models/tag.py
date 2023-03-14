from dataclasses import dataclass

from libs.models.base import SEO, CodeInjection, CreationAt, Social


@dataclass
class OtherInfo:
    accent_color: str = None

@dataclass
class Tag:
    name: str
    slug: str = None
    description: str = None
    feature_image: str = None
    creation: CreationAt = None
    codeinjection: CodeInjection = None
    social: Social = None
    seo: SEO = None
    other_info = OtherInfo
    
    
    
