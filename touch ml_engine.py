class MLEngine:
    def predict_probability(self, amount):
        if amount > 25000:
            return 0.8
        elif amount > 15000:
            return 0.6
        elif amount > 8000:
            return 0.4
        else:
            return 0.1
