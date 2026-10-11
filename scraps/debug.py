import streamlit as st
import persist as db

def render():
    with st.expander(":orange-badge[:desktop_computer: DEBUG SETTINGS]"):
        msg = None
        col1, col2 = st.columns(2, width=400)
        with col1:
            if st.button("Clear Session", width=150):
                st.session_state.clear()
                msg = "Browser session data has been cleared"
        with col2:
            if st.button("Delete DB", width=150):
                db.delete_all()
                msg = "Deleted the entire database, refresh the page to redo initialization"

        if msg:
            st.success(msg)