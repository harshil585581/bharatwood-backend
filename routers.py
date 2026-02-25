from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from schemas import ProductResponse
import os
import uuid

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    name: str = Form(...),
    category: str = Form(None),
    tags: str = Form(None),
    description: str = Form(None),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    image_paths = []
    if images:
        for image in images:
            # Generate unique filename
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(file_path, "wb") as f:
                f.write(await image.read())
                
            # Store the relative URL to access the image
            image_paths.append(f"/uploads/{filename}")

    db_product = Product(
        name=name,
        category=category,
        tags=tags,
        description=description,
        images=image_paths
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    name: str = Form(None),
    category: str = Form(None),
    tags: str = Form(None),
    description: str = Form(None),
    images: list[UploadFile] = File(None),
    existing_images: str = Form(None),   # 👈 NEW
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if name is not None:
        db_product.name = name
    if category is not None:
        db_product.category = category
    if tags is not None:
        db_product.tags = tags
    if description is not None:
        db_product.description = description

    # 🔥 Handle existing images (after deletion from frontend)
    final_images = []

    if existing_images:
        import json
        final_images = json.loads(existing_images)

    # 🔥 Add newly uploaded images
    if images:
        for image in images:
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                f.write(await image.read())

            final_images.append(f"/uploads/{filename}")

    db_product.images = final_images

    db.commit()
    db.refresh(db_product)

    return db_product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete image files from uploads folder
    if db_product.images:
        for img_path in db_product.images:
            full_path = img_path.lstrip("/")  # removes leading "/"
            if os.path.exists(full_path):
                os.remove(full_path)

    db.delete(db_product)
    db.commit()

    return