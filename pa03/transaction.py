'''
This program is written by Angela Lam and Dexin Huang

Transaction is an Object Relational Mapping to the transactions.db database

The ORM will work map SQL rows with the schema
    (rowid, amount, category, date, description)
to Python Dictionaries as follows:

(100, 'food', 2023-10-5, 'beef') <-->
{rowid:1, amount:100, category:'food', date:'2023-10-5', description:'beef'}

In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/transactions.db

'''
import sqlite3

def to_dict(tuples):
    '''
    Convert a tuple of transaction information into a dictionary.

    Args:
        tuples: A tuple containing transaction information in the order
                (rowid, amount, category, date, description)

    Returns:
        A dictionary containing the transaction information with keys
        'rowid', 'amount', 'category', 'date', and 'description'.

    Note:
        The input tuple can have less than 5 elements, and the returned
        dictionary will only have keys for the available elements.
    '''
    transaction = {}
    if len(tuples) >= 1:
        transaction['rowid'] = tuples[0]
    if len(tuples) >= 2:
        transaction['amount'] = tuples[1]
    if len(tuples) >= 3:
        transaction['category'] = tuples[2]
    if len(tuples) >= 4:
        transaction['date'] = tuples[3]
    if len(tuples) >= 5:
        transaction['description'] = tuples[4]
    return transaction


def tuples_to_dicts(t_s):
    '''
    Convert a list of transaction tuples to a list of dictionaries.

    Args:
        t_s: A list of tuples, where each tuple contains transaction information
             in the order (rowid, amount, category, date, description)

    Returns:
        A list of dictionaries, where each dictionary contains the transaction
        information with keys 'rowid', 'amount', 'category', 'date', and 'description'.

    Note:
        This function utilizes the to_dict() function for converting individual tuples.
    '''
    return [to_dict(tuples) for tuples in t_s]


class Transaction:
    '''Initialize the class and create the table if there has no such table'''
    def __init__(self, filename):
        self.filename = filename
        self.run_query('''CREATE TABLE IF NOT EXISTS transactions
                    (amount int, category text, date int, description text)''',())

    def show_transactions(self):
        ''' Show all the transactions '''
        return self.run_query("SELECT rowid, * FROM transactions",())

    def add_transaction(self, item):
        ''' Add a new transaction '''
        return self.run_query("INSERT INTO transactions VALUES(?,?,?,?)",
                              (item['amount'], item['category'], item['date'], item['description']))

    def delete_transaction(self, rowid):
        ''' Delete a transaction by item_no '''
        return self.run_query("DELETE FROM transactions WHERE rowid=?", (rowid,))
    #Angela
    def summarize_by_date(self):
        ''' Summarize transactions by date '''
        return self.run_query("SELECT date, SUM(amount) FROM transactions GROUP BY date",())
    #Angela
    def summarize_by_month(self):
        ''' Summarize transactions by month '''
        return self.run_query(
            "SELECT strftime('%m', date) AS month, SUM(amount) FROM transactions GROUP BY month",())
    #Angela
    def summarize_by_year(self):
        ''' Summarize transactions by year '''
        return self.run_query(
            "SELECT strftime('%Y', date) AS year, SUM(amount) FROM transactions GROUP BY year",())

    def summarize_by_category(self):
        ''' Summarize transactions by category '''
        return self.run_query(
            "SELECT category, SUM(amount) AS amount FROM transactions GROUP BY category",())

    def run_query(self, query, data):
        ''' Execute a SQL query and return the results '''
        # con = sqlite3.connect(os.getenv('HOME') + '/' + self.filename)
        con = sqlite3.connect(self.filename)
        cur = con.cursor()
        cur.execute(query,data)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return tuples_to_dicts(tuples)
