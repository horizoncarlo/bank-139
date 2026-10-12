import streamlit as st
import random

import persist as db
import util

from scraps.dialog import do_transaction

def render():
    col1, col2, col3, col4 = st.columns(4, gap=None)
    with col1:
        st.write(f"## {st.session_state.user.emoji} {st.session_state.user.name} at :rainbow[Bank 139]")
        st.write(f"_{st.session_state.user.message}_")
    with col2:
        st.metric("Balance", util.money(st.session_state.user.balance), delta=random.choice(util.POSITIVE_MESSAGES) if st.session_state.user.balance >= 0 else random.choice(util.NEGATIVE_MESSAGES), delta_arrow="off", delta_color="blue")
    with col3:
        if not st.session_state.user.is_admin:
            if st.session_state.user.balance - (st.session_state.user.pending_balance * -1) < 0:
                st.metric("Pending", util.money(st.session_state.user.pending_balance, disable_color=True),
                          delta="In Debt", delta_color="red", delta_arrow="off")
            else:
                st.metric("Pending", util.money(st.session_state.user.pending_balance, disable_color=True))
        else:
            basic_users = db.get_all_non_admin_users()

            def login_as_user():
                if 'login_as_user' in st.session_state and st.session_state.login_as_user:
                    st.session_state.user = db.get_user_by_username(st.session_state.login_as_user)
                    del st.session_state.transactions
                    st.rerun()

            st.selectbox("Login as User", key="login_as_user", on_change=login_as_user(), options=basic_users, index=None, width=150, placeholder="Choose person", help="Switch entirely to a different user. To go back, just Refresh the browser and login again.")
    with col4:
        with st.container(horizontal=True):
            if st.button(":moneybag: Deposit", width=200, type="primary"):
                do_transaction(deposit=True)
            if st.button(":money_with_wings: Withdraw", width=200):
                do_transaction(deposit=False)