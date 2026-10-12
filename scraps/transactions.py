import streamlit as st
import pandas as pd

import persist as db
import util

def render():
    if len(st.session_state.get('transactions', [])) == 0:
        st.divider()
        st.info("No transactions yet, go spend or get some :green[money]!")
        return

    # Mutate our data a bit - wrap as Pandas df, format our timestamps, and add a button column
    # For the waiting/pending transactions scrap we tried this at the DB level instead
    transactions = pd.DataFrame(st.session_state.transactions)
    transactions["reviewed_at"] = pd.to_datetime(transactions["reviewed_at"], unit="s", utc=True).dt.tz_convert(util.TIMEZONE)
    transactions["created_at"] = pd.to_datetime(transactions["created_at"], unit="s", utc=True).dt.tz_convert(util.TIMEZONE)
    transactions["control"] = [
        "Cancel" if (not row.reviewed_by or row.is_approved == "No") else None
        for row in st.session_state.transactions
    ]

    # Convert from a Pandas dataframe to a styled map, so we can color our amounts
    transactions = transactions.style.map(
        lambda amount: "color: green" if amount >= 0 else "color: red",
        subset=["amount"]
    ).format({
        "amount": lambda amount: util.money(amount, disable_color=True)
    })

    def handle_cancel():
        row_index = st.session_state.row_cancel['row']
        record = st.session_state.transactions[row_index]
        if record:
            db.delete_pending_transaction(record, st.session_state.user.username)
            st.toast(f"Successfully canceled pending transaction for {util.money(record.amount)}")
            del st.session_state.transactions
            del st.session_state.user.pending_balance

    # See https://docs.streamlit.io/develop/api-reference/data/st.column_config for dataframe column config
    trans_config = {
        "transaction_id": "ID",
        "amount": "Amount",
        "description": "Description",
        "location": "Location",
        "is_approved": "Approved?",
        "reviewed_by": "Reviewed By",
        "reviewed_at": st.column_config.DatetimeColumn("Reviewed At", format="distance"),
        "created_at": st.column_config.DatetimeColumn("Date", format=util.DEFAULT_DATE_FORMAT),
        "control": st.column_config.ButtonColumn(
            "",
            type="primary",
            on_click=handle_cancel,
            key="row_cancel"
        )
    }

    st.dataframe(transactions,
                   column_config=trans_config,
                   height="content",
                   hide_index=True,)

    with st.container(horizontal_alignment="right"):
        if st.button("Get Entire History", type="tertiary"):
            st.session_state.transactions = db.get_recent_transactions(st.session_state.user.username, fetch_all_instead=True)