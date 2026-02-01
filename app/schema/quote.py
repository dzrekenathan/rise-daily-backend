from pydantic import BaseModel
import uuid
from app.schema.category import Category
from datetime import datetime

class QuoteBase(BaseModel):
    quote: str
    image_url: str | None = None
    category_id: int | None = None
    author: str | None = None
    # id: int
    # # id: uuid.uuid5
    # quote: str
    # author: str | None = None
    # image_url: str | None = None
    # category: Category | None = None


class Quote(QuoteBase):
    id: int
    date_created: datetime
    date_updated: datetime