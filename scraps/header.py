import streamlit as st

import persist as db
import util

from scraps.dialog import do_transaction

def render():
    col1, col2, col3, col4 = st.columns(4, gap=None)
    with col1:
        st.write(f"## {st.session_state.user.emoji} {st.session_state.user.name} at :rainbow[Bank 139]")
        st.write("_Total change over the last 2 weeks_")
    with col2:
        st.metric("Balance", util.money(st.session_state.user.balance), f"{db.calc_balance_delta()}%")
    with col3:
        if not st.session_state.user.is_admin:
            if st.session_state.user.balance - (st.session_state.user.pending_balance * -1) < 0:
                st.metric("Pending", util.money(st.session_state.user.pending_balance, disable_color=True),
                          delta="In Debt", delta_color="red", delta_arrow="off")
            else:
                st.metric("Pending", util.money(st.session_state.user.pending_balance, disable_color=True))
    with col4:
        with st.container():
            if st.button(":moneybag: Deposit", width=200, type="primary"):
                do_transaction(deposit=True)
            if st.button(":money_with_wings: Withdraw", width=200):
                do_transaction(deposit=False)