import streamlit as st

from support import persist as db, workarounds, util

@st.dialog("Transaction")
def dialog_do_transaction(deposit = True):
    with st.form("trans_form"):
        trans_type = ':moneybag: :green[Deposit]' if deposit else ':money_with_wings: :red[Withdraw]'

        st.write(f"### Preparing to make a {trans_type}...")

        st.number_input("Amount ($) :orange[*]", key="trans_amount", on_change="ignore", required=True, value=None, min_value=0.0, max_value=1000.0, step=0.5, format="%0.2f", placeholder="Enter the money")
        workarounds.focus_element(by_placeholder_text="Enter the money")
        st.text_area("Description and Notes :orange[*]", key="trans_description", on_change="ignore")
        st.text_input("Location", key="trans_location", on_change="ignore")
        if st.session_state.user.is_admin:
            basic_users = db.get_all_non_admin_users()
            st.divider()
            st.selectbox("For a Different User?", key="trans_target", on_change="ignore", options=basic_users, index=None)

        if 'trans_amount' in st.session_state and 'trans_description' in st.session_state and st.form_submit_button(trans_type):
            if st.session_state.trans_amount <= 0:
                st.error("Enter an Amount bigger than $0 of course")
                return

            amount_as_cents = round(abs(st.session_state.trans_amount) * (1 if deposit else -1) * 100, 2)  # Store based on deposit or withdraw

            db.create_transaction(username=st.session_state.user.username,
                                  amount_as_cents=amount_as_cents,
                                  description=st.session_state.trans_description,
                                  location=st.session_state.trans_location,
                                  is_admin=st.session_state.user.is_admin,
                                  for_username=st.session_state.trans_target if 'trans_target' in st.session_state else None)

            # Send a notification for user approvals
            if not st.session_state.user.is_admin:
                util.send_phone_notification(username=st.session_state.user.username, is_deposit=deposit,
                                             amount_as_cents=amount_as_cents, description=st.session_state.trans_description)

            out_of_money = False
            if not deposit:
                if not st.session_state.user.is_admin:
                    out_of_money = st.session_state.user.balance + amount_as_cents < 0
            else:
                st.session_state.need_balloons = True
            st.toast(f"Completed new {trans_type} for ${st.session_state.trans_amount:.2f}! {'\n\nNote you would be :red-badge[OUT OF MONEY] from this transaction. Good luck with approval :smirk:' if out_of_money else ''}", duration="long" if out_of_money else "short")

            if st.session_state.user.is_admin:
                st.session_state.user.balance += amount_as_cents

            # Clear our transactions in-memory so we refetch
            del st.session_state.transactions
            del st.session_state.user.pending_balance
            st.rerun()