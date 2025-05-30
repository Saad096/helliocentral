from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import datasets

app = FastAPI(
    title="helliocentral",
    description="Central platform for solar irradiance and energy datasets",
    version="1.0.0"
)

# Enable CORS for frontend
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])