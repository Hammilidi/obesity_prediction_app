import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import tempfile

from app import app
from database.database import get_db, Base
from database.models import User, Prediction
# from auth.password_utils import hash_password
from auth.jwt_handler import create_access_token
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Configuration de la base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """Créer le moteur de base de données pour les tests"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    """Créer une session de base de données pour chaque test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Créer un client de test FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Créer un utilisateur de test"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": hash_password("testpassword"),
        "is_admin": False,
        "is_active": True
    }
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin_user(db_session):
    """Créer un utilisateur admin de test"""
    admin_data = {
        "username": "adminuser",
        "email": "admin@example.com",
        "hashed_password": hash_password("adminpassword"),
        "is_admin": True,
        "is_active": True
    }
    admin = User(**admin_data)
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def user_token(test_user):
    """Créer un token JWT pour l'utilisateur de test"""
    return create_access_token(data={"sub": test_user.username})

@pytest.fixture
def admin_token(test_admin_user):
    """Créer un token JWT pour l'admin de test"""
    return create_access_token(data={"sub": test_admin_user.username})

@pytest.fixture
def auth_headers(user_token):
    """Créer les headers d'authentification pour l'utilisateur"""
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture
def admin_headers(admin_token):
    """Créer les headers d'authentification pour l'admin"""
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
def sample_prediction_data():
    """Données d'exemple pour les prédictions"""
    return {
        "gender": "Female",
        "age": 21.0,
        "height": 1.62,
        "weight": 64.0,
        "family_history_with_overweight": "yes",
        "favc": "no",
        "fcvc": 2.0,
        "ncp": 3.0,
        "caec": "Sometimes",
        "smoke": "no",
        "ch2o": 2.0,
        "scc": "no",
        "faf": 0.0,
        "tue": 1.0,
        "calc": "no",
        "mtrans": "Public_Transportation"
    }

@pytest.fixture
def test_prediction(db_session, test_user, sample_prediction_data):
    """Créer une prédiction de test"""
    prediction_data = {
        "user_id": test_user.id,
        "predicted_class": "Normal_Weight",
        "confidence": 0.85,
        "probabilities": '{"Normal_Weight": 0.85, "Overweight_Level_I": 0.15}',
        **sample_prediction_data
    }
    prediction = Prediction(**prediction_data)
    db_session.add(prediction)
    db_session.commit()
    db_session.refresh(prediction)
    return prediction