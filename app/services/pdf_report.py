from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def create_pdf_report(report, output_path):
    """
    Create a PDF DFM analysis report.
    """

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    story = []

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "DFM ANALYSIS REPORT",
            title_style
        )
    )

    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # PART INFORMATION
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Part Information",
            heading_style
        )
    )

    part_info = report.get("part_information", {})

    part_table = Table([
        ["Part Name", part_info.get("part_name", "")],
        ["Manufacturing Process", part_info.get("process", "")],
        ["Material", part_info.get("material", "")]
    ], colWidths=[60 * mm, 100 * mm])

    part_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    story.append(part_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # DFM SUMMARY
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "DFM Summary",
            heading_style
        )
    )

    dfm_summary = report.get("dfm_summary", {})

    summary_table = Table([
        ["DFM Score", str(dfm_summary.get("dfm_score", 0)) + " / 100"],
        ["Total Checks", str(dfm_summary.get("total_checks", 0))],
        ["Passed", str(dfm_summary.get("passed", 0))],
        ["Warnings", str(dfm_summary.get("warning", 0))],
        ["Critical", str(dfm_summary.get("critical", 0))],
        ["Information", str(dfm_summary.get("information", 0))]
    ], colWidths=[60 * mm, 100 * mm])

    summary_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # GEOMETRY SUMMARY
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Geometry Summary",
            heading_style
        )
    )

    geometry = report.get("geometry_summary", {})
    bounding_box = geometry.get("bounding_box", {})

    geometry_table = Table([
        ["Solids", str(geometry.get("solid_count", 0))],
        ["Faces", str(geometry.get("face_count", 0))],
        ["Edges", str(geometry.get("edge_count", 0))],
        ["Vertices", str(geometry.get("vertex_count", 0))],
        ["Volume", str(geometry.get("volume", 0))],
        ["Surface Area", str(geometry.get("surface_area", 0))],
        ["Length", str(bounding_box.get("length", 0))],
        ["Width", str(bounding_box.get("width", 0))],
        ["Height", str(bounding_box.get("height", 0))]
    ], colWidths=[60 * mm, 100 * mm])

    geometry_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))

    story.append(geometry_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # FEATURE SUMMARY
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Feature Summary",
            heading_style
        )
    )

    feature_summary = report.get("feature_summary", {})

    story.append(
        Paragraph(
            "Total Detected Features: "
            + str(feature_summary.get("total_features", 0)),
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # VIOLATIONS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "DFM Violations",
            heading_style
        )
    )

    violations = report.get("violations", [])

    if not violations:

        story.append(
            Paragraph(
                "No DFM violations detected.",
                normal_style
            )
        )

    else:

        violation_data = [
            [
                "Feature",
                "Rule",
                "Status",
                "Measured",
                "Recommendation"
            ]
        ]

        for violation in violations:

            violation_data.append([
                str(violation.get("feature_id", "")),
                str(violation.get("rule_name", "")),
                str(violation.get("status", "")),
                str(violation.get("measured_value", "")),
                str(violation.get("recommendation", ""))
            ])

        violation_table = Table(
            violation_data,
            colWidths=[
                25 * mm,
                35 * mm,
                22 * mm,
                25 * mm,
                55 * mm
            ],
            repeatRows=1
        )

        violation_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("PADDING", (0, 0), (-1, -1), 4)
        ]))

        story.append(violation_table)

    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # REPORT STATUS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Report Status: "
            + report.get("report_status", ""),
            normal_style
        )
    )

    document.build(story)