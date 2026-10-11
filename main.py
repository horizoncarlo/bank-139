import streamlit as st

import persist as db
import util

# Torn on the "scraps" concept, where smaller individual rendering pieces are put into component-like individual files
# Easier to read this main script, but marginally harder to track down where a particular UI element comes from
import scraps.debug
import scraps.login
import scraps.transactions

# Setup our global page config
st.set_page_config(page_title="Bank 139 - \"Real World Money. Virtually\"",
                   page_icon=":money_mouth_face:",
                   layout="wide" if st.session_state.get('logged_in') else "centered",
                   initial_sidebar_state="collapsed")

# Initialize the db, which creates all necessary tables, sets up the connection, etc.
db.init()

# If we're not logged in, show that screen
if 'logged_in' not in st.session_state:
    scraps.login.render()

# Our debug options
if util.DEBUG:
    scraps.debug.render()

if 'transactions' not in st.session_state:
    st.session_state.transactions = db.get_recent_transactions(st.session_state.user.username)

# Render header for transactions
col1, col2, col3 = st.columns(3, gap=None)
with col1:
    st.write(f"## {st.session_state.user.emoji} {st.session_state.user.name} at :rainbow[Bank 139]")
    st.write("_Total change over the last 2 weeks_")
with col2:
    st.metric("Balance", util.money(st.session_state.user.balance), f"{db.calc_balance_delta()}%")
with col3:
    with st.container():
        st.button(":moneybag: Deposit", width=200, type="primary")
        st.button(":money_with_wings: Withdraw", width=200)

scraps.transactions.render()