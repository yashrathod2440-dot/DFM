def generate_violation_summary(features):
    """
    Generate a summary of all DFM rule results.
    """

    summary = {
        "total_checks": 0,
        "critical": 0,
        "warning": 0,
        "information": 0,
        "passed": 0
    }

    violations = []

    for feature in features:

        feature_id = feature.get("feature_id", "UNKNOWN")
        feature_type = feature.get("feature_type", "UNKNOWN")

        for key, check in feature.items():

            if not key.endswith("_dfm_check"):
                continue

            if not isinstance(check, dict):
                continue

            status = check.get("status", "Information")

            summary["total_checks"] += 1

            if status == "Critical":
                summary["critical"] += 1

            elif status == "Warning":
                summary["warning"] += 1

            elif status == "Information":
                summary["information"] += 1

            elif status == "Pass":
                summary["passed"] += 1

            # Store only actual violations
            if status in ["Critical", "Warning", "Information"]:

                violations.append({
                    "feature_id": feature_id,
                    "feature_type": feature_type,
                    "rule_id": check.get("rule_id"),
                    "rule_name": check.get("rule_name"),
                    "status": status,
                    "measured_value": check.get("measured_value"),
                    "guideline": check.get("guideline"),
                    "description": check.get("description"),
                    "recommendation": check.get("recommendation")
                })

    return {
        "summary": summary,
        "violations": violations
    }