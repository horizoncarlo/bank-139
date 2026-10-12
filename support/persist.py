import sqlite3
import time
from contextlib import closing, contextmanager
from dataclasses import dataclass

import streamlit as st

from support import util
from support.queries import query_strings as queries


@dataclass
class User:
    username: str
    password: str
    emoji: str  # Emoji shortcode such as :smirk:
    name: str
    message: str  # Message below their name on home
    balance: int
    is_admin: bool = False
    pending_balance: int | None = None


@dataclass
class Transaction:
    transaction_id: int
    amount: int
    description: str
    location: str | None  # Optional
    created_at: int  # Unix timestamp
    is_approved: (
        str | None
    )  # Actual table is boolean, but here we use Yes or No for readability
    reviewed_by: str | None = None
    reviewed_at: int | None = None  # Unix timestamp


@contextmanager
def connection():
    with closing(sqlite3.connect(util.DB_NAME)) as conn:
        with conn:
            yield conn


def init():
    with connection() as conn:
        conn.execute(queries["create_user_table"])
        conn.execute(queries["create_transaction_table"])
        conn.execute(queries["create_allowance_table"])

        if util.DEBUG:
            default_users = util.get_default_users()
            if default_users:
                conn.executemany(queries["insert_default_users"], default_users)


def deposit_weekly_allowance(db_conn, sunday_date):
    for username, amount in util.get_allowances():
        create_transaction(
            username,
            amount_as_cents=amount * 100,
            description="Weekly allowance",
            location="Home",
            is_admin=True,
            conn_override=db_conn,
        )
        print(f"Deposit allowance for {username} for {sunday_date}")


def delete_all_tables():
    with connection() as conn:
        conn.execute(queries["drop_user_table"])
        conn.execute(queries["drop_transaction_table"])
        conn.execute(queries["drop_allowance_table"])


def login(username, password):
    with connection() as conn:
        res = conn.execute(queries["do_login"], (username, password)).fetchone()
        return User(*res) if res else None


def get_recent_transactions(username, fetch_all_instead=False):
    with connection() as conn:
        res = conn.execute(
            queries["select_recent_transactions"],
            (username, util.RECENT_TRANSACTION_LIMIT if not fetch_all_instead else -1),
        ).fetchall()
        return [Transaction(*row) for row in res]


def get_pending_total(username):
    with connection() as conn:
        return conn.execute(queries["select_pending_total"], (username,)).fetchone()[0]


def get_waiting_transactions(username):
    with connection() as conn:
        res = conn.execute(
            queries["select_waiting_transactions"], (username,)
        ).fetchall()

        return [
            {
                "ID": row[0],
                "Owner": row[1],
                "Amount": util.money(row[2], disable_color=True),
                "Description": row[3],
                "Location": row[4],
                "Deny": "Deny",
                "Approve": "Approve",
                "Current Balance": util.money(row[5], disable_color=True),
            }
            for row in res
        ]


def review_transaction(transaction_id, is_approved, reviewer_username):
    with connection() as conn:
        row = conn.execute(queries["select_transaction"], (transaction_id,)).fetchone()

        if row is None:
            return False

        conn.execute(
            queries["update_transaction_approval"],
            (is_approved, reviewer_username, int(time.time()), transaction_id),
        )

        # Only update the balance if we actually approve the transaction
        if is_approved:
            owner, amount = row
            conn.execute(queries["update_balance"], (amount, owner))


def create_transaction(
    username,
    amount_as_cents,
    description,
    location,
    is_admin,
    conn_override=None,
    for_username=None,
):
    conn = conn_override or connection()
    with conn:
        owner = for_username if for_username else username
        reviewed_by = username if is_admin else None
        reviewed_at = int(time.time()) if is_admin else None
        conn.execute(
            queries["insert_new_transaction"],
            (
                owner,
                amount_as_cents,
                description,
                location,
                is_admin,
                reviewed_by,
                reviewed_at,
                int(time.time()),
            ),
        )

        if is_admin:
            conn.execute(queries["update_balance"], (amount_as_cents, owner))


def delete_pending_transaction(transaction: Transaction, username):
    with connection() as conn:
        conn.execute(
            queries["delete_transaction"], (transaction.transaction_id, username)
        )


@st.cache_data()  # This list can safely be application wide
def get_all_non_admin_users():
    with connection() as conn:
        return [
            row[0] for row in conn.execute(queries["select_all_usernames"]).fetchall()
        ]


def get_user_by_username(username):
    with connection() as conn:
        res = conn.execute(queries["select_user"], (username,)).fetchone()
        return User(*res) if res else None


def update_user(user: User):
    with connection() as conn:
        conn.execute(
            queries["update_user"],
            (user.emoji, user.name, user.message, user.password, user.username),
        )


def get_first_user():
    """
    For debugging purposes, get the first normal user to login in as automatically in Dev mode
    """
    with connection() as conn:
        res = conn.execute(queries["select_all_users"], (False,)).fetchone()
        return User(*res) if res else None


def get_first_admin_user():
    """
    For debugging purposes, get the first Admin user to login in as automatically in Dev mode
    """
    with connection() as conn:
        res = conn.execute(queries["select_all_users"], (True,)).fetchone()
        return User(*res) if res else None
