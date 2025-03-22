import random
from datetime import datetime, timedelta

DESTINATIONS = ["Orbital Space Station", "Lunar Hotel Alpha", "Mars Prep Module", "ISS Viewpoint Lounge"]

PACKAGES = [
    {"name": "Economy Shuttle", "description": "Affordable and safe", "base_price": 100000},
    {"name": "Luxury Cabin", "description": "Premium seating and meals", "base_price": 250000},
    {"name": "VIP Zero-Gravity", "description": "Personal pod & gravity-free experience", "base_price": 500000},
]

AI_TIPS = [
    "Did you know? Your body gets 2cm taller in space due to spine elongation!",
    "Drink more water before space flights to stay hydrated and counter fluid loss.",
    "Zero gravity affects your taste buds. Food tastes blander!",
    "Pack smart! No loose items—everything floats in microgravity."
]

def get_available_dates():
    return [(datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(3, 30, 3)]

def generate_ai_tip():
    return random.choice(AI_TIPS)

def dynamic_price(date_str, seat_class):
    base = {"Economy": 100000, "Luxury": 250000, "VIP": 500000}
    days_to_launch = (datetime.strptime(date_str, "%Y-%m-%d") - datetime.today()).days
    multiplier = 1.5 if days_to_launch < 10 else 1.0
    return round(base[seat_class] * multiplier, 2)
