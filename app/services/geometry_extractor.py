import cadquery as cq


def extract_geometry(file_path):
    """
    Import a STEP file and extract basic geometry information.
    """

    model = cq.importers.importStep(str(file_path))
    shape = model.val()

    solids = shape.Solids()
    faces = shape.Faces()
    edges = shape.Edges()
    vertices = shape.Vertices()

    bounding_box = shape.BoundingBox()

    return {
        "solid_count": len(solids),
        "face_count": len(faces),
        "edge_count": len(edges),
        "vertex_count": len(vertices),
        "volume": round(shape.Volume(), 3),
        "surface_area": round(shape.Area(), 3),
        "bounding_box": {
            "length": round(bounding_box.xlen, 3),
            "width": round(bounding_box.ylen, 3),
            "height": round(bounding_box.zlen, 3)
        }
    }