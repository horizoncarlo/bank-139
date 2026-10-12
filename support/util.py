import streamlit as st

DEBUG = st.secrets.get("is_dev", True)
DB_NAME = st.secrets.get("db_name", "bank.db")
RECENT_TRANSACTION_LIMIT = st.secrets.get("recent_transaction_limit", 50)
DEFAULT_DATE_FORMAT = "hh:mma, YYYY-MM-DD"
TIMEZONE = st.secrets.get("timezone", "America/Edmonton")
POSITIVE_MESSAGES = st.secrets.get("positive_messages", [
    "Rad", "Nice", "Sweet", "Awesome", "Excellent",
    "Fantastic", "Brilliant", "Superb", "Stellar", "Amazing",
    "Wonderful", "Splendid", "Epic", "Thriving", "Winning",
    "Flourishing", "Prosperous", "Booming", "Mint", "Legendary"
])
NEGATIVE_MESSAGES = st.secrets.get("negative_messages", [
    "Bummer", "Whoops", "Yikes", "Oops", "Darn",
    "Drat", "Oof", "Eek", "Rough", "Meh",
    "Ouch", "Yowch", "Bleak", "Trouble", "Struggling",
    "Wobbly", "Dire", "Unlucky", "Uh-oh", "Yikes"
])

def money(value_in_cents: int, disable_color: bool = False):
    as_money = f"${value_in_cents/100:.2f}"
    if not disable_color:
        color = "green" if value_in_cents >= 0 else "red"
        return f":{color}[{as_money}]"
    return as_money

def get_default_users():
    return [
        (username, password, emoji, name, message, int(balance), int(is_admin == "True"))
        for username, password, emoji, name, message, balance, is_admin
        in st.secrets.get("default_users", [])
    ]