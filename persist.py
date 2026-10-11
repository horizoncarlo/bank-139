import time
import sqlite3
from contextlib import closing, contextmanager
from dataclasses import dataclass

from queries import query_strings as queries
import util

@dataclass
class User:
    username: str
    password: str
    emoji: str # Emoji shortcode such as :smirk:
    name: str
    balance: int
    is_admin: bool = False
    pending_balance: int | None = None

@dataclass
class Transaction:
    # owner: str - is used in the table itself, but not in our returned results
    amount: int
    description: str
    location: str | None # Optional
    created_at: int  # Unix timestamp
    is_approved: str | None  # Actual table is boolean, but here we use Yes or No for readability
    reviewed_by: str | None = None
    reviewed_at: int | None = None # Unix timestamp

@contextmanager
def connection():
    with closing(sqlite3.connect(util.DB_NAME)) as conn:
        with conn:
            yield conn

def init():
    with connection() as conn:
        conn.execute(queries['create_user_table'])
        conn.execute(queries['create_transaction_table'])

        if util.DEBUG:
            default_users = util.get_default_users()
            if default_users:
                conn.executemany(queries['insert_default_users'], default_users)

def delete_all():
    with connection() as conn:
        conn.execute(queries['drop_user_table'])
        conn.execute(queries['drop_transaction_table'])

def login(username, password):
    with connection() as conn:
        res = conn.execute(queries['do_login'], (username, password)).fetchone()
        return User(*res) if res else None

def get_recent_transactions(username):
    with connection() as conn:
        res = conn.execute(queries['select_recent_transactions'], (username, util.RECENT_TRANSACTION_LIMIT))
        to_return = [
            Transaction(*row)
            for row in res.fetchall()
        ]
        print(f"TRANSACTIONS TO RETURN {to_return}")
        return to_return

def get_pending_total(username):
    with connection() as conn:
        return conn.execute(queries['select_pending_total'], (username,)).fetchone()[0]

def get_waiting_transactions(username):
    with connection() as conn:
        res = conn.execute("""
            SELECT t.transaction_id, u.name, t.amount, t.description, t.location, u.balance, t.reviewed_by
            FROM transactions t
            JOIN users u ON u.username = t.owner
            WHERE t.owner != ?
              AND t.reviewed_by IS NULL
        """, (username,)).fetchall()

        return [
            {
                "ID": row[0],
                "Owner": row[1],
                "Amount": util.money(row[2], disable_color=True),
                "Description": row[3],
                "Location": row[4],
                "Deny": "Deny",
                "Approve": "Approve",
                "Current Balance": util.money(row[5], disable_color=True)
            }
            for row in res
        ]

def review_transaction(transaction_id, is_approved, reviewer_username):
    with connection() as conn:
        row = conn.execute(
            "SELECT owner, amount FROM transactions WHERE transaction_id = ?",
            (transaction_id,)
        ).fetchone()

        if row is None:
            return False

        conn.execute("UPDATE transactions SET is_approved = ?, reviewed_by = ?, reviewed_at = ? WHERE transaction_id = ?",
                     (is_approved, reviewer_username, int(time.time()), transaction_id))

        # Only update the balance if we actually approve the transaction
        if is_approved:
            owner, amount = row
            conn.execute(
                "UPDATE users SET balance = balance + ? WHERE username = ?",
                (amount, owner)
            )

def create_transaction(username, amount_as_cents, description, location, is_admin):
    with connection() as conn:
        reviewed_by = username if is_admin else None
        reviewed_at = int(time.time()) if is_admin else None
        conn.execute("INSERT INTO transactions (owner, amount, description, location, is_approved, reviewed_by, reviewed_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (username, amount_as_cents, description, location, is_admin, reviewed_by, reviewed_at, int(time.time())))

        if is_admin:
            conn.execute(
                "UPDATE users SET balance = balance + ? WHERE username = ?",
                (amount_as_cents, username)
            )

def get_first_user(): # For debugging
    with connection() as conn:
        res = conn.execute("SELECT * FROM users WHERE is_admin = ?", (False,)).fetchone()
        return User(*res) if res else None

def get_first_admin_user(): # For debugging
    with connection() as conn:
        res = conn.execute("SELECT * FROM users WHERE is_admin = ?", (True,)).fetchone()
        return User(*res) if res else None

def calc_balance_delta():
    return 5 # TODO Determine our balance delta from the most recent 2 weeks