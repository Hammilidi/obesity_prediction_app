import pickle
import pandas as pd
import numpy as np
from typing import Dict, List
from config import settings
from schemas.prediction_schema import PredictionInput

class ModelHandler:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoders = None
        self.metadata = None
        self.load_model()
    
    def load_model(self):
        """Charger le modèle et les préprocesseurs"""
        try:
            with open(settings.MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            
            with open(settings.SCALER_PATH, "rb") as f:
                self.scaler = pickle.load(f)
            
            with open(settings.ENCODERS_PATH, "rb") as f:
                self.label_encoders = pickle.load(f)
            
            # Charger les métadonnées si disponibles
            try:
                with open("../../models/metadata.pkl", "rb") as f:
                    self.metadata = pickle.load(f)
            except FileNotFoundError:
                self.metadata = {"model_name": "RandomForestClassifier"}
            
            print("✅ Modèle chargé avec succès!")
            
        except FileNotFoundError as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            raise Exception("Modèle non trouvé. Veuillez d'abord entraîner le modèle.")
    
    def preprocess_input(self, input_data: PredictionInput) -> np.ndarray:
        """Préprocesser les données d'entrée"""
        # Convertir en DataFrame
        data_dict = {
            'Gender': input_data.gender,
            'Age': input_data.age,
            'Height': input_data.height,
            'Weight': input_data.weight,
            'family_history_with_overweight': input_data.family_history_with_overweight,
            'FAVC': input_data.favc,
            'FCVC': input_data.fcvc,
            'NCP': input_data.ncp,
            'CAEC': input_data.caec,
            'SMOKE': input_data.smoke,
            'CH2O': input_data.ch2o,
            'SCC': input_data.scc,
            'FAF': input_data.faf,
            'TUE': input_data.tue,
            'CALC': input_data.calc,
            'MTRANS': input_data.mtrans
        }
        
        df = pd.DataFrame([data_dict])
        
        # Encoder les variables catégorielles
        categorical_columns = [
            'Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 
            'SMOKE', 'SCC', 'CALC', 'MTRANS'
        ]
        
        for col in categorical_columns:
            if col in self.label_encoders:
                try:
                    df[col] = self.label_encoders[col].transform(df[col])
                except ValueError:
                    # Si la valeur n'est pas dans l'encodeur, utiliser la première classe
                    df[col] = 0
        
        # Normaliser avec le scaler
        X_scaled = self.scaler.transform(df)
        
        return X_scaled
    
    def predict(self, input_data: PredictionInput) -> Dict:
        """Faire une prédiction"""
        if not self.model:
            raise Exception("Modèle non chargé")
        
        # Préprocesser les données
        X = self.preprocess_input(input_data)
        
        # Prédiction
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Décoder la prédiction
        predicted_class = self.label_encoders['target'].inverse_transform([prediction])[0]
        
        # Créer le dictionnaire des probabilités
        classes = self.label_encoders['target'].classes_
        prob_dict = {classes[i]: float(probabilities[i]) for i in range(len(classes))}
        
        # Confiance = probabilité maximum
        confidence = float(max(probabilities))
        
        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "probabilities": prob_dict
        }
    
    def get_model_info(self) -> Dict:
        """Obtenir les informations du modèle"""
        if self.metadata:
            return self.metadata
        else:
            return {
                "model_name": "RandomForestClassifier",
                "status": "loaded"
            }

# Instance globale du gestionnaire de modèle
model_handler = ModelHandler()