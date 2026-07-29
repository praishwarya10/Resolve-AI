import streamlit as st


st.set_page_config(
    page_title="ResolveAI",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)


student_page = st.Page(
    "student_portal.py",
    title="Student Portal",
    icon="🏠",
    default=True,
)

admin_page = st.Page(
    "pages/Admin_Portal.py",
    title="Admin Portal",
    icon="🧑‍💼",
)


navigation = st.navigation(
    {
        "ResolveAI": [
            student_page,
            admin_page,
        ]
    }
)

navigation.run()
