import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()


class ComplaintAnalysis(BaseModel):
    category: str
    priority: str
    department: str
    summary: str
    reason: str
    detected_location: str


ALLOWED_CATEGORIES = [
    "IT Services",
    "Library Services",
    "Hostel Services",
    "Facilities",
    "Housekeeping",
    "Finance",
    "Academic Services",
    "General Administration",
]

ALLOWED_PRIORITIES = [
    "Critical",
    "High",
    "Medium",
    "Low",
]

DEPARTMENT_MAPPING = {
    "IT Services": "IT Helpdesk",
    "Library Services": "Library Administration",
    "Hostel Services": "Hostel Maintenance",
    "Facilities": "Campus Maintenance",
    "Housekeeping": "Housekeeping Department",
    "Finance": "Accounts Office",
    "Academic Services": "Examination Cell",
    "General Administration": "Administrative Office",
}


def analyse_complaint_with_gemini(
    complaint: str,
    location: str = "",
) -> ComplaintAnalysis:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a complaint analysis agent for a college campus.

Analyse the complaint and return structured information.

Complaint:
{complaint}

Location entered by user:
{location or "Not provided"}

Allowed categories:
{", ".join(ALLOWED_CATEGORIES)}

Allowed priorities:
{", ".join(ALLOWED_PRIORITIES)}

Department mapping:
- IT Services -> IT Helpdesk
- Library Services -> Library Administration
- Hostel Services -> Hostel Maintenance
- Facilities -> Campus Maintenance
- Housekeeping -> Housekeeping Department
- Finance -> Accounts Office
- Academic Services -> Examination Cell
- General Administration -> Administrative Office

Priority rules:
- Critical: fire, electric shock, smoke, flooding, immediate safety danger
- High: urgent deadline, exam tomorrow, essential service unavailable
- Medium: normal complaint that affects work or campus activity
- Low: minor issue or general suggestion

Instructions:
1. Choose exactly one allowed category.
2. Choose exactly one allowed priority.
3. Use the mapped department for the selected category.
4. Write a short one-sentence summary.
5. Explain briefly why the category and priority were selected.
6. Use the user-provided location when available.
7. When location is not provided, infer it only when clearly mentioned.
8. If location cannot be determined, return "Not specified".
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComplaintAnalysis,
            temperature=0.2,
        ),
    )

    if not response.parsed:
        raise ValueError("Gemini did not return valid complaint analysis.")

    analysis = response.parsed

    if analysis.category not in ALLOWED_CATEGORIES:
        analysis.category = "General Administration"

    if analysis.priority not in ALLOWED_PRIORITIES:
        analysis.priority = "Medium"

    analysis.department = DEPARTMENT_MAPPING[analysis.category]

    return analysis