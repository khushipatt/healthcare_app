"""
Mock city-wise disease monitoring data
Provides weekly trends for different cities and diseases
"""

from typing import Dict, List
import random

# City-wise disease trends (Week 1 → Week 4)
CITY_DISEASE_DATA: Dict[str, Dict[str, List[int]]] = {
    "Ahmedabad": {
        "Dengue": [120, 135, 150, 168],  # ↑40% trend
        "TB": [45, 44, 46, 45],  # Steady
        "Flu": [80, 85, 90, 88],
        "Typhoid": [30, 32, 35, 33],
    },
    "Mumbai": {
        "Typhoid": [95, 110, 125, 140],  # Rising
        "Flu": [200, 220, 240, 260],  # Peak next week
        "Dengue": [60, 65, 70, 68],
        "TB": [55, 56, 57, 56],
    },
    "Delhi": {
        "Flu": [150, 145, 140, 135],
        "Dengue": [100, 105, 110, 108],
        "TB": [70, 72, 71, 70],
        "Typhoid": [50, 52, 54, 53],
    },
    "Bangalore": {
        "Dengue": [85, 90, 95, 92],
        "Flu": [120, 125, 130, 128],
        "TB": [40, 41, 42, 41],
        "Typhoid": [35, 36, 37, 36],
    },
    "Chennai": {
        "Typhoid": [70, 75, 80, 78],
        "Dengue": [95, 100, 105, 103],
        "Flu": [110, 115, 120, 118],
        "TB": [50, 51, 52, 51],
    },
    "Kolkata": {
        "TB": [60, 62, 64, 63],
        "Dengue": [75, 78, 80, 79],
        "Flu": [90, 92, 94, 93],
        "Typhoid": [40, 42, 44, 43],
    },
    "Hyderabad": {
        "Dengue": [110, 115, 120, 118],
        "Flu": [130, 135, 140, 138],
        "Typhoid": [45, 47, 49, 48],
        "TB": [35, 36, 37, 36],
    },
    "Pune": {
        "Flu": [100, 105, 110, 108],
        "Dengue": [70, 72, 74, 73],
        "TB": [30, 31, 32, 31],
        "Typhoid": [55, 57, 59, 58],
    },
}

# Disease symptoms mapping
DISEASE_SYMPTOMS: Dict[str, List[str]] = {
    "Dengue": ["fever", "headache", "joint pain", "rash", "bleeding", "nausea"],
    "Typhoid": ["fever", "headache", "stomach pain", "diarrhea", "weakness", "loss of appetite"],
    "Flu": ["fever", "cough", "sore throat", "body ache", "fatigue", "runny nose"],
    "TB": ["cough", "fever", "weight loss", "night sweats", "chest pain", "fatigue"],
    "Malaria": ["fever", "chills", "headache", "nausea", "sweating", "fatigue"],
    "COVID-19": ["fever", "cough", "breathing difficulty", "fatigue", "loss of taste", "body ache"],
}


def get_city_trends(city: str) -> Dict[str, List[int]]:
    """Get disease trends for a specific city"""
    return CITY_DISEASE_DATA.get(city, {})


def get_all_cities() -> List[str]:
    """Get list of all available cities"""
    return list(CITY_DISEASE_DATA.keys())


def get_disease_symptoms(disease: str) -> List[str]:
    """Get symptoms for a specific disease"""
    return DISEASE_SYMPTOMS.get(disease, [])


def get_trend_direction(cases: List[int]) -> str:
    """Determine trend direction: ↑ (rising), ↓ (falling), or → (steady)"""
    if len(cases) < 2:
        return "→"
    
    first_half = sum(cases[:len(cases)//2])
    second_half = sum(cases[len(cases)//2:])
    
    if second_half > first_half * 1.1:
        return "↑"
    elif second_half < first_half * 0.9:
        return "↓"
    else:
        return "→"


def get_city_summary(city: str) -> str:
    """Get a text summary of city disease trends"""
    trends = get_city_trends(city)
    if not trends:
        return f"No data available for {city}"
    
    summary_parts = []
    for disease, cases in trends.items():
        direction = get_trend_direction(cases)
        change_pct = int(((cases[-1] - cases[0]) / cases[0]) * 100) if cases[0] > 0 else 0
        status = "rising" if direction == "↑" else "falling" if direction == "↓" else "steady"
        summary_parts.append(f"{disease} {status} ({change_pct:+d}%)")
    
    return ", ".join(summary_parts)

