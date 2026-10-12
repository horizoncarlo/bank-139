import streamlit as st

from support import persist as db
from support import util, workarounds


def render():
    if util.DEBUG:
        st.session_state.logged_in = True
        st.session_state.user = db.get_first_admin_user()
        return

    stop_flow = True

    with st.form("login_form"):
        st.write("### Welcome to :rainbow[Bank 139], please :shimmer[login]")
        st.text_input(
            "Username",
            key="username",
            on_change="ignore",
            required=True,
            placeholder="Enter your username",
        )
        workarounds.focus_element("Enter your username")
        st.text_input(
            "Password",
            key="password",
            on_change="ignore",
            required=True,
            type="password",
            placeholder="Enter your password",
        )

        if (
            "username" in st.session_state
            and "password" in st.session_state
            and st.form_submit_button(":+1: Submit Login", type="primary")
        ):
            user = db.login(st.session_state["username"], st.session_state["password"])
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user

                st.success(f"Login successful as {user.name}")
                stop_flow = False
            else:
                st.error("Login failed, just keep trying maybe...")

    st.stop() if stop_flow else st.rerun()
