import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os
from datetime import datetime

def train_obesity_model(data_path: str = "../../data/ObesityDataSet_raw_and_data_sinthetic.csv"):
    """
    Entraîne le modèle de classification d'obésité
    """
    print("🚀 Début de l'entraînement du modèle...")
    
    # Charger les données
    try:
        df = pd.read_csv(data_path)
        print(f"✅ Données chargées: {df.shape}")
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {data_path}")
        return
    
    # Préparation des données
    print("🔄 Préparation des données...")
    
    # Variables catégorielles à encoder
    categorical_columns = [
        'Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 
        'SMOKE', 'SCC', 'CALC', 'MTRANS'
    ]
    
    # Créer les encodeurs
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Séparer les features et le target
    X = df.drop('NObeyesdad', axis=1)
    y = df['NObeyesdad']
    
    # Encoder le target
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)
    label_encoders['target'] = target_encoder
    
    # Normaliser les features numériques
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print("🤖 Entraînement du modèle...")
    
    # Entraîner le modèle
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    model.fit(X_train, y_train)
    
    # Évaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Précision du modèle: {accuracy:.4f}")
    print("\n📊 Rapport de classification:")
    print(classification_report(y_test, y_pred, 
                               target_names=target_encoder.classes_))
    
    # Créer le dossier models s'il n'existe pas
    os.makedirs("models", exist_ok=True)
    
    # Sauvegarder le modèle et les préprocesseurs
    print("💾 Sauvegarde du modèle et des préprocesseurs...")
    
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    with open("models/label_encoders.pkl", "wb") as f:
        pickle.dump(label_encoders, f)
    
    # Sauvegarder les métadonnées du modèle
    metadata = {
        'model_name': 'RandomForestClassifier',
        'features': list(X.columns),
        'classes': list(target_encoder.classes_),
        'accuracy': accuracy,
        'training_date': datetime.now().isoformat(),
        'n_samples': len(df)
    }
    
    with open("models/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)
    
    print("✅ Modèle sauvegardé avec succès!")
    return model, scaler, label_encoders, metadata

if __name__ == "__main__":
    train_obesity_model()