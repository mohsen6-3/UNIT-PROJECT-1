from fpdf import FPDF
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
        
        try:
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
        except ValueError:
            print("Invalid input. Please enter a valid number.")

        # function financial summary
    def financial_summary(self,account: dict):
        total_income = 0
        total_expenses = 0
        total_debts = 0 
        total_balance = 0

        for acc in account.values():
            total_income += sum(acc["income"])
            total_expenses += sum(acc["expenses"])
            total_debts += sum(debt["amount"] for debt in acc["debts"])
            total_balance += acc["balance"]

        print("\n==== Financial Summary ====")
        print(f"Total Income: {total_income:.2f}")
        print(f"Total Expenses: {total_expenses:.2f}")
        print(f"Total Debts: {total_debts:.2f}")
        print(f"Total Balance: {total_balance:.2f}")
    
    # function net worth calculation
    def net_worth_calculation(self,account: dict):
        total_balance = 0
        total_debts = 0
        for acc in account.values():
            total_balance += acc["balance"] 
            total_debts += sum(debt["amount"] for debt in acc["debts"])
        net_worth = total_balance - total_debts
        print("\n==== Net Worth Calculation ====")
        print(f"Total Balance : {total_balance:.2f}")
        print(f"Total Debts   : {total_debts:.2f}")
        print(f"Net Worth     : {net_worth:.2f}")

    def financial_score(self,account: dict):
        total_balance = 0
        total_debts = 0
        total_income = 0
        total_expenses = 0

        for acc in account.values():
            total_balance += acc["balance"] 
            total_debts += sum(debt["amount"] for debt in acc["debts"])
            total_income += sum(acc["income"])
            total_expenses += sum(acc["expenses"])  
        
        score= 100

        #debt to income ratio
        if total_balance > 0:
            debt_ratio = total_debts / total_balance
            score -= debt_ratio * 40
        # expense to income ratio
        if total_expenses > total_income:
            score -=30

        if total_balance <100:
            score -=10

        score = max(0,round(score,2))
        print("\n==== Financial Score ====")
        print(f"Score: {score}/100")

        if score >= 80:
            print("Excellent financial health.")
        elif score >= 60:
            print("Good financial health.")
        elif score >= 40:
            print("Average financial health.")
        else:
            print("Poor financial health.")
        
    def generate_financial_report(self,account: dict):

        total_balance = 0
        total_debts = 0
        total_income = 0
        total_expenses = 0

        for acc in account.values():
            total_balance += acc["balance"] 
            total_debts += sum(debt["amount"] for debt in acc["debts"])
            total_income += sum(acc["income"])
            total_expenses += sum(acc["expenses"])
        
        net_worth = total_balance - total_debts

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="Personal Financial Report", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Total Income: {total_income:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Expenses: {total_expenses:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Debts: {total_debts:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Balance: {total_balance:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Net Worth: {net_worth:.2f}", ln=True)

        pdf.output("financial_report.pdf")
        print("Financial report generated successfully.")
        