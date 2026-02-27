from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Category
from schemas import ProductResponse, CategoryResponse
import os
import uuid

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

category_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@category_router.get("/", response_model=list[str])
def get_categories(db: Session = Depends(get_db)):
    db_products_cats = db.query(Product.category).filter(Product.category.isnot(None), Product.category != "").distinct().all()
    db_product_cat_list = [c[0] for c in db_products_cats]
    
    db_categories = db.query(Category.name).all()
    custom_cat_list = [c[0] for c in db_categories]
    
    # Merge defaults and db categories, removing duplicates
    all_categories = sorted(list(set(custom_cat_list)))
    return all_categories

@category_router.get("/all", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.created_at.desc()).all()
    return categories

@category_router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    name: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Check if category already exists
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
        
    image_path = None
    if image:
        ext = os.path.splitext(image.filename)[1]
        filename = f"cat_{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(await image.read())
            
        image_path = f"/uploads/{filename}"

    db_category = Category(
        name=name,
        image=image_path
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    name: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    if name is not None:
        existing = db.query(Category).filter(Category.name == name, Category.id != category_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        db_category.name = name

    if image:
        ext = os.path.splitext(image.filename)[1]
        filename = f"cat_{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as f:
            f.write(await image.read())
            
        if db_category.image:
            old_full_path = db_category.image.lstrip("/")
            if os.path.exists(old_full_path):
                try:
                    os.remove(old_full_path)
                except Exception as e:
                    print(f"Error removing old image: {e}")

        db_category.image = f"/uploads/{filename}"

    db.commit()
    db.refresh(db_category)
    return db_category

@category_router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    if db_category.image:
        full_path = db_category.image.lstrip("/")
        if os.path.exists(full_path):
            os.remove(full_path)
            
    db.delete(db_category)
    db.commit()
    return

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total_products = db.query(Product).count()
    
    db_products_cats = db.query(Product.category).filter(Product.category.isnot(None), Product.category != "").distinct().all()
    db_product_cat_list = [c[0] for c in db_products_cats]
    
    db_categories = db.query(Category.name).all()
    custom_cat_list = [c[0] for c in db_categories]
    
    total_categories = len(set(custom_cat_list))
    
    return {
        "total_products": total_products,
        "total_categories": total_categories
    }

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
def read_products(skip: int = 0, limit: int = 100, search: str = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    products = query.order_by(Product.id.desc()).offset(skip).limit(limit).all()
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
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

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