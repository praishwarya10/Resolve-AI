import os

import streamlit as st

from agent import process_complaint
from database import (
    create_database,
    get_all_complaints,
)


st.set_page_config(
    page_title="ResolveAI",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)


create_database()

st.title("🛠️ ResolveAI")
st.subheader("Intelligent Complaint Resolution Agent")

st.write(
    "Enter a complaint below. The system will analyse it, "
    "assign a priority, select the correct department, "
    "and create a complaint ticket."
)

st.divider()

complaint = st.text_area(
    "Complaint Description",
    placeholder=(
        "Example: The projector in Room 305 is not working "
        "and we have a presentation tomorrow."
    ),
    height=150,
)

location = st.text_input(
    "Location",
    placeholder="Example: Room 305",
)
student_email = st.text_input(
    "Email Address",
    placeholder="Example: student@college.edu",
)
submitted = st.button(
    "Analyse Complaint",
    type="primary",
)

if submitted:
    if not complaint.strip():
        st.error("Please enter a complaint description.")
    elif not student_email.strip():
        st.error("Please enter your email address.")

    elif "@" not in student_email or "." not in student_email:
        st.error("Please enter a valid email address.")

    else:
        try:
            result = process_complaint(
                complaint=complaint,
                location=location,
                student_email=student_email,
            )

            st.success(
                "Complaint analysed and ticket generated successfully."
            )
            if result["email_sent"]:
                st.success("📧 Department notification sent successfully.")
            else:
                st.warning(
                    f"Ticket created, but email could not be sent.\n\n"
                    f"{result['email_message']}"
                    )
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Category", result["category"])

            with col2:
                st.metric("Priority", result["priority"])

            with col3:
                st.metric("Status", result["status"])

            st.subheader("Complaint Details")

            st.write("**Ticket ID:**", result["ticket_id"])
            st.write("**Complaint:**", result["complaint"])
            st.write("**Location:**", result["location"])
            st.write(
                "**Assigned Department:**",
                result["department"],
            )
            st.write("**Summary:**", result["summary"])
            st.write("**AI Reasoning:**", result["reason"])
            st.write(
                "**Analysed Using:**",
                result["analysis_source"],
            )
            st.write("**Created At:**", result["created_at"])

            new_pdf_path = result["pdf_path"]

            if os.path.exists(new_pdf_path):
                with open(new_pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 Download Complaint Report",
                        data=pdf_file.read(),
                        file_name=f"{result['ticket_id']}.pdf",
                        mime="application/pdf",
                        key=f"new_download_{result['ticket_id']}",
                    )
            else:
                st.warning("PDF report was not generated.")

        except Exception as error:
            st.error(
                f"Complaint processing failed: {error}"
            )

st.divider()

st.subheader("Complaint History")

if st.button("View Saved Complaints"):
    complaints = get_all_complaints()

    if not complaints:
        st.info("No complaints have been saved yet.")

    else:
        for index, complaint_record in enumerate(complaints):
            (
                ticket_id,
                complaint_text,
                saved_location,
                saved_student_email,
                category,
                priority,
                department,
                status,
                created_at,
            ) = complaint_record

            with st.expander(
                f"{ticket_id} | {category} | {priority} | {status}"
            ):
                st.write(
                    "**Complaint:**",
                    complaint_text,
                )

                st.write(
                    "**Location:**",
                    saved_location or "Not provided",
                )

                st.write(
                    "**Department:**",
                    department,
                )

                st.write(
                    "**Status:**",
                    status,
                        )
                st.write(
                    "**Created At:**",
                    created_at,
                )
                st.write(
                    "**Student Email:**",
                    saved_student_email or "Not provided",
                )
                history_pdf_path = os.path.join(
                    "reports",
                    f"NEW_{ticket_id}.pdf",
                )

                if os.path.exists(history_pdf_path):
                    with open(history_pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📄 Download Complaint Report",
                            data=pdf_file.read(),
                            file_name=f"NEW_{ticket_id}.pdf",
                            mime="application/pdf",
                            key=f"history_download_{ticket_id}_{index}",
                        )
                else:
                    st.warning(
                        "PDF report is not available for this complaint."
                    )