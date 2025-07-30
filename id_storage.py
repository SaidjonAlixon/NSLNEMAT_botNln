import sqlite3

class IDStorage:
    def __init__(self, db_path="user_ids.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS user_ids (telegram_id INTEGER PRIMARY KEY, client_id TEXT)"
            )

    def set_client_id(self, telegram_id, client_id):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO user_ids (telegram_id, client_id) VALUES (?, ?)",
                (telegram_id, client_id)
            )

    def get_client_id(self, telegram_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT client_id FROM user_ids WHERE telegram_id = ?", (telegram_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None

    def delete_client_id(self, telegram_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM user_ids WHERE telegram_id = ?",
                (telegram_id,)
            )