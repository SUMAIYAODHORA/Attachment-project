import datetime
import calendar

# The constructor method (__init__) is responsible for initializing the attributes of an expense object when it is created.


class Expense:
    def __init__(self, name, category, amount, date) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date
# The __repr__ method is used to define how an expense object should be represented as a string when it is printed or converted to a string.

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f}, Date: {self.date}>"


def get_user_expense():
    print(f" Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_date = input("Enter the date of the expense (DD/MM/YYYY): ")

    # Check if the date format is valid
    try:
        # Convert the input date format "DD/MM/YYYY" to "YYYY-MM-DD"
        expense_date = datetime.datetime.strptime(
            expense_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return get_user_expense()
# dictionary expense_categories is defined to map category numbers (as strings) to their corresponding category names.
    expense_categories = {
        "1": "Food",
        "2": "Home",
        "3": "Work",
        "4": "Fun",
        "5": "Transport",
        "6": "Medical",
        "7": "Misc",
    }
    print("Select a category: ")
    for key, category_name in expense_categories.items():
        print(f"{key}. {category_name}")

    selected_index = input("Enter a category number: ")
# If a valid category is selected, a new Expense object is created with the provided name, category, amount, and date. This object is returned as the result of the get_user_expense() function.
    if selected_index in expense_categories:
        selected_category = expense_categories[selected_index]

        new_expense = Expense(
            name=expense_name, category=selected_category, amount=expense_amount, date=expense_date
        )
        return new_expense
    else:
        print("Invalid category number. Please try again!")
        return get_user_expense()


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f" Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(
            f"{expense.date},{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print(f" Summarizing User Expense")
    # Here, an empty list called expenses is created. This list will be used to store Expense objects after reading them from the file.
    expenses: list[Expense] = []

    # Display the list of expenses with details
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # Split the line into four values (date, name, amount, category)
            expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")

            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
                date=expense_date
            )
            expenses.append(line_expense)

    if not expenses:
        print("No recorded expenses.")
        return

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category :")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f" Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f" Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f" Budget Per Day: ${daily_budget:.2f}"))


def list_expenses(expense_file_path):
    print(f" Listing All Recorded Expenses:")
    expenses: list[Expense] = []

    # Display the list of expenses with details
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # Split the line into four values (date, name, amount, category)
            parts = line.strip().split(",")
            if len(parts) != 4:
                print(
                    f"Records: {index + 1} - Invalid number of values: {line}")
                continue

            expense_date, expense_name, expense_amount, expense_category = parts

            # Convert the date string to a datetime object using the format "dd/mm/yyyy"
            try:
                expense_date = datetime.datetime.strptime(
                    expense_date, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                print(
                    f"Records: {index + 1}  {line}")
                continue  # Skip this line and continue with the next one

            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
                date=expense_date
            )
            expenses.append(line_expense)
            print(f"Expense ID: {index + 1}")
            print(f"Date: {line_expense.date}")
            print(f"Description: {line_expense.name}")
            print(f"Category: {line_expense.category}")
            print(f"Amount: ${line_expense.amount:.2f}")
            print("\n")

    if not expenses:
        print("No recorded expenses.")


def delete_expense(expense_file_path):
    print(f" Deleting User Expense")
    expenses: list[Expense] = []

    # Display the list of expenses with IDs for selection
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            # Split the line into four values (date, name, amount, category)
            expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")

            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
                date=expense_date  # Include the date when creating the Expense object
            )
            expenses.append(line_expense)
            print(f"{index + 1}. {line_expense}")

    if not expenses:
        print("No expenses to delete.")
        return

    try:
        expense_id_to_delete = int(
            input("Enter the ID of the expense to delete: "))

        if 1 <= expense_id_to_delete <= len(expenses):
            # Delete the selected expense
            deleted_expense = expenses.pop(expense_id_to_delete - 1)
            with open(expense_file_path, "w") as f:
                for expense in expenses:
                    f.write(
                        f"{expense.date},{expense.name},{expense.amount},{expense.category}\n")  # Include date in the saved file
            print(f"Deleted Expense: {deleted_expense}")
        else:
            print("Invalid expense ID. No expense deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid expense ID.")


def green(text):
    return f"\033[92m{text}\033[0m"


def main():
    print("Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    budget = float(input("Enter your budget for the month: "))
    choice = None

    while choice != "5":
        print("\nMenu:")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. List Expenses")
        print("4. Summarize Expenses")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == "2":
            delete_expense(expense_file_path)
        elif choice == "3":
            list_expenses(expense_file_path)
        elif choice == "4":
            summarize_expenses(expense_file_path, budget)
        elif choice == "5":
            print("Exiting Expense Tracker.")
        else:
            print("Invalid choice. Please try again!")


if __name__ == "__main__":
    main()
