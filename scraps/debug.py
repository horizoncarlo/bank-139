import streamlit as st
import persist as db

def render():
    with st.expander(":orange-badge[:desktop_computer: DEBUG SETTINGS]"):
        msg = None
        stop_requested = False

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Become Admin", width=150):
                st.session_state.logged_in = True
                st.session_state.user = db.get_first_admin_user()
                del st.session_state.transactions
                del st.session_state.waiting_transactions
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
                db.delete_all_tables()
                msg = "Deleted the entire database, refresh the page to redo initialization"
                stop_requested = True

        # Put at the bottom so the message formats our entire column width
        if msg:
            st.success(msg)
        if stop_requested:
            st.stop()
