# Bank 139
## "Real World Money. Virtually"
Financial app for users to deposit or withdraw arbitrary sums of money against a balance. Admins need to approve any transaction.

This was designed for family use, where kids can see their balance and mark when they spend real-world money on something. Saves having a bunch of cash on-hand.

Also has a built in automatic Allowance depositing feature.

### Tech Stack
Built with [Streamlit](https://streamlit.io/) in pure Python as I wanted to try something new and depart from my usual client-side work. SQLite is used as a simple backing db.

All of the custom app configuration is done through `.streamlit/secrets.toml` via util.py, which has these options:
```
is_dev = false                  # If true, will automatically login as first viable admin. Turns on debugging options like switching to a user, deleting the db, etc.
db_name = bank.db               # Default SQLite database filename
recent_transaction_limit = 50   # How many transactions to get by default. There is an option to get ALL transactions via the UI as well
timezone = America/Edmonton     # Timestamps are Unix epoch, this timezone is used for converting for visual display
positive_messages = ["Rad", "Nice"]     # Random motivational message shown every render below a positive account balance
negative_messages = ["Whoops", "Poor"]  # Same as positive, but for negative account balances
default_users = [                       # List of users to insert into the database when the app starts. Order is [username, password (unhashed), emoji, name, slogan, balance, is_admin]
    ["carlo", "git", ":man_technologist:", "Carlo", "Keep on keepin' on", "0", "True"],
]
allowances = [                  # Automatic approved deposits every Sunday, format is [username, dollar amount], for example this kid is getting $5 a week
    ["kid", "5"],
]
ntfy_topic = "optional"         # Optional ntfy.sh Topic to alert Admins when a new transaction needs approval. Subscribe to this same channel on your phone
ntfy_return_url =               # Live app URL to include as a return URL in any ntfy.sh notification
```

Also look at `.streamlit/config.toml` for Streamlit specific configuration settings.

### Setup
```
python -m venv .venv
pip install -r requirements
bash go.sh OR python -m streamlit run main.py
```

Then visit http://localhost:8501/ (default Streamlit port) and start having fun!
