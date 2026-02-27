from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    images: Optional[List[str]] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True