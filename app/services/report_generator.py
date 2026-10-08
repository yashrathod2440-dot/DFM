
def generate_dfm_report(
    filename,
    geometry,
    features,
    violation_summary,
    dfm_score,
    process="CNC Milling",
    material="Aluminium"
):
    """
    Generate a structured DFM analysis report.
    """

    summary = violation_summary.get("summary", {})
    violations = violation_summary.get("violations", [])

    report = {
        "report_title": "DFM Analysis Report",

        "part_information": {
            "part_name": filename,
            "process": process,
            "material": material
        },

        "dfm_summary": {
            "dfm_score": dfm_score.get("score", 0),
            "total_checks": summary.get("total_checks", 0),
            "passed": summary.get("passed", 0),
            "critical": summary.get("critical", 0),
            "warning": summary.get("warning", 0),
            "information": summary.get("information", 0)
        },

        "geometry_summary": {
            "solid_count": geometry.get("solid_count", 0),
            "face_count": geometry.get("face_count", 0),
            "edge_count": geometry.get("edge_count", 0),
            "vertex_count": geometry.get("vertex_count", 0),
            "volume": geometry.get("volume", 0),
            "surface_area": geometry.get("surface_area", 0),
            "bounding_box": geometry.get("bounding_box", {})
        },

        "feature_summary": {
            "total_features": len(
                features.get("detected_features", [])
            )
        },

        "violations": violations,

        "report_status": (
            "No DFM violations detected"
            if len(violations) == 0
            else "DFM violations detected"
        )
    }

    return report