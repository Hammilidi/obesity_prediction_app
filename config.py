import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:admin@localhost:5432/obesity_db"
    )
    
    # Model paths
    MODEL_PATH = "models/model.pkl"
    SCALER_PATH = "models/scaler.pkl"
    ENCODERS_PATH = "models/label_encoders.pkl"
    
    # App config
    APP_NAME = "Obesity Prediction API"
    VERSION = "1.0.0"

settings = Settings()