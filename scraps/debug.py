import streamlit as st
import persist as db

def render():
    with st.expander(":orange-badge[:desktop_computer: DEBUG SETTINGS]"):
        msg = None
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Become Admin", width=150):
                st.session_state.logged_in = True
                st.session_state.user = db.get_first_admin_user()
                del st.session_state.transactions
        with col2:
            if st.button("Become User", width=150):
                st.session_state.logged_in = True
                st.session_state.user = db.get_first_user()
                del st.session_state.transactions
        with col3:
            if st.button("Clear Session", width=150):
                st.session_state.clear()
                msg = "Browser session data has been cleared"
        with col4:
            if st.button("Delete DB", width=150):
                db.delete_all()
                msg = "Deleted the entire database, refresh the page to redo initialization"

        if msg:
            st.success(msg)