# create a finance manager class
class FinanceManager:
    # function add income
    def add_income(self,account: dict, amount: float):
        account["income"].append(amount)
        account["balance"] += amount
        print("Income added successfully.")
    
    # function add expense
    def add_expense(self,account: dict, amount: float):
        if amount > account["balance"]:
            print("Insufficient balance for this expense.")
            return
        account["expenses"].append(amount)
        account["balance"] -= amount
        print("Expense added successfully.")
    
    # function add debt
    def add_debt(self,account: dict, amount: float, description: str):

        debt={
            "amount": amount,
            "description": description
        }

        account["debts"].append(debt)
        account["balance"] += amount
        print("Debt added successfully.")

    # function pay debt
    def pay_debt(self,account: dict, amount: float):
        if not account["debts"]:
            print("No debts to pay.")
            return
        if amount > account["balance"]:
            print("Insufficient balance to pay this debt.")
            return
        print("Your debts:")
        for i, debt in enumerate(account["debts"],start=1):
            print(f"{i}- {debt['description']} : {debt['amount']:.2f}")
        
        choice_debt = int(input("Choose a debt to pay: "))-1
        if choice_debt < 0 or choice_debt >= len(account["debts"]):
            print("Invalid choice.")
            return
        if amount > account["debts"][choice_debt]["amount"]:
            print("Amount exceeds total debt.")
            return
        account["balance"] -= amount  
        account["debts"][choice_debt]["amount"] -= amount

        if account["debts"][choice_debt]["amount"] <= 0:
            account["debts"].pop(choice_debt)

        print("Debt paid successfully.")