from pydantic import BaseModel
import uuid


class Category(BaseModel):
    id: int
    # id: uuid.uuid5
    name: str
    image_url: str | None = None
    description: str | None = None



class CategoryCreate(BaseModel):
    name: str
    image_url: str | None = None
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    image_url: str | None = None
    description: str | None = None


class CategoryInDB(BaseModel):
    id: uuid.uuid5
    name: str
    image_url: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True

        