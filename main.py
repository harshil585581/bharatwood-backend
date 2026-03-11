from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routers
import analytics_router
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend API")

from fastapi.staticfiles import StaticFiles

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, replace "*" with the specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# hi thisis test

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(routers.router)
app.include_router(routers.category_router)
app.include_router(routers.brand_router)
app.include_router(analytics_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
