"""
This program is written by Angela Lam and Dexin Huang

Tracker is an app that maintains a transactions database.

It also uses an Object Relational Mapping (ORM)
to abstract out the database operations from the
UI/UX code.

The ORM, Transaction, will map SQL rows with the schema
    (rowid, amount, category, date, description)
to Python Dictionaries as follows:

(100, 'food', 2023-10-5, 'beef') <-->
{rowid:1,
 amount:100,
 category:'food',
 date:'2023-10-5',
 description:'beef'
}

In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/transactions.db
"""
import sys
import datetime
from transaction import Transaction


def print_usage():
    ''' print the menu options '''
    print('''usage:
            0. quit
            1. show transactions
            2. add transaction
            3. delete transaction
            4. summarize transactions by date
            5. summarize transactions by month
            6. summarize transactions by year
            7. summarize transactions by category
            8. show menu
            '''
          )


def print_summary(header, transaction):
    '''
    Print a summary of transactions based on the provided header.

    Args:
        header (str): A formatted string representing the header of the summary table.
        transaction (list): A list of transaction dictionaries.

    Note:
        If the transaction list is empty, it will print 'no tasks to print'.
    '''
    if len(transaction) == 0:
        print('no tasks to print')
        return

    print('\n' + header)
    print('-' * len(header))

    for item in transaction:
        values = tuple(item.values())
        print(f"{values[0]:<18} {values[1]}")

# Angela
def print_transactions(transaction):
    '''
    Print a formatted table of transactions with headers and values.

    Args:
        transaction (list): A list of transaction dictionaries.

    Note:
        If the transaction list is empty, it will print 'no tasks to print'.
    '''
    if len(transaction) == 0:
        print('no tasks to print')
        return

    print('\n' + f"{'item #':<10} {'amount':<12} {'category':<15} {'date':<18} {'description'}")
    print('-' * 75)
    for item in transaction:
        values = tuple(item.values())
        print(f"{values[0]:<10} {values[1]:<12} {values[2]:<15} {values[3]:<18} {values[4]}")


def process_args(arglist):
    '''
    Process the command line arguments and execute the corresponding transaction operations.

    Args:
        arglist (list): A list of command line arguments.

    Note:
        Supported commands include: quit, show transactions, add, delete, summarize by date,
        summarize by month, summarize by year, summarize by category, and show menu.
        If an unsupported command is entered, it will print "is not implemented" and show the usage.
    '''
    transaction = Transaction("transactions.db")

    if not arglist:
        print_usage()
    elif 'quit' in arglist[0]:
        print('\n' + "You have been disconnected" + '\n')
        sys.exit()
    elif 'show transactions' in arglist[0]:
        print_transactions(transaction.show_transactions())
    elif 'add' in arglist[0]:
        amount = int(input('\n' + 'Enter amount: '))
        category = input('Enter category: ')
        date = datetime.datetime.strptime(input('Enter date (yyyy-mm-dd): '), '%Y-%m-%d')
        description = input('Enter description: ')
        info = {'amount': amount, 'category': category, 'date': date.date(),
                'description': description}
        transaction.add_transaction(info)
    elif 'delete' in arglist[0]:
        print_transactions(transaction.show_transactions())
        print('-' * 75 + '\n')
        num = input('Enter transaction id: ')
        print_transactions(transaction.delete_transaction(num))
    elif 'summarize by' in arglist[0]:
        if 'date' in arglist[0]:
            print_summary("date         amount", transaction.summarize_by_date())
        elif 'month' in arglist[0]:
            print_summary("month        amount", transaction.summarize_by_month())
        elif 'year' in arglist[0]:
            print_summary("year         amount", transaction.summarize_by_year())
        elif 'category' in arglist[0]:
            print_transactions(transaction.summarize_by_category())
    elif 'menu' in arglist[0]:
        print_usage()
    else:
        print(arglist, "is not implemented")
        print_usage()


def toplevel():
    '''
    Process command line arguments and execute corresponding transaction operations.

    Note:
        If no arguments are passed, the function will enter an interactive command prompt mode,
        continuously asking for user input until an empty input is received.
        In both cases, whether arguments are passed or not, the function will call process_args()
        to handle the entered commands and execute the corresponding operations.
    '''
    if len(sys.argv) == 1:
        # they didn't pass any arguments,
        # so prompt for them in a loop
        print('\n' + '-' * 40)
        print_usage()
        args = []
        while args != ['']:
            args = input("command> ").split(' ')
            curr = args[0]
            args = [' '.join(args[0:])]
            process_args(args)
            if curr == 'summarize':
                print('-' * 30 + '\n')
            elif args[0] == 'show transactions':
                print('-' * 75 + '\n')
            else:
                print('-' * 40 + '\n')
    else:
        # read the args and process them
        args = sys.argv[1:]
        process_args(args)
        print('-' * 40 + '\n' * 3)


if __name__ == '__main__':
    toplevel()
