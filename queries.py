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
        owner TEXT NOT NULL,
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
    "insert_default_users": f"""INSERT OR IGNORE INTO users (username, password, emoji, name, balance, is_admin) VALUES (?, ?, ?, ?, ?, ?)""",
    "do_login": "SELECT * FROM users WHERE username = ? AND password = ?",
    "select_recent_transactions": """
        SELECT
            t.amount / 100.0 AS amount,
            t.description,
            t.location,
            CASE WHEN t.is_approved THEN 'Yes' ELSE 'No' END AS is_approved,
            u.name AS approved_by,
            t.approved_at,
            t.created_at
        FROM transactions t
        LEFT JOIN users u ON u.username = t.approved_by
        WHERE t.owner = ?
    """
}