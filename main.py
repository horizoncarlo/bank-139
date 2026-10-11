import streamlit as st
import pandas as pd
import persist as db
import util

_DEBUG = st.secrets.get("is_dev", True)

if _DEBUG and st.button("Clear Session"):
    st.session_state.clear()

if 'user' not in st.session_state:
    st.session_state.user = db.get_current_user()
    print(f"USER IS {st.session_state.user}")

st.set_page_config(page_title="Bank 139 - \"Real World Money. Virtually\"",
                   page_icon=":money_mouth_face:",
                   layout="wide",
                   initial_sidebar_state="collapsed")

col1, col2 = st.columns([3, 1], gap=None, width=700)
with col1:
    st.write(f"## {st.session_state.user.emoji} {st.session_state.user.name} at :rainbow[Bank 139]")
    st.write("_Total change over the last 2 weeks_")
with col2:
    st.metric("Balance", util.money(st.session_state.user.balance), f"{db.calc_balance_delta()}%")

transactions = pd.DataFrame(db.get_transactions())

transactions["approved_at"] = pd.to_datetime(transactions["approved_at"], unit="s")
transactions["created_at"] = pd.to_datetime(transactions["created_at"], unit="s")

default_date_format = "YYYY-MM-DD HH:mm:ss"

trans_config = {
    "amount": st.column_config.NumberColumn(
        label="Amount",
        format="dollar" # TODO Need to use util.money here
    ),
    "description": "Description",
    "location": "Location",
    "is_approved": st.column_config.MarkdownColumn("Approved?"),
    "approved_id": "Approved By",
    "approved_at": st.column_config.DatetimeColumn("Approved At", format="distance"),
    "created_at": st.column_config.DatetimeColumn("Date", format=default_date_format)
}

st.dataframe(transactions,
             column_config=trans_config,
             height="content",
             on_select="ignore",
             hide_index=True)
