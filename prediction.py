"""
Disease prediction and risk classification logic
Maps symptoms to diseases and calculates risk levels
"""

from typing import Dict, List, Tuple
from data import DISEASE_SYMPTOMS


# Symptom to disease matching weights
SYMPTOM_WEIGHTS: Dict[str, Dict[str, float]] = {
    "fever": {"Dengue": 0.9, "Typhoid": 0.95, "Flu": 0.85, "TB": 0.7, "Malaria": 0.95, "COVID-19": 0.9},
    "headache": {"Dengue": 0.8, "Typhoid": 0.85, "Flu": 0.75, "TB": 0.6, "Malaria": 0.8, "COVID-19": 0.7},
    "joint pain": {"Dengue": 0.9, "Typhoid": 0.5, "Flu": 0.7, "TB": 0.4, "Malaria": 0.6, "COVID-19": 0.6},
    "rash": {"Dengue": 0.85, "Typhoid": 0.3, "Flu": 0.2, "TB": 0.2, "Malaria": 0.4, "COVID-19": 0.3},
    "bleeding": {"Dengue": 0.7, "Typhoid": 0.2, "Flu": 0.1, "TB": 0.3, "Malaria": 0.3, "COVID-19": 0.2},
    "nausea": {"Dengue": 0.6, "Typhoid": 0.7, "Flu": 0.5, "TB": 0.4, "Malaria": 0.7, "COVID-19": 0.5},
    "stomach pain": {"Dengue": 0.3, "Typhoid": 0.9, "Flu": 0.2, "TB": 0.3, "Malaria": 0.5, "COVID-19": 0.3},
    "diarrhea": {"Dengue": 0.4, "Typhoid": 0.85, "Flu": 0.3, "TB": 0.2, "Malaria": 0.4, "COVID-19": 0.4},
    "weakness": {"Dengue": 0.7, "Typhoid": 0.8, "Flu": 0.7, "TB": 0.85, "Malaria": 0.8, "COVID-19": 0.75},
    "loss of appetite": {"Dengue": 0.5, "Typhoid": 0.8, "Flu": 0.6, "TB": 0.75, "Malaria": 0.7, "COVID-19": 0.6},
    "cough": {"Dengue": 0.3, "Typhoid": 0.4, "Flu": 0.9, "TB": 0.95, "Malaria": 0.3, "COVID-19": 0.9},
    "sore throat": {"Dengue": 0.2, "Typhoid": 0.3, "Flu": 0.85, "TB": 0.4, "Malaria": 0.2, "COVID-19": 0.7},
    "body ache": {"Dengue": 0.7, "Typhoid": 0.5, "Flu": 0.8, "TB": 0.5, "Malaria": 0.7, "COVID-19": 0.85},
    "fatigue": {"Dengue": 0.8, "Typhoid": 0.75, "Flu": 0.8, "TB": 0.85, "Malaria": 0.8, "COVID-19": 0.8},
    "runny nose": {"Dengue": 0.2, "Typhoid": 0.2, "Flu": 0.75, "TB": 0.2, "Malaria": 0.2, "COVID-19": 0.6},
    "weight loss": {"Dengue": 0.3, "Typhoid": 0.4, "Flu": 0.2, "TB": 0.9, "Malaria": 0.5, "COVID-19": 0.4},
    "night sweats": {"Dengue": 0.3, "Typhoid": 0.4, "Flu": 0.2, "TB": 0.85, "Malaria": 0.6, "COVID-19": 0.3},
    "chest pain": {"Dengue": 0.2, "Typhoid": 0.3, "Flu": 0.4, "TB": 0.8, "Malaria": 0.3, "COVID-19": 0.7},
    "chills": {"Dengue": 0.5, "Typhoid": 0.6, "Flu": 0.6, "TB": 0.5, "Malaria": 0.9, "COVID-19": 0.5},
    "sweating": {"Dengue": 0.4, "Typhoid": 0.5, "Flu": 0.3, "TB": 0.6, "Malaria": 0.85, "COVID-19": 0.4},
    "breathing difficulty": {"Dengue": 0.4, "Typhoid": 0.3, "Flu": 0.5, "TB": 0.7, "Malaria": 0.4, "COVID-19": 0.9},
    "loss of taste": {"Dengue": 0.2, "Typhoid": 0.2, "Flu": 0.3, "TB": 0.2, "Malaria": 0.2, "COVID-19": 0.8},
}


