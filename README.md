# ResolveAI 🛠️

### Intelligent Campus Complaint Management

ResolveAI is a Python-based campus complaint management application that helps students submit issues and helps administrators manage their resolution. It combines Google Gemini analysis with a rule-based fallback to classify complaints, determine urgency, assign departments, generate tickets, and notify the relevant people.

## The problem

Campus complaints can be difficult to route when students do not know which department is responsible. Manual categorization and follow-up can slow down resolution. ResolveAI organizes that workflow from complaint submission to status updates.

## Key features

- **Student portal:** Submit a complaint with its description, location, and student email address.
- **AI-assisted triage:** Gemini identifies a category, priority, responsible department, short summary, and reasoning.
- **Fallback classification:** Keyword-based rules handle classification if Gemini analysis is unavailable.
- **Ticket generation:** Creates dated IDs such as `AVVP-20260729-001` and records tickets in SQLite.
- **Department notifications:** Sends an SMTP email to the mapped department when configured.
- **Admin portal:** Review tickets and change their status to `New`, `Assigned`, `In Progress`, or `Resolved`.
- **Resolution notifications:** Sends the student an email when an administrator marks a complaint resolved.
- **PDF reports:** Generates a downloadable complaint report using ReportLab.
- **Complaint history:** Displays previously saved complaints.

## How it works

```text
Student submits complaint
          |
          v
Gemini analyses complaint
          |
          +-- If unavailable --> Rule-based classification
          |
          v
Category + priority + department
          |
          v
Generate ticket and save to SQLite
          |
          +--> Notify department by email (if configured)
          |
          +--> Generate downloadable PDF
          |
          v
Admin reviews and updates status
          |
          v
When resolved, notify student by email
```

## Complaint categories

| Category | Assigned department |
| --- | --- |
| IT Services | IT Helpdesk |
| Library Services | Library Administration |
| Hostel Services | Hostel Maintenance |
| Facilities | Campus Maintenance |
| Housekeeping | Housekeeping Department |
| Finance | Accounts Office |
| Academic Services | Examination Cell |
| General Administration | Administrative Office |

Gemini can assign `Critical`, `High`, `Medium`, or `Low` priority. The rule-based fallback supports `Critical`, `High`, and `Medium`.

## Tech stack

| Layer | Technology |
| --- | --- |
| Interface | Streamlit |
| Application logic | Python |
| AI analysis | Google Gemini (`google-genai`) |
| Structured AI output | Pydantic |
| Storage | SQLite |
| Notifications | SMTP / Python `smtplib` |
| PDF generation | ReportLab |
| Configuration | `python-dotenv` |


## Application Screenshots

### Student Portal

Students can submit complaints, enter their location and email address, and receive AI-assisted complaint analysis.

![Student Portal](application%20screenshots/resolveAI_Student%20portal.png)

### Admin Portal

Administrators can review submitted complaints, update their status, and manage the resolution process.

![Admin Portal](application%20screenshots/ResolveAI_Admin%20portal.png)

### AI-Powered Complaint Management

ResolveAI classifies complaints, determines priority, assigns the responsible department, and generates unique complaint tickets.

![Complaint Management](application%20screenshots/ResolveAI-%20complain%20management.png)

### Automated Department Assignment Email

Once a complaint is registered, the assigned department receives an email containing the complaint details.

![Assignment Email](application%20screenshots/ResolveAI%20assignment%20mail.png)

### Complaint Resolution Email

When an administrator marks a complaint as resolved, ResolveAI sends a resolution notification to the student.

![Resolution Email](application%20screenshots/ResolveAI%20resolved%20mail.png)

## Getting started

### Prerequisites

- Python 3.10+ (recommended)
- A Google Gemini API key for AI analysis
- SMTP credentials if you want email notifications

### Installation

```bash
# Clone the repository
git clone https://github.com/praishwarya10/Resolve-AI.git
cd Resolve-AI

# Create a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@example.com
SMTP_PASSWORD=your_smtp_app_password
```

Configure actual department recipient addresses in `config.py` before enabling email notifications. The repository currently maps all departments to a demonstration address.

**Security:** Never commit `.env`, SMTP passwords, API keys, or a database containing real student details. Add `.env`, `.venv/`, `__pycache__/`, `complaints.db`, and `reports/` to `.gitignore` as appropriate.

### Run the application

```bash
streamlit run app.py
```

Use the navigation menu to open the **Student Portal** or **Admin Portal**.

## Project structure

```text
Resolve-AI/
├── app.py                 # Streamlit navigation
├── student_portal.py      # Complaint submission and history
├── pages/
│   └── Admin_Portal.py    # Complaint review and status updates
├── agent.py               # Complaint-processing workflow
├── gemini_service.py      # Gemini analysis and structured output
├── tools.py               # Rule-based classification and ticket creation
├── database.py            # SQLite persistence
├── email_service.py       # Department and resolution notifications
├── report_pdf.py          # PDF report generation
├── config.py              # Department email mapping
└── requirements.txt       # Python dependencies
```

## Example workflow

**Complaint:** “The projector in Room 305 is not working and we have a presentation tomorrow.”

The application analyzes the text, selects a category and priority, assigns a department, and creates a ticket. It then saves the complaint, attempts a department email notification, and makes a PDF report available. An administrator can later change its status and trigger a resolution email.

*The example illustrates the workflow; exact AI classifications can vary.*

## Current scope and limitations

- Designed as a campus-focused prototype, not a production-ready helpdesk.
- Both portals are accessible through the Streamlit navigation; authentication and role-based access control are not implemented in the reviewed code.
- Email delivery requires valid SMTP settings and correctly configured department addresses.
- SQLite is local to the running application.
- AI results depend on the configured Gemini model and API availability; rule-based fallback is available.

## Future improvements

- Student and administrator authentication
- Department-specific dashboards and assignment queues
- Ticket search, filters, and analytics
- Deployment with persistent storage and secure secrets management
- Automated tests and deployment documentation

## Author

Developed as a campus complaint management project.

GitHub: [@praishwarya10](https://github.com/praishwarya10)
