from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class PredictionInput(BaseModel):
    gender: str
    age: float
    height: float
    weight: float
    family_history_with_overweight: str
    favc: str
    fcvc: float
    ncp: float
    caec: str
    smoke: str
    ch2o: float
    scc: str
    faf: float
    tue: float
    calc: str
    mtrans: str

class PredictionOutput(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: Dict[str, float]
    
class PredictionHistory(BaseModel):
    id: int
    predicted_class: str
    confidence: float
    probabilities: str
    created_at: datetime
    
    # Features d'entrée
    gender: str
    age: float
    height: float
    weight: float
    family_history_with_overweight: str
    favc: str
    fcvc: float
    ncp: float
    caec: str
    smoke: str
    ch2o: float
    scc: str
    faf: float
    tue: float
    calc: str
    mtrans: str
    
    class Config:
        from_attributes = True