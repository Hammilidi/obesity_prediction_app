from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relation avec les prédictions
    predictions = relationship("Prediction", back_populates="user")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Features d'entrée
    gender = Column(String)
    age = Column(Float)
    height = Column(Float)
    weight = Column(Float)
    family_history_with_overweight = Column(String)
    favc = Column(String)
    fcvc = Column(Float)
    ncp = Column(Float)
    caec = Column(String)
    smoke = Column(String)
    ch2o = Column(Float)
    scc = Column(String)
    faf = Column(Float)
    tue = Column(Float)
    calc = Column(String)
    mtrans = Column(String)
    
    # Résultats de la prédiction
    predicted_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    probabilities = Column(String)  # JSON string des probabilités
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relation avec l'utilisateur
    user = relationship("User", back_populates="predictions")