def normalize_symptom_name(symptom: str) -> str:
    """Normalize symptom name to lowercase and handle variations"""
    symptom = symptom.lower().strip()
    # Handle common variations
    variations = {
        "fever": ["fever", "high temperature", "temp"],
        "headache": ["headache", "head pain", "head ache"],
        "cough": ["cough", "coughing"],
        "breathing difficulty": ["breathing difficulty", "shortness of breath", "breathlessness", "difficulty breathing"],
        "body ache": ["body ache", "body pain", "muscle pain", "aches"],
        "stomach pain": ["stomach pain", "abdominal pain", "belly pain"],
    }
    
    for standard, variants in variations.items():
        if symptom in variants:
            return standard
    
    return symptom


def predict_disease(symptoms: List[str], age: int, city: str, vitals: Dict[str, float]) -> Tuple[str, float]:
    """
    Predict disease based on symptoms, age, city, and vitals
    Returns: (disease_name, confidence_percentage)
    """
    if not symptoms:
        return "No Disease", 0.0
    
    # Normalize symptoms
    normalized_symptoms = [normalize_symptom_name(s) for s in symptoms]
    
    # Calculate scores for each disease
    disease_scores: Dict[str, float] = {}
    
    for disease in DISEASE_SYMPTOMS.keys():
        score = 0.0
        matched_symptoms = 0
        
        for symptom in normalized_symptoms:
            if symptom in SYMPTOM_WEIGHTS and disease in SYMPTOM_WEIGHTS[symptom]:
                score += SYMPTOM_WEIGHTS[symptom][disease]
                matched_symptoms += 1
        
        # Average score weighted by number of matched symptoms
        if matched_symptoms > 0:
            disease_scores[disease] = (score / matched_symptoms) * 100
        else:
            disease_scores[disease] = 0.0
    
    # Adjust based on vitals
    if vitals:
        bp_systolic = vitals.get("bp_systolic", 120)
        bp_diastolic = vitals.get("bp_diastolic", 80)
        temperature = vitals.get("temperature", 98.6)
        
        # Low BP increases risk for Dengue/Typhoid
        if bp_systolic < 90 or bp_diastolic < 60:
            disease_scores["Dengue"] *= 1.2
            disease_scores["Typhoid"] *= 1.15
        
        # High temperature increases all fever-related diseases
        if temperature > 100:
            for disease in ["Dengue", "Typhoid", "Flu", "Malaria", "COVID-19"]:
                disease_scores[disease] *= 1.1
    
    # Get top disease
    if not disease_scores or max(disease_scores.values()) < 30:
        return "No Disease", 0.0
    
    top_disease = max(disease_scores.items(), key=lambda x: x[1])
    return top_disease[0], min(top_disease[1], 100.0)


def classify_risk(
    age: int,
    symptoms: List[str],
    vitals: Dict[str, float],
    city: str,
    disease: str,
    disease_confidence: float
) -> Tuple[str, int]:
    """
    Classify risk level: HIGH, MEDIUM, or LOW
    Returns: (risk_level, risk_percentage)
    
    HIGH: Elderly + multiple symptoms + rising city trend
    MEDIUM: 2+ symptoms OR abnormal vitals
    LOW: 1 symptom + normal vitals
    """
    risk_score = 0
    
    # Age factor (elderly = higher risk)
    if age >= 65:
        risk_score += 30
    elif age >= 50:
        risk_score += 15
    
    # Symptom count
    symptom_count = len(symptoms)
    if symptom_count >= 4:
        risk_score += 35
    elif symptom_count >= 2:
        risk_score += 20
    else:
        risk_score += 10
    
    # Vitals check
    if vitals:
        bp_systolic = vitals.get("bp_systolic", 120)
        bp_diastolic = vitals.get("bp_diastolic", 80)
        temperature = vitals.get("temperature", 98.6)
        
        # Abnormal vitals
        if bp_systolic < 90 or bp_diastolic < 60 or bp_systolic > 140 or bp_diastolic > 90:
            risk_score += 20
        
        if temperature > 101:
            risk_score += 15
    
    # Disease confidence
    risk_score += int(disease_confidence * 0.3)
    
    # City trend factor (would need to check if disease is rising in city)
    # For now, add small boost if confidence is high
    if disease_confidence > 70:
        risk_score += 10
    
    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Classify
    if risk_score >= 70:
        return "HIGH", risk_score
    elif risk_score >= 40:
        return "MEDIUM", risk_score
    else:
        return "LOW", risk_score

