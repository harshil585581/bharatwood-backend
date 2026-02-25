from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routers

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

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(routers.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
