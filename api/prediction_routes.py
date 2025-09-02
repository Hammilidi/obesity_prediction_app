from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from typing import List

from database.database import get_db
from database.models import User, Prediction
from schemas.prediction_schema import PredictionInput, PredictionOutput, PredictionHistory
from auth.jwt_handler import get_current_user
from ml.model_handler import model_handler 

router = APIRouter()

@router.post("/", response_model=PredictionOutput)
async def create_prediction(
    prediction_input: PredictionInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new prediction for the authenticated user.
    """
    try:
        # 1. Get prediction from the encapsulated model handler
        prediction_result = model_handler.predict(prediction_input)
        
        # 2. Create a new prediction entry in the database
        new_prediction = Prediction(
            user_id=current_user.id,
            # Unpack all input fields from the Pydantic model
            **prediction_input.model_dump(),
            # Add prediction results
            predicted_class=prediction_result["predicted_class"],
            confidence=prediction_result["confidence"],
            probabilities=json.dumps(prediction_result["probabilities"])  # Serialize to JSON string
        )
        
        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)
        
        return prediction_result

    except Exception as e:
        # Handle errors from the model or database
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during prediction: {str(e)}"
        )

@router.get("/history", response_model=List[PredictionHistory])
async def get_my_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Gets the prediction history for the currently authenticated user.
    """
    # Query all predictions belonging to the current user
    predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id).order_by(Prediction.created_at.desc()).all()
    
    # The response_model will automatically handle the conversion
    # from SQLAlchemy objects to Pydantic models because `from_attributes = True`
    # is set in your PredictionHistory schema.
    return predictions