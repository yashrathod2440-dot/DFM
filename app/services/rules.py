
STANDARD_TOOLS = [1, 2, 3, 4, 6, 8, 10, 12, 16, 20]


def check_hole_diameter(diameter):
    smallest_tool = min(STANDARD_TOOLS)

    if diameter < smallest_tool:
        return {
            "rule_id": "HOLE_DIAMETER_001",
            "rule_name": "Minimum Hole Diameter",
            "status": "Critical",
            "measured_value": diameter,
            "guideline": smallest_tool,
            "description": f"Hole diameter {diameter} mm is smaller than the minimum tool diameter.",
            "recommendation": f"Increase the hole diameter to at least {smallest_tool} mm."
        }

    return {
        "rule_id": "HOLE_DIAMETER_001",
        "rule_name": "Minimum Hole Diameter",
        "status": "Pass",
        "measured_value": diameter,
        "guideline": smallest_tool,
        "description": f"Hole diameter {diameter} mm is acceptable.",
        "recommendation": "No change required."
    }


def check_hole_depth(diameter, depth, material="Aluminium"):
    """
    Check hole depth using the diameter-to-depth ratio.

    Aluminium:
        Up to 8D  -> Pass
        8D to 10D -> Warning
        Above 10D  -> Critical

    Steel:
        Up to 6D  -> Pass
        6D to 8D  -> Warning
        Above 8D   -> Critical
    """

    if diameter <= 0:
        return {
            "rule_id": "HOLE_DEPTH_001",
            "rule_name": "Hole Depth Ratio",
            "status": "Critical",
            "measured_value": depth,
            "guideline": "Valid diameter required",
            "description": "Hole diameter must be greater than zero.",
            "recommendation": "Check the detected hole diameter."
        }

    ratio = depth / diameter

    if material.lower() == "steel":
        easy_limit = 6
        difficult_limit = 8
    else:
        easy_limit = 8
        difficult_limit = 10

    if ratio <= easy_limit:
        status = "Pass"
        recommendation = "No change required."

    elif ratio <= difficult_limit:
        status = "Warning"
        recommendation = (
            f"Reduce the hole depth or increase the diameter. "
            f"The current depth-to-diameter ratio is {ratio:.2f}D."
        )

    else:
        status = "Critical"
        recommendation = (
            f"Reduce the hole depth or increase the diameter. "
            f"The current depth-to-diameter ratio is {ratio:.2f}D."
        )

    return {
        "rule_id": "HOLE_DEPTH_001",
        "rule_name": "Hole Depth Ratio",
        "status": status,
        "measured_value": round(ratio, 2),
        "guideline": f"{easy_limit}D easy / {difficult_limit}D difficult",
        "description": (
            f"Hole depth is {depth} mm and diameter is {diameter} mm. "
            f"Depth-to-diameter ratio = {ratio:.2f}D."
        ),
        "recommendation": recommendation
    }


def check_wall_thickness(thickness, material="Aluminium"):
    """
    Check minimum wall thickness.

    Aluminium:
        Minimum = 1.0 mm
        1.0 to 1.5 mm -> Warning
        Below 1.0 mm -> Critical
        Above 1.5 mm -> Pass

    Steel:
        Minimum = 2.0 mm
    """

    if material.lower() == "steel":
        minimum_wall = 2.0
        recommended_wall = 2.5
    else:
        minimum_wall = 1.0
        recommended_wall = 1.5

    if thickness < minimum_wall:
        status = "Critical"
        recommendation = (
            f"Increase wall thickness to at least {minimum_wall} mm."
        )

    elif thickness < recommended_wall:
        status = "Warning"
        recommendation = (
            f"Consider increasing wall thickness to {recommended_wall} mm "
            f"for easier manufacturing."
        )

    else:
        status = "Pass"
        recommendation = "No change required."

    return {
        "rule_id": "WALL_THICKNESS_001",
        "rule_name": "Minimum Wall Thickness",
        "status": status,
        "measured_value": thickness,
        "guideline": f"{minimum_wall} mm minimum / {recommended_wall} mm recommended",
        "description": (
            f"Wall thickness is {thickness} mm for {material}."
        ),
        "recommendation": recommendation
    }