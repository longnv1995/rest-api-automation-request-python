from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreationAt:
    created_at: datetime = None
    updated_at: datetime = None
    
@dataclass
class SEO:
    title: str = None
    description: str = None
    canonical_url: str = None

@dataclass
class Twitter:
    image: str = None
    title: str = None
    description: str = None

@dataclass
class Facebook:
    title: str = None
    description: str = None

@dataclass
class Social:
    twitter: Twitter = None
    facebook: Facebook = None

@dataclass
class CodeInjection:
    codeinjection_head: str = None
    codeinjection_foot: str = None

@dataclass
class Email:
    email: str = None
    subject: str = None
    segment: str = None