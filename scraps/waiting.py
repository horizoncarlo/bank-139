import streamlit as st

from support import persist as db


def render():
    if "waiting_transactions" not in st.session_state:
        st.session_state.waiting_transactions = db.get_waiting_transactions(
            st.session_state.user.username
        )

    if len(st.session_state.waiting_transactions) > 0:

        def handle_deny():
            handle_review(st.session_state.row_deny["row"], is_approved=False)

        def handle_approve():
            handle_review(st.session_state.row_approve["row"], is_approved=True)

        def handle_review(row_index: int, is_approved=False):
            record = st.session_state.waiting_transactions[row_index]
            if record:
                db.review_transaction(
                    record["ID"], is_approved, st.session_state.user.username
                )
                st.toast(
                    f"{':green[APPROVED]' if is_approved else ':red[DENIED]'} the transaction from {record['Owner']} for {record['Amount']}"
                )
                del st.session_state.waiting_transactions

        st.subheader(":crown: Awaiting Your :yellow[Royal Review]", divider=True)
        st.dataframe(
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
                "Current Balance": st.column_config.NumberColumn(
                    "Current Balance", format="dollar"
                ),
            },
            hide_index=True,
        )

    with st.container(horizontal_alignment="right"):
        if st.button(
            ":shimmer[Refresh Approvals] :arrows_counterclockwise:", type="tertiary"
        ):
            del st.session_state.waiting_transactions
            st.rerun()
