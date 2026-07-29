
import os
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


def generate_complaint_pdf(result: dict) -> str:
    os.makedirs("reports", exist_ok=True)

    file_path = os.path.join(
        "reports",
        f"{result['ticket_id']}.pdf",
    )
    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ResolveAITitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        spaceAfter=16,
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1F2937"),
        spaceBefore=8,
        spaceAfter=7,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.black,
        spaceAfter=5,
        wordWrap="CJK",
    )

    label_style = ParagraphStyle(
        "LabelBody",
        parent=body_style,
        leftIndent=0,
        spaceAfter=4,
    )

    footer_style = ParagraphStyle(
        "FooterText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#666666"),
    )

    def clean(value):
        return escape(str(value or "Not provided")).replace(
            "\n",
            "<br/>",
        )

    def detail_line(label, value):
        return Paragraph(
            f"<b>{escape(label)}:</b> {clean(value)}",
            label_style,
        )

    def divider():
        return HRFlowable(
            width="100%",
            thickness=0.8,
            color=colors.HexColor("#888888"),
            spaceBefore=5,
            spaceAfter=8,
        )

    story = []

    story.append(Paragraph("ResolveAI", title_style))
    story.append(
        Paragraph(
            "Complaint Resolution Report",
            subtitle_style,
        )
    )
    story.append(divider())

    story.append(
        detail_line(
            "Ticket ID",
            result.get("ticket_id"),
        )
    )
    story.append(
        detail_line(
            "Status",
            result.get("status"),
        )
    )
    story.append(
        detail_line(
            "Created At",
            result.get("created_at"),
        )
    )

    story.append(Spacer(1, 8))
    story.append(divider())

    story.append(
        Paragraph(
            "Student Details",
            section_style,
        )
    )

    story.append(
        detail_line(
            "Email",
            result.get("student_email"),
        )
    )
    story.append(
        detail_line(
            "Location",
            result.get("location"),
        )
    )

    story.append(Spacer(1, 8))
    story.append(divider())

    story.append(
        Paragraph(
            "Complaint",
            section_style,
        )
    )

    story.append(
        Paragraph(
            clean(result.get("complaint")),
            body_style,
        )
    )

    story.append(Spacer(1, 8))
    story.append(divider())

    story.append(
        Paragraph(
            "AI Analysis",
            section_style,
        )
    )

    story.append(
        detail_line(
            "Category",
            result.get("category"),
        )
    )
    story.append(
        detail_line(
            "Priority",
            result.get("priority"),
        )
    )
    story.append(
        detail_line(
            "Department",
            result.get("department"),
        )
    )
    story.append(
        detail_line(
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
            clean(result.get("summary")),
            body_style,
        )
    )

    story.append(Spacer(1, 4))

    story.append(
        Paragraph(
            "<b>Reason:</b>",
            body_style,
        )
    )

    story.append(
        Paragraph(
            clean(result.get("reason")),
            body_style,
        )
    )

    story.append(Spacer(1, 12))
    story.append(divider())

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

    return file_path