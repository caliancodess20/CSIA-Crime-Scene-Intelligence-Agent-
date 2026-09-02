from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def build_pdf_report(case_id: str):

    case_folder = Path("uploads") / case_id

    if not case_folder.exists():
        return None

    evidence_files = list(case_folder.iterdir())

    report_folder = Path("reports")
    report_folder.mkdir(exist_ok=True)

    pdf_path = report_folder / f"{case_id}_report.pdf"

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4
    )

    content = []

    content.append(
        Paragraph(
            "Crime Scene Intelligence Assistant",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"<b>Case ID:</b> {case_id}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Total Evidence:</b> {len(evidence_files)}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    table_data = [
        ["Evidence File", "Type", "Size"]
    ]

    for file in evidence_files:
        table_data.append([
            file.name,
            file.suffix.lower(),
            f"{file.stat().st_size} bytes"
        ])

    table = Table(
        table_data,
        colWidths=[280, 80, 100]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    content.append(table)

    document.build(content)

    return str(pdf_path)