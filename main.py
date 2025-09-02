from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json

from config import settings
from database.database import create_tables, get_db
from database.models import User
from auth import auth_routes
from api import prediction_routes, admin_routes, metrics_routes
from auth.jwt_handler import get_current_user
from schemas.prediction_schema import PredictionInput

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API de prédiction d'obésité avec authentification JWT"
)

# Créer les tables au démarrage
create_tables()

# Configuration des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inclure les routes
app.include_router(auth_routes.router)
app.include_router(
    prediction_routes.router, 
    prefix="/prediction", 
    tags=["Prediction"]
)
app.include_router(admin_routes.router)
app.include_router(metrics_routes.router)

# Routes HTML
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    return templates.TemplateResponse("app_obesity.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

# Route de base pour tester l'API
@app.get("/api/health")
async def root():
    return {
        "message": "Obesity Prediction API is running!",
        "version": settings.VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)