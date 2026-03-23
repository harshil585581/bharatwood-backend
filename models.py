from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    subcategory = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    brand = Column(String, nullable=False, default="")
    description = Column(Text, nullable=True)
    images = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    image = Column(String, nullable=True)
    subcategories = Column(JSON, default=list, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SiteVisit(Base):
    __tablename__ = "site_visits"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True, nullable=True)
    session_id = Column(String, index=True, nullable=True)
    user_agent = Column(String, nullable=True)
    origin = Column(String, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
