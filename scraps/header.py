import random

import streamlit as st

from scraps.dialogs.operation import dialog_do_transaction
from scraps.dialogs.profile import dialog_edit_profile
from support import persist as db
from support import util


def render():
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1], gap=None)
    with col1:
        st.write(
            f"## {st.session_state.user.emoji} {st.session_state.user.name} at :rainbow[Bank 139]"
        )
        with st.container(horizontal=True, vertical_alignment="center"):
            if st.button("", icon=":material/person_edit:", type="tertiary"):
                dialog_edit_profile()
            st.markdown(st.session_state.user.message)
            if st.button("", icon=":material/logout:", type="tertiary"):
                st.session_state.clear()
                st.rerun()
    with col2:
        st.metric(
            "Balance",
            util.money(st.session_state.user.balance),
            delta=(
                random.choice(util.POSITIVE_MESSAGES)
                if st.session_state.user.balance >= 0
                else random.choice(util.NEGATIVE_MESSAGES)
            ),
            delta_arrow="off",
            delta_color="blue",
        )
    with col3:
        if not st.session_state.user.is_admin:
            if (
                st.session_state.user.balance
                - (st.session_state.user.pending_balance * -1)
                < 0
            ):
                st.metric(
                    "Pending",
                    util.money(
                        st.session_state.user.pending_balance, disable_color=True
                    ),
                    delta="In Debt",
                    delta_color="red",
                    delta_arrow="off",
                )
            else:
                st.metric(
                    "Pending",
                    util.money(
                        st.session_state.user.pending_balance, disable_color=True
                    ),
                )
        else:
            basic_users = db.get_all_non_admin_users()

            def login_as_user():
                if (
                    "login_as_user" in st.session_state
                    and st.session_state.login_as_user
                ):
                    st.session_state.user = db.get_user_by_username(
                        st.session_state.login_as_user
                    )
                    del st.session_state.transactions
                    st.rerun()

            st.selectbox(
                "Login as User",
                key="login_as_user",
                on_change=login_as_user(),
                options=[user[0] for user in basic_users],
                format_func=lambda username: next(
                    f"{u} ({util.money(balance, disable_color=True)})"
                    for u, balance in basic_users
                    if u == username
                ),
                index=None,
                width=150,
                placeholder="Choose person",
                help="Switch entirely to a different user. To go back, just Refresh the browser and login again.",
            )
    with col4:
        with st.container(horizontal=True):
            if st.button(":moneybag: Deposit", width=200, type="primary"):
                dialog_do_transaction(deposit=True)
            if st.button(":money_with_wings: Withdraw", width=200):
                dialog_do_transaction(deposit=False)
