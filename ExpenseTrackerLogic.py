import datetime as dt
import json
import math
from pathlib import Path

DATA_FILE_EX = Path("expenses.json")
DATA_FILE_BD = Path("budgets.json")
DATA_FILE_SM = Path("summary.json")

BASE_DIR = Path(__file__).parent
REPORTS_DIR =BASE_DIR /"reports"

def create_expense(name, category, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    ExpensesTemplate = {
        "name": name,
        "category": category,
        "amount": amount,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
    }

    if DATA_FILE_EX.exists():
        expenses = json.loads(DATA_FILE_EX.read_text(encoding="utf-8"))
    else:
        expenses = []

    expenses.append(ExpensesTemplate)

    DATA_FILE_EX.write_text(json.dumps(expenses, indent=4), encoding="utf-8")

    print("Expense created.")
    return ExpensesTemplate

def load_expenses():
    if not DATA_FILE_EX.exists():
        return []
    return json.loads(DATA_FILE_EX.read_text(encoding="utf-8"))

def SetBudget(name, target_amount, monthly_amount):
    if not name.strip():
        raise ValueError("Name cannot be empty.")
    if target_amount <= 0 or monthly_amount <= 0:
        raise ValueError("Amounts must be greater than zero.")
    if monthly_amount > target_amount:
        raise ValueError("Monthly amount cannot be bigger than the target.")

    budget = {
        "name": name.strip(),
        "target_amount": target_amount,
        "monthly_amount": monthly_amount,
        "created": dt.datetime.now().isoformat(timespec="seconds"),
    }

    budgets = load_budgets()
    budgets.append(budget)
    DATA_FILE_BD.write_text(json.dumps(budgets, indent=4), encoding="utf-8")
    return budget

def load_budgets():
    if not DATA_FILE_BD.exists():
        return []
    return json.loads(DATA_FILE_BD.read_text(encoding="utf-8"))

def Load_Summary():
    expenses = load_expenses()
    budgets = load_budgets()

    total_spent = sum(expense["amount"] for expense in expenses)

    by_category = {}
    for expense in expenses:
        category = expense["category"]
        by_category[category] = by_category.get(category, 0) + expense["amount"]


    now = dt.datetime.now()
    budget_progress = []
    for budget in budgets:
        saved = budget.get("saved", 0)
        remaining = budget["target_amount"] - saved

        budget_progress.append({
            "name": budget["name"],
            "target": budget["target_amount"],
            "monthly": budget["monthly_amount"],
            "saved": saved,
            "remaining": remaining,
            "percent": saved / budget["target_amount"] * 100,
            "months_left": math.ceil(remaining / budget["monthly_amount"]),
        })

    return {
        "expense_count": len(expenses),
        "total_spent": total_spent,
        "by_category": by_category,
        "budgets": budget_progress,
    }

def StatementReport():
    summary = Load_Summary()
    expenses = load_expenses()

    now = dt.datetime.now()
    REPORTS_DIR.mkdir(exist_ok=True)
    file_path = REPORTS_DIR / f"statement_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    line = "=" * 50
    thin = "-" * 50

    lines = [
        line,
        "EXPENSE TRACKER STATEMENT".center(50),
        line,
        f"Generated on: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        thin,
        "SUMMARY",
        thin,
        f"Expenses recorded : {summary['expense_count']}",
        f"Total spent       : {summary['total_spent']:.2f}",
        "",
        "Spending by category:",
    ]

    if not summary["by_category"]:
        lines.append("  None")
    for category, total in summary["by_category"].items():
        lines.append(f"  {category:<15} : {total:.2f}")

    lines += ["", thin, "BUDGET PROGRESS", thin]

    if not summary["budgets"]:
        lines.append("No budgets yet.")
    for budget in summary["budgets"]:
        lines += [
            budget["name"],
            f"  Target          : {budget['target']:.2f}",
            f"  Saved so far    : {budget['saved']:.2f} ({budget['percent']:.0f}%)",
            f"  Months left     : {budget['months_left']}",
            "",
        ]

    lines += [thin, "ALL EXPENSES", thin]

    if not expenses:
        lines.append("No expenses yet.")
    for expense in expenses:
        when = expense["timestamp"].replace("T", " ")
        lines.append(
            f"{when} | {expense['name']:<15} | {expense['category']:<12} | {expense['amount']:.2f}"
        )

    lines += ["", line, "END OF STATEMENT".center(50), line]

    file_path.write_text("\n".join(lines), encoding="utf-8")
    return file_path

def AddToBudget(number, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    budgets = load_budgets()
    if not 1 <= number <= len(budgets):
        raise ValueError("No budget with that number.")

    budget = budgets[number - 1]
    saved = budget.get("saved", 0)
    remaining = budget["target_amount"] - saved

    if amount > remaining:
        raise ValueError(f"Only {remaining:.2f} left to reach the target.")

    budget["saved"] = saved + amount
    DATA_FILE_BD.write_text(json.dumps(budgets, indent=4), encoding="utf-8")
    return budget