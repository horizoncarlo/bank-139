import streamlit as st

DEBUG = st.secrets.get("is_dev", True)
DB_NAME = st.secrets.get("db_name", "bank.db")
RECENT_TRANSACTION_LIMIT = st.secrets.get("recent_transaction_limit", 50)
DEFAULT_DATE_FORMAT = "hh:mm:ss a, YYYY-MM-DD"
TIMEZONE = st.secrets.get("timezone", "America/Edmonton")

def money(value_in_cents: int, disable_color: bool = False):
    as_money = f"${value_in_cents/100:.2f}"
    if not disable_color:
        color = "green" if value_in_cents >= 0 else "red"
        return f":{color}[{as_money}]"
    return as_money

def get_default_users():
    return [
        (username, password, emoji, name, int(balance), int(is_admin == "True"))
        for username, password, emoji, name, balance, is_admin
        in st.secrets.get("default_users", [])
    ]