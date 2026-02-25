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
    tags = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    images = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
