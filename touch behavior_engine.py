
import numpy as np

class BehaviorEngine:
    def __init__(self):
        self.user_profiles = {
            "U1": {"avg": 1200, "std": 400, "start": 9, "end": 21, "device": "Android", "city": "Delhi"},
            "U2": {"avg": 800, "std": 300, "start": 8, "end": 20, "device": "Android", "city": "Mumbai"},
            "U3": {"avg": 1500, "std": 500, "start": 10, "end": 22, "device": "iPhone", "city": "Kolkata"}
        }

    def compute_behavior_risk(self, user, amount, hour, device, city):
        if user not in self.user_profiles:
            return 0.0, {}

        profile = self.user_profiles[user]

        amount_z = abs(amount - profile["avg"]) / profile["std"]
        amount_score = min(amount_z / 5, 1)

        time_flag = 0 if profile["start"] <= hour <= profile["end"] else 1
        device_flag = 0 if device == profile["device"] else 1
        city_flag = 0 if city == profile["city"] else 1

        behavior_score = (
            0.4 * amount_score +
            0.2 * time_flag +
            0.2 * device_flag +
            0.2 * city_flag
        )

        explanation = {
            "Amount deviation": round(amount_score, 2),
            "Unusual time": time_flag,
            "New device": device_flag,
            "New city": city_flag
        }

        return min(behavior_score, 1.0), explanation
