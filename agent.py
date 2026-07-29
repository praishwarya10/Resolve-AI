from database import save_complaint
from email_service import send_department_notification
from gemini_service import analyse_complaint_with_gemini
from report_pdf import generate_report_pdf
from tools import (
    assign_department,
    calculate_priority,
    classify_category,
    generate_ticket,
)


def process_complaint(
    complaint: str,
    location: str,
    student_email: str,
) -> dict:
    if not complaint or not complaint.strip():
        raise ValueError(
            "Complaint description cannot be empty."
        )

    if not student_email or not student_email.strip():
        raise ValueError(
            "Student email cannot be empty."
        )

    complaint = complaint.strip()
    location = location.strip() if location else ""
    student_email = student_email.strip()

    try:
        analysis = analyse_complaint_with_gemini(
            complaint=complaint,
            location=location,
        )

        category = analysis.category
        priority = analysis.priority
        department = analysis.department
        summary = analysis.summary
        reason = analysis.reason
        detected_location = (
            analysis.detected_location
            or location
            or "Not specified"
        )

        analysis_source = "Gemini AI"

    except Exception as error:
        print(f"Gemini analysis failed: {error}")

        category = classify_category(complaint)
        priority = calculate_priority(complaint)
        department = assign_department(category)

        summary = complaint[:120]

        reason = (
            "Gemini analysis was unavailable, so the complaint "
            "was processed using the rule-based fallback."
        )

        detected_location = location or "Not specified"
        analysis_source = "Rule-based fallback"

    ticket = generate_ticket()

    result = {
        "ticket_id": ticket["ticket_id"],
        "complaint": complaint,
        "location": detected_location,
        "student_email": student_email,
        "category": category,
        "priority": priority,
        "department": department,
        "status": ticket["status"],
        "created_at": ticket["created_at"],
        "summary": summary,
        "reason": reason,
        "analysis_source": analysis_source,
    }

    save_complaint(
        ticket_id=result["ticket_id"],
        complaint=result["complaint"],
        location=result["location"],
        student_email=result["student_email"],
        category=result["category"],
        priority=result["priority"],
        department=result["department"],
        status=result["status"],
        created_at=result["created_at"],
    )

    try:
        email_sent, email_message = (
            send_department_notification(
                ticket_id=result["ticket_id"],
                complaint=result["complaint"],
                location=result["location"],
                student_email=result["student_email"],
                category=result["category"],
                priority=result["priority"],
                department=result["department"],
                summary=result["summary"],
            )
        )

    except Exception as error:
        email_sent = False
        email_message = str(error)

    result["email_sent"] = email_sent
    result["email_message"] = email_message

    pdf_path = generate_report_pdf(result)
    result["pdf_path"] = pdf_path

    return result