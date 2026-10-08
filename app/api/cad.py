from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.services.geometry_extractor import extract_geometry
from app.services.feature_detection import detect_cylindrical_features
from app.services.violation_summary import generate_violation_summary
from app.services.scoring import calculate_dfm_score
from app.services.report_generator import generate_dfm_report
from app.services.pdf_report import create_pdf_report


router = APIRouter()

# Directory for uploaded STEP files
UPLOAD_DIR = Path("test_parts")
UPLOAD_DIR.mkdir(exist_ok=True)

# Directory for generated PDF reports
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


@router.post("/upload-step")
async def upload_step(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in [".step", ".stp"]:
        raise HTTPException(
            status_code=400,
            detail="Only .step and .stp files are allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()
    file_path.write_bytes(contents)

    return {
        "message": "STEP file uploaded successfully",
        "filename": file.filename,
        "path": str(file_path),
        "size_bytes": len(contents)
    }


@router.post("/analyze-step")
async def analyze_step(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in [".step", ".stp"]:
        raise HTTPException(
            status_code=400,
            detail="Only .step and .stp files are allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()
    file_path.write_bytes(contents)

    try:
        # Extract basic geometry
        geometry = extract_geometry(file_path)

        # Detect cylindrical features and DFM checks
        features = detect_cylindrical_features(file_path)

        # Generate violation summary
        violation_summary = generate_violation_summary(
            features["detected_features"]
        )

        # Calculate DFM score
        dfm_score = calculate_dfm_score(
            features["detected_features"]
        )

        # Generate DFM report
        dfm_report = generate_dfm_report(
            filename=file.filename,
            geometry=geometry,
            features=features,
            violation_summary=violation_summary,
            dfm_score=dfm_score,
            process="CNC Milling",
            material="Aluminium"
        )

        # Create PDF report
        pdf_filename = Path(file.filename).stem + "_DFM_Report.pdf"
        pdf_path = REPORT_DIR / pdf_filename

        create_pdf_report(
            dfm_report,
            pdf_path
        )

        return {
            "message": "STEP analysis completed",
            "filename": file.filename,
            "geometry": geometry,
            "features": features,
            "violation_summary": violation_summary,
            "dfm_score": dfm_score,
            "dfm_report": dfm_report,
            "pdf_report": {
                "filename": pdf_filename,
                "path": str(pdf_path)
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read STEP file: {str(e)}"
        )


@router.get("/download-report/{filename}")
def download_report(filename: str):

    file_path = REPORT_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF report not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )