import sys
from transactions import Transaction


def print_menu():
    """Print the menu of available commands."""
    menu = """
=======================================
           TRANSACTION MENU
  Type any of the following commands.

  1. show_categories
  2. add_category <category>
  3. modify_category <category> <modified category name>
  4. show_transactions
  5. add_transaction <category> <trans. amount> <date (YYYY-MM-DD)> <description>
  6. delete_transaction <transaction id>
  7. summarize_transactions_date
  8. summarize_transactions_month
  9. summarize_transactions_year
  10. summarize_transactions_category
  11. help
  12. reselect_file <file_path>
  13. quit

=======================================
"""
    print(menu)


def main():
    """Main function to handle user input and execute commands."""
    print("\nEnter your database filename. If the file does not exist, a new one will be created.")
    filename = input("filename >>> ")
    transaction = Transaction(filename)
    print_menu()

    commands = {
        "show_categories": transaction.get_categories,
        "add_category": transaction.add_category,
        "modify_category": transaction.modify_category,
        "show_transactions": transaction.get_transactions,
        "add_transaction": transaction.add_transaction,
        "delete_transaction": transaction.delete_transaction,
        "summarize_transactions_date": transaction.summarize_by_date,
        "summarize_transactions_month": transaction.summarize_by_month,
        "summarize_transactions_year": transaction.summarize_by_year,
        "summarize_transactions_category": transaction.summarize_by_category,
    }

    while True:
        command_input = input(">>> ")
        if command_input.strip() == "help":
            print_menu()
        elif command_input.strip() == "quit":
            break
        else:
            command_parts = command_input.split(" ")
            command = command_parts[0]
            args = command_parts[1:]

            if command in commands:
                try:
                    result = commands[command](*args)
                    if result is not None:
                        print(result)
                except TypeError:
                    print(f"Invalid number of arguments for command '{command}'. Type 'help' for usage information.")
            else:
                print("Unknown command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    main()
