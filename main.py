import os
from unittest import case

import ExpenseTrackerLogic as ExpenseTracker

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def menu():

    print("[ Expense Tracker ]")
    print("\n[ MENU OPTIONS ]")
    print("  1. Add New Expense")
    print("  2. Set a New Budget")
    print ("  3. Load Budget")
    print("  4. View Summary & Budget Progress")
    print("  5. Generate & Print Statement Report")
    print("  6. Exit")

def main():
    menu()
    while True:


        expenses = ExpenseTracker.load_expenses()
        budgetLoader = ExpenseTracker.load_budgets()

        if not expenses:
            print("\nNo expenses yet.")
        for e in expenses:
            print("Expenses \n",f"{e['timestamp']} | {e['name']} | {e['category']} | {e['amount']}")

        if not budgetLoader:
            print("\nNo budgets yet.")
        for BL in budgetLoader:
            print(f"Budget: {BL['name']} | {BL['target_amount']} | {BL['monthly_amount']}")

        try:
            choice = int(input("\nPlease select an option: "))
        except ValueError:
            print("\nPlease enter a number from the menu.")
            continue

        match choice:

            case 1:
                clear_screen()
                name = input("Name of the expense: ")
                category = input("Category of the expense: ")

                try:
                    amount = float(input("Amount of the expense: "))
                    ExpenseTracker.create_expense(name, category, amount)
                    print("\nExpense created.")
                except ValueError as error:
                    print(f"\nCould not create expense: {error}")

            case 2 :
                clear_screen()
                budgetname = input("Name of the budget: ")
                budgetamount = float(input("Amount of the budget: "))
                budgetaddamount = float(input("How much will you add per month: "))
                ExpenseTracker.SetBudget(budgetname,budgetamount,budgetaddamount)

            case 3:
                os.system("cls" if os.name == "nt" else "clear")
                budgetLoader = ExpenseTracker.load_budgets()

                budnum = int(input("what budget you want to deposit in: "))
                budam = int(input("How much do you want to deposit : "))

                ExpenseTracker.AddToBudget(budnum, budam)

                if not budgetLoader:
                    print("\nNo budgets yet.")
                for BL in budgetLoader:
                    print(f"Budget: {BL['name']} | {BL['target_amount']} | {BL['monthly_amount']}")
            case 4:
                clear_screen()
                summary = ExpenseTracker.Load_Summary()

                print("[ Expenses Summary ]")
                print(f"Expenses recorded: {summary['expense_count']}")
                print(f"Total spent: {summary['total_spent']:.2f}")

                for category, total in summary["by_category"].items():
                    print(f"  {category}: {total:.2f}")

                print("\n[ Budget Progress ]")
                if not summary["budgets"]:
                    print("No budgets yet.")
                for budget in summary["budgets"]:
                    print(f"{budget['name']}: {budget['saved']:.2f} / {budget['target']:.2f} "
                          f"({budget['percent']:.0f}%) | {budget['months_left']} months left")

            case 5:
                clear_screen()
                path = ExpenseTracker.StatementReport()
                print(f"\nReport saved to: {path}")
            case _:
                print("\nInvalid option, please choose 1 to 6.")


if __name__ == "__main__":
    main()