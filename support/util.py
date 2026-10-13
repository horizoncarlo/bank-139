import urllib.request
from datetime import datetime

import streamlit as st

DEBUG = st.secrets.get("is_dev", True)
DB_NAME = st.secrets.get("db_name", "bank.db")
RECENT_TRANSACTION_LIMIT = st.secrets.get("recent_transaction_limit", 50)
DEFAULT_DATE_FORMAT = "hh:mma, YYYY-MM-DD"
TIMEZONE = st.secrets.get("timezone", "America/Edmonton")
NTFY_TOPIC = st.secrets.get("ntfy_topic")
NTFY_RETURN_URL = st.secrets.get("ntfy_return_url")
POSITIVE_MESSAGES = st.secrets.get(
    "positive_messages",
    [
        "Rad",
        "Nice",
        "Sweet",
        "Awesome",
        "Excellent",
        "Fantastic",
        "Brilliant",
        "Superb",
        "Stellar",
        "Amazing",
        "Wonderful",
        "Splendid",
        "Epic",
        "Thriving",
        "Winning",
        "Flourishing",
        "Prosperous",
        "Booming",
        "Mint",
        "Legendary",
    ],
)
NEGATIVE_MESSAGES = st.secrets.get(
    "negative_messages",
    [
        "Bummer",
        "Whoops",
        "Yikes",
        "Oops",
        "Darn",
        "Drat",
        "Oof",
        "Eek",
        "Rough",
        "Meh",
        "Ouch",
        "Yowch",
        "Bleak",
        "Trouble",
        "Struggling",
        "Wobbly",
        "Dire",
        "Unlucky",
        "Uh-oh",
        "Yikes",
    ],
)


def log(message: str):
    print(f"{datetime.now()}: {message}")


def money(value_in_cents: int, disable_color: bool = False):
    as_money = f"${value_in_cents/100:.2f}"
    if not disable_color:
        color = "green" if value_in_cents >= 0 else "red"
        return f":{color}[{as_money}]"
    return as_money


def get_default_users():
    return [
        (
            username,
            password,
            emoji,
            name,
            message,
            int(balance),
            int(is_admin == "True"),
        )
        for username, password, emoji, name, message, balance, is_admin in st.secrets.get(
            "default_users", []
        )
    ]


def get_allowances():
    return [
        (username, int(amount)) for username, amount in st.secrets.get("allowances", [])
    ]


def send_phone_notification(username, is_deposit: bool, amount_as_cents, description):
    if not NTFY_TOPIC:
        return

    url = f"https://ntfy.sh/{NTFY_TOPIC}"

    message = f"{username.capitalize()} {'Deposited' if is_deposit else 'Withdrew'} {money(amount_as_cents, disable_color=True)}: {description}"
    data = message.encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")

    req.add_header("Title", f"Bank 139 - {username.capitalize()}")
    req.add_header("Tags", "bank")
    if NTFY_RETURN_URL:
        req.add_header("Actions", f"view, Open App, {NTFY_RETURN_URL}")

    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode() == 200
    except Exception as e:
        log(f"Error sending alert phone notification: {e}")
