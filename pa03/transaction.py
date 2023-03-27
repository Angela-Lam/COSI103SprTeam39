"""
Transaction module for managing transactions
"""
import sqlite3

class Transaction:
    """
    Transaction class for handling transaction operations.
    """

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        description TEXT,
                        category TEXT,
                        amount REAL
                        )""")
        self.conn.commit()

    def add_transaction(self, amount, category, date, description):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (amount, category, date, description) VALUES (?, ?, ?, ?)", (
                amount, category, date, description))
        self.conn.commit()

    def delete_transaction(self, transaction_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        self.conn.commit()

    def update_transaction(self, transaction_id,
                           amount=None, category=None, date=None, description=None):
        cursor = self.conn.cursor()
        updates = {}
        if amount:
            updates['amount'] = amount
        if category:
            updates['category'] = category
        if date:
            updates['date'] = date
        if description:
            updates['description'] = description
        query = "UPDATE transactions SET " + ", ".join(
            f"{key}=?" for key in updates.keys()) + " WHERE id=?"
        params = tuple(updates.values()) + (transaction_id,)
        cursor.execute(query, params)
        self.conn.commit()

    def get_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()

    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM transactions")
        return [row[0] for row in cursor.fetchall()]

    def summarize_by_date(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT date, SUM(amount) FROM transactions GROUP BY date")
        return cursor.fetchall()

    def summarize_by_month(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM transactions GROUP BY month")
        return cursor.fetchall()

    def summarize_by_year(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT strftime('%Y', date) AS year, SUM(amount) FROM transactions GROUP BY year")
        return cursor.fetchall()

    def summarize_by_category(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category, SUM(amount) FROM transactions GROUP BY category")
        return cursor.fetchall()

    def add_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (category) VALUES (?)", (
                category,))
        self.conn.commit()

    def modify_category(self, old_category, new_category):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE transactions SET category=? WHERE category=?", (
            new_category, old_category))
        self.conn.commit()
