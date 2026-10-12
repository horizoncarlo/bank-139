import streamlit as st

# These are mostly client-side workarounds. Streamlit seems to change and update and improve often, so over time these might not be necessary
# Workarounds are based on Oct 2026


def always_show_scrollbar():
    """
    No way to control scrolling, so we unfortunately need to touch CSS, defeating the ENTIRE PURPOSE (lol)
    """
    st.html("<style>.stMain { overflow-y: scroll; }</style>")


def focus_element(by_placeholder_text):
    """
    No way to focus an element, such as an input from st.text_input, so we insert some client side JS
    """
    st.html(
        f"""<script>
        setTimeout(() => {{
            document.querySelector(\"[placeholder='{by_placeholder_text}']\")?.focus();
        }}, 100);
    </script>""",
        unsafe_allow_javascript=True,
    )
