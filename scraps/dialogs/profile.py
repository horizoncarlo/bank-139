from dataclasses import replace

import streamlit as st

from support import persist as db
from support import workarounds


@st.dialog("Edit Profile")
def dialog_edit_profile():
    # Intentionally put Emoji outside the form, so we can use "live" and show a preview right away
    with st.container(horizontal=True, vertical_alignment="center"):
        if "new_emoji" not in st.session_state:
            st.session_state.new_emoji = st.session_state.user.emoji

        st.text_input(
            "Emoji",
            key="new_emoji",
            help="View your options at https://getemoji.com/",
            max_chars=30,
            autocomplete="off",
            live=True,
        )
        st.markdown(f"## {st.session_state.new_emoji}")

    with st.form("profile_form", border=False):
        st.text_input(
            "Name",
            key="new_name",
            value=st.session_state.user.name,
            required=True,
            max_chars=30,
            autocomplete="off",
            placeholder="Enter a new name",
        )
        workarounds.focus_element(by_placeholder_text="Enter a new name")
        st.text_input(
            "Your Slogan",
            key="new_message",
            value=st.session_state.user.message,
            max_chars=200,
            autocomplete="off",
        )
        st.divider()
        st.text_input("New Password", key="new_password", type="password", max_chars=20)

        if st.form_submit_button(":floppy_disk: :blue[Save Profile]"):
            # Determine what has changed, and only apply those
            to_save = replace(
                st.session_state.user,
                password=st.session_state.new_password
                or st.session_state.user.password,
                emoji=st.session_state.new_emoji,
                name=st.session_state.new_name or st.session_state.user.name,
                message=st.session_state.new_message,
            )

            db.update_user(to_save)
            st.session_state.user = to_save
            st.toast("Profile changes successfully saved")
            st.rerun()
