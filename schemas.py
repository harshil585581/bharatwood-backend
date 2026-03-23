from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[str] = None
    brand: str = ""
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
    subcategory: Optional[str] = None
    tags: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    image: Optional[str] = None
    subcategories: Optional[List[str]] = []
    order: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryReference(BaseModel):
    id: int
    order: int

class CategoryOrderUpdate(BaseModel):
    categories: List[CategoryReference]

class BrandBase(BaseModel):
    name: str

class BrandResponse(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MonthlyVisitStats(BaseModel):
    month: str
    visits: int

class VisitRecord(BaseModel):
    ip_address: Optional[str] = None
    session_id: Optional[str] = None
    user_agent: Optional[str] = None