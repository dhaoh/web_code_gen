from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, routes
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="University Course Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)