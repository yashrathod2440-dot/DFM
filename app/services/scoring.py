def calculate_dfm_score(features):
    """
    Calculate an initial DFM score from rule results.

    Critical    = -25 points
    Warning     = -10 points
    Information = -2 points
    Pass        = 0 points

    Maximum score = 100
    Minimum score = 0
    """

    score = 100

    counts = {
        "Critical": 0,
        "Warning": 0,
        "Information": 0,
        "Pass": 0
    }

    for feature in features:

        for key, check in feature.items():

            if not key.endswith("_dfm_check"):
                continue

            if not isinstance(check, dict):
                continue

            status = check.get("status", "Information")

            if status in counts:
                counts[status] += 1

            if status == "Critical":
                score -= 25

            elif status == "Warning":
                score -= 10

            elif status == "Information":
                score -= 2

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return {
        "score": score,
        "total_checks": sum(counts.values()),
        "critical": counts["Critical"],
        "warning": counts["Warning"],
        "information": counts["Information"],
        "passed": counts["Pass"]
    }