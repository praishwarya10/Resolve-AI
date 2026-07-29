from datetime import datetime
from database import get_next_ticket_number

def classify_category(complaint: str) -> str:

    text = complaint.lower()

    if any(word in text for word in [
        "wifi", "internet", "computer", "projector",
        "printer", "software", "portal", "login",
        "password", "website", "system"
    ]):
        return "IT Services"

    if any(word in text for word in [
        "library", "book", "id card", "library card",
        "access card", "entry gate"
    ]):
        return "Library Services"

    if any(word in text for word in [
        "hostel", "room", "warden", "mess",
        "water", "toilet", "bathroom"
    ]):
        return "Hostel Services"

    if any(word in text for word in [
        "chair", "desk", "door", "window",
        "fan", "light", "ac", "classroom"
    ]):
        return "Facilities"

    if any(word in text for word in [
        "clean", "garbage", "dust",
        "dirty", "washroom", "waste"
    ]):
        return "Housekeeping"

    if any(word in text for word in [
        "fees", "payment", "refund",
        "scholarship", "accounts"
    ]):
        return "Finance"

    if any(word in text for word in [
        "exam", "registration", "hall ticket",
        "marks", "result", "attendance"
    ]):
        return "Academic Services"

    return "General Administration"


def calculate_priority(complaint: str) -> str:
    text = complaint.lower()

    critical_words = ["fire", "smoke", "shock", "sparking", "flood", "danger"]
    high_words = ["urgent", "tomorrow", "exam", "presentation", "broken", "not working"]

    if any(word in text for word in critical_words):
        return "Critical"

    if any(word in text for word in high_words):
        return "High"

    return "Medium"


def assign_department(category: str) -> str:

    department_map = {

        "IT Services": "IT Helpdesk",

        "Library Services": "Library Administration",

        "Hostel Services": "Hostel Maintenance",

        "Facilities": "Campus Maintenance",

        "Housekeeping": "Housekeeping Department",

        "Finance": "Accounts Office",

        "Academic Services": "Examination Cell",

        "General Administration": "Administrative Office"
    }

    return department_map.get(
        category,
        "Administrative Office"
    )



def generate_ticket() -> dict:
    now = datetime.now()
    ticket_number = get_next_ticket_number()

    ticket_id = (
        f"AVVP-{now.strftime('%Y%m%d')}-"
        f"{ticket_number:03d}"
    )

    return {
        "ticket_id": ticket_id,
        "status": "New",
        "created_at": now.strftime("%d-%b-%Y %I:%M %p"),
    }