query_strings = {
    "create_user_table": """CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        emoji TEXT DEFAULT ":zany:",
        name TEXT NOT NULL,
        balance INTEGER NOT NULL DEFAULT 0,
        is_admin INTEGER NOT NULL DEFAULT 0
        )""",
    "create_transaction_table": """CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY,
        owner_id TEXT NOT NULL,
        amount INTEGER NOT NULL DEFAULT 0,
        description TEXT NOT NULL,
        location TEXT,
        is_approved INTEGER DEFAULT 0,
        approved_by TEXT,
        approved_at INTEGER,
        created_at INTEGER NOT NULL DEFAULT (unixepoch())
        )""",
    "drop_user_table": "DROP TABLE IF EXISTS users",
    "drop_transaction_table": "DROP TABLE IF EXISTS transactions",
    "insert_default_users": f"""INSERT OR IGNORE INTO users (username, password, emoji, name, balance, is_admin) VALUES (?, ?, ?, ?, ?, ?)"""
}