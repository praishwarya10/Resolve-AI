import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def generate_report_pdf(result: dict) -> str:
    os.makedirs("reports", exist_ok=True)

    file_path = os.path.join(
        "reports",
        f"NEW_{result['ticket_id']}.pdf",
    )

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        spaceAfter=14,
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=4,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        textColor=colors.black,
        spaceAfter=5,
        splitLongWords=True,
        wordWrap="CJK",
    )

    footer_style = ParagraphStyle(
        "ReportFooter",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#666666"),
    )

    def clean_text(value) -> str:
        text = str(value or "Not provided")
        text = escape(text)
        return text.replace("\n", "<br/>")

    def add_field(label: str, value):
        return Paragraph(
            f"<b>{escape(label)}:</b> {clean_text(value)}",
            body_style,
        )

    def add_divider():
        return HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.HexColor("#777777"),
            spaceBefore=6,
            spaceAfter=10,
        )

    story = []

    story.append(
        Paragraph(
            "RESOLVEAI",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Complaint Resolution Report",
            subtitle_style,
        )
    )

    story.append(add_divider())

    story.append(
        add_field(
            "Ticket ID",
            result.get("ticket_id"),
        )
    )

    story.append(
        add_field(
            "Status",
            result.get("status"),
        )
    )

    story.append(
        add_field(
            "Created At",
            result.get("created_at"),
        )
    )

    story.append(Spacer(1, 8))
    story.append(add_divider())

    story.append(
        Paragraph(
            "Student Details",
            section_style,
        )
    )

    story.append(
        add_field(
            "Email",
            result.get("student_email"),
        )
    )

    story.append(
        add_field(
            "Location",
            result.get("location"),
        )
    )

    story.append(Spacer(1, 8))
    story.append(add_divider())

    story.append(
        Paragraph(
            "Complaint",
            section_style,
        )
    )

    story.append(
        Paragraph(
            clean_text(result.get("complaint")),
            body_style,
        )
    )

    story.append(Spacer(1, 8))
    story.append(add_divider())

    story.append(
        Paragraph(
            "AI Analysis",
            section_style,
        )
    )

    story.append(
        add_field(
            "Category",
            result.get("category"),
        )
    )

    story.append(
        add_field(
            "Priority",
            result.get("priority"),
        )
    )

    story.append(
        add_field(
            "Department",
            result.get("department"),
        )
    )

    story.append(
        add_field(
            "Analysis Source",
            result.get("analysis_source"),
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Summary:</b>",
            body_style,
        )
    )

    story.append(
        Paragraph(
            clean_text(result.get("summary")),
            body_style,
        )
    )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            "<b>Reason:</b>",
            body_style,
        )
    )

    story.append(
        Paragraph(
            clean_text(result.get("reason")),
            body_style,
        )
    )

    story.append(Spacer(1, 12))
    story.append(add_divider())

    story.append(
        Paragraph(
            "Generated by ResolveAI",
            footer_style,
        )
    )

    story.append(
        Paragraph(
            "Powered by Google Gemini",
            footer_style,
        )
    )

    document.build(story)

    print(
        "REPORT PDF GENERATED:",
        os.path.abspath(file_path),
    )

    return file_path