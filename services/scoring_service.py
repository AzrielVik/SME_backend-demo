def generate_score(metrics):
    score = 100

    if metrics["cash_ratio"] > 0.6:
        score -= 20

    if metrics["total_outflow"] > metrics["total_inflow"]:
        score -= 30

    if score >= 75:
        status = "healthy"
    elif score >= 50:
        status = "moderate"
    else:
        status = "risky"

    return score, status


def generate_flags(metrics):
    flags = []

    if metrics["cash_ratio"] > 0.6:
        flags.append(("warning", "High cash usage reduces traceability"))

    if metrics["total_outflow"] > metrics["total_inflow"]:
        flags.append(("warning", "Business spending exceeds income"))

    return flags
