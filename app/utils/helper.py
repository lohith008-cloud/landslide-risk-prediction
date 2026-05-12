def get_risk_level(probability):

    if probability < 0.3:
        return "LOW RISK"

    elif probability < 0.6:
        return "MEDIUM RISK"

    return "HIGH RISK"