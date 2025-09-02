from fastapi import APIRouter, Depends
from auth.jwt_handler import get_current_user
from database.models import User
from ml.model_handler import model_handler

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/")
def get_model_metrics(current_user: User = Depends(get_current_user)):
    """
    Obtenir les métriques du modèle ML
    """
    return model_handler.get_model_info()

@router.get("/health")
def health_check():
    """
    Vérifier l'état de santé de l'API
    """
    return {
        "status": "healthy",
        "model_loaded": model_handler.model is not None,
        "version": "1.0.0"
    }