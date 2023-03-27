import sqlite3
import pytest
import datetime
from transaction import Transaction, to_dict, tuples_to_dicts

@pytest.fixture
def tuples():
    " create some tuples to put in the database "
    return [
        (10, "category0", datetime.date(2023, 1, 1).strftime('%Y-%m-%d'), "test0"),
        (10, "category1", datetime.date(2023, 1, 2).strftime('%Y-%m-%d'), "test1")
    ]

@pytest.fixture
def returned_tuples(tuples):
    " add a rowid to the beginning of each tuple "
    return [(i+1,)+tuples[i] for i in range(len(tuples))]

@pytest.fixture
def returned_dicts(tuples):
    " add a rowid to the beginning of each tuple "
    return tuples_to_dicts([(i+1,)+tuples[i] for i in range(len(tuples))])

@pytest.fixture
def transactions_path(tmp_path):
    return tmp_path / 'transactions.db'

@pytest.fixture(autouse=True)
def transactions(transactions_path,tuples):
    "create and initialize the transactions.db database in /tmp "
    con = sqlite3.connect(transactions_path)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (amount int, category text, date date, description text)''')
    cur = con.cursor()
    for i in range(len(tuples)):
        cur.execute('''insert into transactions values(?,?,?,?)''',tuples[i])
    con.commit()
    t = Transaction(transactions_path)
    yield t
    cur.execute('''drop table transactions''')
    con.commit()

def test_show_transactions(transactions, returned_dicts):
    # Test that show_transactions returns a list of dictionaries that match the expected data
    result = transactions.show_transactions()
    assert result == returned_dicts

def test_add_transaction(transactions, returned_dicts):
    # Test that add_transaction successfully adds a new transaction to the database
    new_transaction = (len(returned_dicts) + 1, 100, 'food', datetime.date(2023, 10, 5).strftime('%Y-%m-%d'), 'beef')
    transactions.add_transaction(to_dict(new_transaction))
    result = transactions.show_transactions()
    assert result[-1] == to_dict(new_transaction)

def test_delete_transaction(transactions, returned_dicts):
    # Test that delete_transaction successfully removes a transaction from the database
    transactions.delete_transaction(1)
    result = transactions.show_transactions()
    expected = returned_dicts[1:]
    assert result == expected

def test_summarize_by_date(transactions):
    # Test that summarize_by_date returns a list of dictionaries with the expected data
    expected = ('2023-01-02', 10)
    result = transactions.summarize_by_date()
    assert result[-1] == to_dict(expected)

def test_summarize_by_month(transactions):
    # Test that summarize_by_month returns a list of dictionaries with the expected data
    expected = ('01', 20)
    result = transactions.summarize_by_month()
    assert result[-1] == to_dict(expected)

def test_summarize_by_year(transactions):
    # Test that summarize_by_year returns a list of dictionaries with the expected data
    expected = ('2023', 20)
    result = transactions.summarize_by_year()
    assert result[-1] == to_dict(expected)

def test_summarize_by_category(transactions, returned_dicts):
    # Test that summarize_by_category returns a list of dictionaries with the expected data
    expected = ('category1', 10)
    result = transactions.summarize_by_category()
    assert result[-1] == to_dict(expected)
