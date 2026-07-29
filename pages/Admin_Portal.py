import streamlit as st

from database import (
    create_database,
    get_all_complaints,
    update_complaint_status,
)

from email_service import send_resolution_notification


st.set_page_config(
    page_title="ResolveAI Admin",
    page_icon="🧑‍💼",
    layout="wide",
)

create_database()

st.title("🧑‍💼 ResolveAI Admin Portal")
st.subheader("Complaint Management")

st.write(
    "Review complaints, update ticket status, "
    "and notify students when issues are resolved."
)

st.divider()

complaints = get_all_complaints()

if not complaints:
    st.info("No complaints have been submitted yet.")

else:
    for index, complaint_record in enumerate(complaints):
        (
            ticket_id,
            complaint_text,
            saved_location,
            student_email,
            category,
            priority,
            department,
            status,
            created_at,
        ) = complaint_record

        with st.expander(
            f"{ticket_id} | {category} | "
            f"{priority} | {status}"
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
                "**Student Email:**",
                student_email or "Not provided",
            )

            st.write(
                "**Category:**",
                category,
            )

            st.write(
                "**Priority:**",
                priority,
            )

            st.write(
                "**Assigned Department:**",
                department,
            )

            st.write(
                "**Created At:**",
                created_at,
            )

            status_options = [
                "New",
                "Assigned",
                "In Progress",
                "Resolved",
            ]

            current_status_index = (
                status_options.index(status)
                if status in status_options
                else 0
            )

            selected_status = st.selectbox(
                "Update Status",
                status_options,
                index=current_status_index,
                key=f"admin_status_{ticket_id}_{index}",
            )

            if st.button(
                "Save Status",
                key=f"save_status_{ticket_id}_{index}",
            ):
                if selected_status == status:
                    st.info(
                        "No status change was made."
                    )

                else:
                    update_complaint_status(
                        ticket_id=ticket_id,
                        new_status=selected_status,
                    )

                    if (
                        selected_status == "Resolved"
                        and status != "Resolved"
                    ):
                        if not student_email:
                            st.warning(
                                "Status updated, but the student "
                                "email is missing."
                            )

                        else:
                            email_sent, email_message = (
                                send_resolution_notification(
                                    ticket_id=ticket_id,
                                    student_email=student_email,
                                    complaint=complaint_text,
                                    department=department,
                                )
                            )

                            if email_sent:
                                st.success(
                                    "Status updated to Resolved "
                                    "and email sent to the student."
                                )

                            else:
                                st.warning(
                                    "Status updated to Resolved, "
                                    "but the email could not be sent."
                                )

                                st.error(email_message)

                    else:
                        st.success(
                            f"Status updated to "
                            f"{selected_status}."
                        )

                    st.rerun()
                    