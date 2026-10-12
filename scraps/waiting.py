import streamlit as st

import persist as db

def render():
    if 'waiting_transactions' not in st.session_state:
        st.session_state.waiting_transactions = db.get_waiting_transactions(st.session_state.user.username)

    if len(st.session_state.waiting_transactions) > 0:
        def handle_deny():
            handle_review(st.session_state.row_deny['row'], is_approved=False)

        def handle_approve():
            handle_review(st.session_state.row_approve['row'], is_approved=True)

        def handle_review(row_index: int, is_approved=False):
            # TODO New "approval reason" field in a dialog or popover, so that admin can leave a message for user on why something got denied/accepted?
            record = st.session_state.waiting_transactions[row_index]
            if record:
                db.review_transaction(record['ID'], is_approved, st.session_state.user.username)
                st.toast(
                    f"{':green[APPROVED]' if is_approved else ':red[DENIED]'} the transaction from {record['Owner']} for {record['Amount']}")
                del st.session_state.waiting_transactions

        # TODO Need to handle inline row edits properly, which would mean saving back to db, such as for Current Balance to `user` account
        st.subheader(":crown: Awaiting Your :yellow[Royal Review]", divider=True)
        st.data_editor(
            st.session_state.waiting_transactions,
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "Owner": st.column_config.TextColumn("Owner", disabled=True),
                "Amount": st.column_config.NumberColumn("Amount", format="dollar"),
                "Deny": st.column_config.ButtonColumn(
                    "", on_click=handle_deny, key="row_deny"
                ),
                "Approve": st.column_config.ButtonColumn(
                    "", type="primary", on_click=handle_approve, key="row_approve"
                ),
                "Current Balance": st.column_config.NumberColumn("Current Balance", format="dollar")
            },
            hide_index=True,
        )
