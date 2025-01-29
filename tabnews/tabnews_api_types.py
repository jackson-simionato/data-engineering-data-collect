from pydantic import BaseModel, field_validator
from typing import Literal, Optional

class Strategy(BaseModel):
    strategy: Optional[Literal['new', 'old', 'relevant']] = None

class PerPage(BaseModel):
    per_page: Optional[int] = None

    @field_validator('per_page')
    def validate_per_page(cls, v):
        if not isinstance(v, int):
            raise ValueError('per_page must be an integer')
        return v

class Page(BaseModel):
    page: Optional[int] = None

    @field_validator('page')
    def validate_page(cls, v):
        if not isinstance(v, int):
            raise ValueError('page must be an integer')
        return v

class GetContentParams(Strategy, PerPage, Page):
    pass
