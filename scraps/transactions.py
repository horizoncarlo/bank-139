import streamlit as st
import pandas as pd

import util

def render():
    if len(st.session_state.get('transactions', [])) == 0:
        st.divider()
        st.info("No transactions yet, go spend or get some :green[money]!")
        return

    transactions = pd.DataFrame(st.session_state.transactions)
    transactions["approved_at"] = pd.to_datetime(transactions["approved_at"], unit="s")
    transactions["created_at"] = pd.to_datetime(transactions["created_at"], unit="s")

    # TODO See https://docs.streamlit.io/develop/api-reference/data/st.column_config for dataframe column config
    trans_config = {
        "amount": st.column_config.NumberColumn(
            label="Amount",
            format="dollar" # TODO Need to use util.money here
        ),
        "description": "Description",
        "location": "Location",
        "is_approved": st.column_config.MarkdownColumn("Approved?"),
        "approved_by": "Approved By",
        "approved_at": st.column_config.DatetimeColumn("Approved At", format="distance"),
        "created_at": st.column_config.DatetimeColumn("Date", format=util.DEFAULT_DATE_FORMAT)
    }

    st.dataframe(transactions,
                 column_config=trans_config,
                 height="content",
                 on_select="ignore",
                 hide_index=True)