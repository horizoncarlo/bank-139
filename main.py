import streamlit as st

import persist as db
import workarounds
import util

# Torn on the "scraps" concept, where smaller individual rendering pieces are put into component-like individual files
# Easier to read this main script, but marginally harder to track down where a particular UI element comes from
import scraps.debug
import scraps.header
import scraps.login
import scraps.transactions
import scraps.waiting

# Setup our global page config
st.set_page_config(page_title="Bank 139 - \"Real World Money. Virtually\"",
                   page_icon=":money_mouth_face:",
                   layout="wide" if st.session_state.get('logged_in', util.DEBUG) else "centered",
                   initial_sidebar_state="collapsed")

# Always show the vertical scrollbar
workarounds.always_show_scrollbar()

# Initialize the db, which creates all necessary tables, sets up the connection, etc.
db.init()

# If we're not logged in, show that screen
if 'logged_in' not in st.session_state:
    scraps.login.render()
if 'need_balloons' in st.session_state:
    st.balloons() # Celebrate a bit
    del st.session_state.need_balloons

# Remember the actual order in the code of rendering statements is important in Streamlit
# Like the old PHP days
if util.DEBUG:
    scraps.debug.render()

# If we haven't fetch transactions do that
if 'transactions' not in st.session_state:
    st.session_state.transactions = db.get_recent_transactions(st.session_state.user.username)
# If we don't have a calculated pending balance do that now
if not st.session_state.user.pending_balance:
    st.session_state.user.pending_balance = db.get_pending_total(st.session_state.user.username)

scraps.header.render()
scraps.transactions.render()

if st.session_state.user.is_admin:
    scraps.waiting.render()