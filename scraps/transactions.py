import streamlit as st
import pandas as pd

import util

def render():
    if len(st.session_state.get('transactions', [])) == 0:
        st.divider()
        st.info("No transactions yet, go spend or get some :green[money]!")
        return

    transactions = pd.DataFrame(st.session_state.transactions)
    transactions["reviewed_at"] = pd.to_datetime(transactions["reviewed_at"], unit="s", utc=True).dt.tz_convert(util.TIMEZONE)
    transactions["created_at"] = pd.to_datetime(transactions["created_at"], unit="s", utc=True).dt.tz_convert(util.TIMEZONE)

    transactions = transactions.style.map(
        lambda amount: "color: green" if amount >= 0 else "color: red",
        subset=["amount"]
    ).format({
        "amount": lambda amount: util.money(amount, disable_color=True)
    })

    # See https://docs.streamlit.io/develop/api-reference/data/st.column_config for dataframe column config
    trans_config = {
        "amount": "Amount",
        "description": "Description",
        "location": "Location",
        "is_approved": "Approved?",
        "reviewed_by": "Reviewed By",
        "reviewed_at": st.column_config.DatetimeColumn("Reviewed At", format="distance"),
        "created_at": st.column_config.DatetimeColumn("Date", format=util.DEFAULT_DATE_FORMAT)
    }

    # TODO Users should be able to delete their reviewed and REJECTED transactions, to keep the table clean. Means a data_editor instead of dataframe
    # TODO Add "cancel transaction" request for non-approved pending options

    st.dataframe(transactions,
                 column_config=trans_config,
                 height="content",
                 on_select="ignore")