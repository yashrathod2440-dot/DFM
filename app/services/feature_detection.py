import cadquery as cq
from app.services.rules import (
    check_hole_diameter,
    check_hole_depth,
    check_wall_thickness
)


def detect_cylindrical_features(file_path):
    model = cq.importers.importStep(str(file_path))
    shape = model.val()

    features = []
    face_types = []
    detection_errors = []

    # ---------------------------------------------------------
    # FACE TYPE DETECTION
    # ---------------------------------------------------------

    for index, face in enumerate(shape.Faces(), start=1):

        face_type = face.geomType()

        face_types.append({
            "face_number": index,
            "type": face_type
        })

        # -----------------------------------------------------
        # CYLINDRICAL FEATURE / HOLE DETECTION
        # -----------------------------------------------------

        if face_type == "CYLINDER":

            try:
                surface = face._geomAdaptor()

                cylinder = surface.Cylinder()

                radius = cylinder.Radius()

                axis = cylinder.Axis()

                bbox = face.BoundingBox()

                diameter = radius * 2

                # Estimate cylindrical face depth
                depth = max(
                    bbox.xlen,
                    bbox.ylen,
                    bbox.zlen
                )

                feature = {
                    "feature_id": f"CYLINDER_{index}",
                    "feature_type": "potential_hole",
                    "diameter": round(diameter, 3),
                    "radius": round(radius, 3),
                    "depth": round(depth, 3),
                    "face_area": round(face.Area(), 3),

                    "axis": {
                        "x": round(axis.Direction().X(), 3),
                        "y": round(axis.Direction().Y(), 3),
                        "z": round(axis.Direction().Z(), 3)
                    },

                    "bounding_box": {
                        "x": round(bbox.xlen, 3),
                        "y": round(bbox.ylen, 3),
                        "z": round(bbox.zlen, 3)
                    }
                }

                # Rule 1: Hole diameter
                feature["dfm_check"] = check_hole_diameter(
                    feature["diameter"]
                )

                # Rule 2: Hole depth
                feature["depth_dfm_check"] = check_hole_depth(
                    feature["diameter"],
                    feature["depth"],
                    material="Aluminium"
                )

                features.append(feature)

            except Exception as error:

                detection_errors.append({
                    "face_number": index,
                    "error": str(error)
                })

    # ---------------------------------------------------------
    # BASIC WALL THICKNESS DETECTION
    # ---------------------------------------------------------

    try:

        planar_faces = []

        for index, face in enumerate(shape.Faces(), start=1):

            if face.geomType() == "PLANE":

                # Get the plane directly from the face
                surface = face._geomAdaptor()

                normal = surface.Axis().Direction()

                center = face.Center()

                planar_faces.append({
                    "face_number": index,
                    "face": face,
                    "normal": normal,
                    "center": center
                })

        wall_candidates = []

        # Compare pairs of planar faces
        for i in range(len(planar_faces)):

            face1 = planar_faces[i]

            for j in range(i + 1, len(planar_faces)):

                face2 = planar_faces[j]

                normal1 = face1["normal"]
                normal2 = face2["normal"]

                # Check whether the faces are parallel
                dot_product = abs(
                    normal1.X() * normal2.X()
                    + normal1.Y() * normal2.Y()
                    + normal1.Z() * normal2.Z()
                )

                if abs(dot_product - 1.0) > 0.001:
                    continue

                center1 = face1["center"]
                center2 = face2["center"]

                # Distance between face centers
                dx = center2.x - center1.x
                dy = center2.y - center1.y
                dz = center2.z - center1.z

                distance = abs(
                    dx * normal1.X()
                    + dy * normal1.Y()
                    + dz * normal1.Z()
                )

                if distance > 0:

                    wall_candidates.append({
                        "face_1": face1["face_number"],
                        "face_2": face2["face_number"],
                        "thickness": round(distance, 3)
                    })

        # Find smallest candidate wall
        if wall_candidates:

            smallest_wall = min(
                wall_candidates,
                key=lambda item: item["thickness"]
            )

            thickness = smallest_wall["thickness"]

            wall_feature = {
                "feature_id": "WALL_001",
                "feature_type": "potential_wall",
                "thickness": thickness,
                "face_1": smallest_wall["face_1"],
                "face_2": smallest_wall["face_2"],

                "dfm_check": check_wall_thickness(
                    thickness,
                    material="Aluminium"
                )
            }

            features.append(wall_feature)

    except Exception as error:

        detection_errors.append({
            "feature": "wall_thickness",
            "error": str(error)
        })

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    return {
        "face_types": face_types,
        "detected_features": features,
        "detection_errors": detection_errors
    }