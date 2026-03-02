class RiskEngine:
    def aggregate_risk(self, ml_prob, graph_risk, behavior_risk):
        final_score = (
            0.5 * ml_prob +
            0.3 * graph_risk +
            0.2 * behavior_risk
        )
        return min(final_score, 1.0)

    def make_decision(self, risk_score):
        if risk_score < 0.4:
            return "APPROVED"
        elif risk_score < 0.7:
            return "STEP-UP AUTH"
        else:
            return "BLOCKED"
