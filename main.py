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
                   layout="wide" if st.session_state.get('logged_in', util.DEBUG) else "centered",
                   initial_sidebar_state="collapsed")

# Initialize the db, which creates all necessary tables, sets up the connection, etc.
db.init()

# If we're not logged in, show that screen
if 'logged_in' not in st.session_state:
    scraps.login.render()
if 'need_balloons' in st.session_state:
    st.balloons() # Celebrate a bit
    del st.session_state.need_balloons

# Show our debug options
if util.DEBUG:
    scraps.debug.render()

# If we haven't fetch transactions do that
if 'transactions' not in st.session_state:
    st.session_state.transactions = db.get_recent_transactions(st.session_state.user.username)
# If we don't have a calculated pending balance do that now
if not st.session_state.user.pending_balance:
    st.session_state.user.pending_balance = db.get_pending_total(st.session_state.user.username)

@st.dialog("Transaction")
def do_transaction(deposit = True):
    with st.form("trans_form"):
        trans_type = ':moneybag: :green[Deposit]' if deposit else ':money_with_wings: :red[Withdraw]'

        st.write(f"### Preparing to make a {trans_type}...")

        st.number_input("Amount ($) :orange[*]", key="trans_amount", on_change="ignore", required=True, value=None, min_value=0.0, max_value=1000.0, step=0.5, format="%0.2f")
        st.text_area("Description and Notes :orange[*]", key="trans_description", on_change="ignore")
        st.text_input("Location", key="trans_location", on_change="ignore")

        if 'trans_amount' in st.session_state and 'trans_description' in st.session_state and st.form_submit_button(trans_type):
            if st.session_state.trans_amount <= 0:
                st.error("Enter an Amount bigger than $0 of course")
                return

            amount_as_cents = round(abs(st.session_state.trans_amount) * (1 if deposit else -1) * 100, 2)  # Store based on deposit or withdraw

            db.create_transaction(username=st.session_state.user.username,
                                  amount_as_cents=amount_as_cents,
                                  description=st.session_state.trans_description,
                                  location=st.session_state.trans_location,
                                  is_admin=st.session_state.user.is_admin)

            # TODO ntfy.sh admin channel about new transaction?

            out_of_money = False
            if not deposit and not st.session_state.user.is_admin:
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

# TODO Entire approval process. Maybe a new "approval reason" column so we can leave a message for the kids of why something got denied or accepted

# Render header for transactions
col1, col2, col3, col4 = st.columns(4, gap=None)
with col1:
    st.write(f"## {st.session_state.user.emoji} {st.session_state.user.name} at :rainbow[Bank 139]")
    st.write("_Total change over the last 2 weeks_")
with col2:
    st.metric("Balance", util.money(st.session_state.user.balance), f"{db.calc_balance_delta()}%")
with col3:
    if not st.session_state.user.is_admin:
        if st.session_state.user.balance - (st.session_state.user.pending_balance * -1) < 0:
            st.metric("Pending", util.money(st.session_state.user.pending_balance, disable_color=True), delta="In Debt", delta_color="red", delta_arrow="off")
        else:
            st.metric("Pending", util.money(st.session_state.user.pending_balance, disable_color=True))
with col4:
    with st.container():
        if st.button(":moneybag: Deposit", width=200, type="primary"):
            do_transaction(deposit=True)
        if st.button(":money_with_wings: Withdraw", width=200):
            do_transaction(deposit=False)

# TODO Users should be able to delete their reviewed and REJECTED transactions, to keep the table clean. Means a data_editor instead of dataframe
scraps.transactions.render()

# TODO Move the approval table to a new `scraps`
if st.session_state.user.is_admin:
    if 'waiting_transactions' not in st.session_state:
        st.session_state.waiting_transactions = db.get_waiting_transactions(st.session_state.user.username)

    if len(st.session_state.waiting_transactions) > 0:
        def handle_deny():
            handle_review(st.session_state.row_deny['row'], is_approved=False)

        def handle_approve():
            handle_review(st.session_state.row_approve['row'], is_approved=True)

        def handle_review(row_index: int, is_approved = False):
            record = st.session_state.waiting_transactions[row_index]
            if record:
                db.review_transaction(record['ID'], is_approved, st.session_state.user.username)
                st.toast(f"{':green[APPROVED]' if is_approved else ':red[DENIED]'} the transaction from {record['Owner']} for {record['Amount']}")
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
