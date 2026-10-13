query_strings = {
    "create_user_table": """CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        emoji TEXT DEFAULT ":zany:",
        name TEXT NOT NULL,
        message TEXT,
        balance INTEGER NOT NULL DEFAULT 0,
        is_admin INTEGER NOT NULL DEFAULT 0
        )""",
    "create_transaction_table": """CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        amount INTEGER NOT NULL DEFAULT 0,
        description TEXT NOT NULL,
        location TEXT,
        is_approved INTEGER DEFAULT 0,
        reviewed_by TEXT,
        reviewed_at INTEGER,
        created_at INTEGER NOT NULL DEFAULT (unixepoch())
        )""",
    "create_allowance_table": """
        CREATE TABLE IF NOT EXISTS allowances (
            sunday_date TEXT PRIMARY KEY,
            run_timestamp TEXT NOT NULL
        )
    """,
    "drop_user_table": "DROP TABLE IF EXISTS users",
    "drop_transaction_table": "DROP TABLE IF EXISTS transactions",
    "drop_allowance_table": "DROP TABLE IF EXISTS allowances",
    "insert_default_users": f"""INSERT OR IGNORE INTO users (username, password, emoji, name, message, balance, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?)""",
    "do_login": "SELECT * FROM users WHERE username = ? AND password = ?",
    "select_recent_transactions": """
        SELECT
            t.transaction_id,
            t.amount,
            t.description,
            t.location,
            t.created_at,
            CASE
                WHEN NULLIF(TRIM(t.reviewed_by), '') IS NULL THEN 'Waiting'
                WHEN t.is_approved THEN 'Yes'
                ELSE 'No'
            END AS is_approved,
            u.name AS reviewed_by,
            t.reviewed_at
        FROM transactions t
        LEFT JOIN users u ON u.username = t.reviewed_by
        WHERE t.owner = ?
        ORDER BY t.created_at DESC LIMIT ?
    """,
    "select_pending_total": """
        SELECT COALESCE(SUM(amount), 0) AS pending_amount
        FROM transactions
        WHERE owner = ?
          AND reviewed_by IS NULL
    """,
    "select_waiting_transactions": """
        SELECT t.transaction_id, u.name, t.amount, t.description, t.location, u.balance, t.reviewed_by
        FROM transactions t
        JOIN users u ON u.username = t.owner
        WHERE t.owner != ?
          AND t.reviewed_by IS NULL
    """,
    "select_transaction": "SELECT owner, amount FROM transactions WHERE transaction_id = ?",
    "update_transaction_approval": "UPDATE transactions SET is_approved = ?, reviewed_by = ?, reviewed_at = ? WHERE transaction_id = ?",
    "insert_new_transaction": "INSERT INTO transactions (owner, amount, description, location, is_approved, reviewed_by, reviewed_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    "delete_transaction": "DELETE FROM transactions WHERE transaction_id = ? AND owner = ?",
    "update_balance": "UPDATE users SET balance = balance + ? WHERE username = ?",
    "select_user": "SELECT * FROM users WHERE username = ?",
    "update_user": "UPDATE users SET emoji = ?, name = ?, message = ?, password = ? WHERE username = ?",
    "select_normal_users": "SELECT username, balance FROM users WHERE is_admin = FALSE",
    "select_all_users": "SELECT * FROM users WHERE is_admin = ?",
    "select_latest_sunday": "SELECT MAX(sunday_date) FROM allowances",
    "insert_new_allowance": "INSERT INTO allowances (sunday_date, run_timestamp) VALUES (?, ?)",
}
