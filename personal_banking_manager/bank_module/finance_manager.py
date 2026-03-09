from fpdf import FPDF
from pathlib import Path
from colorama import Fore, Style,Back
import os
import shutil
from datetime import datetime 
# create a finance manager class
class FinanceManager:
    # function add income
    def add_income(self,account: dict, amount: float):
        account["income"].append(amount)
        account["balance"] += amount
        print(Fore.GREEN +"Income added successfully." + Style.RESET_ALL)
    
    # function add expense
    def add_expense(self,account: dict, amount: float):
        if amount > account["balance"]:
            print(Fore.RED+"Insufficient balance for this expense."+Style.RESET_ALL)
            return
        account["expenses"].append(amount)
        account["balance"] -= amount
        print(Fore.GREEN +"Expense added successfully." + Style.RESET_ALL)
    
    # function add debt
    def add_debt(self,account: dict, amount: float, description: str):

        debt={
            "amount": amount,
            "description": description
        }

        account["debts"].append(debt)
        account["balance"] += amount
        print(Fore.GREEN +"Debt added successfully." + Style.RESET_ALL)

    # function pay debt
    def pay_debt(self,account: dict, amount: float):
        if not account["debts"]:
            print(Fore.BLUE+"No debts to pay."+Style.RESET_ALL)
            return
        if amount > account["balance"]:
            print(Fore.RED+"Insufficient balance to pay this debt."+Style.RESET_ALL)
            return
        print("Your debts:")
        for i, debt in enumerate(account["debts"],start=1):
            print(f"{i}- {debt['description']} : {debt['amount']:.2f}")
        
        try:
            choice_debt = int(input("Choose a debt to pay: "))-1
            if choice_debt < 0 or choice_debt >= len(account["debts"]):
                print(Fore.RED+"Invalid choice."+Style.RESET_ALL)
                return
            if amount > account["debts"][choice_debt]["amount"]:
                print(Fore.RED+"Amount exceeds total debt."+Style.RESET_ALL)
                return
            account["balance"] -= amount  
            account["debts"][choice_debt]["amount"] -= amount

            if account["debts"][choice_debt]["amount"] <= 0:
                account["debts"].pop(choice_debt)

            print(Fore.GREEN+"Debt paid successfully."+Style.RESET_ALL)
        except ValueError:
            print(Fore.RED+"Invalid input. Please enter a valid number."+Style.RESET_ALL)

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
            print(Fore.BLUE+"Excellent financial health."+Style.RESET_ALL)
        elif score >= 60:
            print(Fore.BLUE+"Good financial health."+Style.RESET_ALL)
        elif score >= 40:
            print(Fore.BLUE+"Average financial health."+Style.RESET_ALL)
        else:
            print(Fore.BLUE+"Poor financial health."+Style.RESET_ALL)
        
    # def generate_financial_report(self,account: dict):

    #     total_balance = 0
    #     total_debts = 0
    #     total_income = 0
    #     total_expenses = 0

    #     for acc in account.values():
    #         total_balance += acc["balance"] 
    #         total_debts += sum(debt["amount"] for debt in acc["debts"])
    #         total_income += sum(acc["income"])
    #         total_expenses += sum(acc["expenses"])
        
    #     net_worth = total_balance - total_debts

    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=16)
    #     pdf.cell(200, 10, txt="Personal Financial Report", ln=True, align="C")

    #     pdf.set_font("Arial", size=12)
    #     pdf.cell(200, 10, txt=f"Total Income: {total_income:.2f}", ln=True)
    #     pdf.cell(200, 10, txt=f"Total Expenses: {total_expenses:.2f}", ln=True)
    #     pdf.cell(200, 10, txt=f"Total Debts: {total_debts:.2f}", ln=True)
    #     pdf.cell(200, 10, txt=f"Total Balance: {total_balance:.2f}", ln=True)
    #     pdf.cell(200, 10, txt=f"Net Worth: {net_worth:.2f}", ln=True)

    #     report_folder="bank_reports"
    #     os.makedirs(report_folder, exist_ok=True)
    #     file_path = os.path.join(report_folder,"financial_report.pdf")
    #     pdf.output(file_path)
    #     print(Fore.GREEN+"Financial report generated successfully."+Style.RESET_ALL)
    
    def generate_financial_report(self, accounts: dict):

        total_balance = 0
        total_debts = 0
        total_income = 0
        total_expenses = 0

        # حساب القيم المالية
        for acc in accounts.values():
            total_balance += acc["balance"]
            total_debts += sum(debt["amount"] for debt in acc["debts"])
            total_income += sum(acc["income"])
            total_expenses += sum(acc["expenses"])

        net_worth = total_balance - total_debts

        # إنشاء التقرير
        pdf = FPDF()
        pdf.add_page()

        # عنوان التقرير
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 10, "Personal Financial Report", ln=True, align="C")

        pdf.ln(5)

        # تاريخ التقرير
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Generated on: {date}", ln=True)

        pdf.ln(5)

        # عنوان القسم
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Financial Summary", ln=True)

        # البيانات المالية
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Total Income      : {total_income:.2f} SAR", ln=True)
        pdf.cell(0, 8, f"Total Expenses    : {total_expenses:.2f} SAR", ln=True)
        pdf.cell(0, 8, f"Total Debts       : {total_debts:.2f} SAR", ln=True)
        pdf.cell(0, 8, f"Total Balance     : {total_balance:.2f} SAR", ln=True)

        pdf.ln(3)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Financial Health", ln=True)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Net Worth         : {net_worth:.2f} SAR", ln=True)

        # إنشاء مجلد التقارير
        report_folder = "personal_banking_manager/bank_reports"
        os.makedirs(report_folder, exist_ok=True)

        file_path = os.path.join(report_folder, "financial_report.pdf")

        # حفظ التقرير
        pdf.output(file_path)

        print(Fore.GREEN + "Financial report generated successfully." + Style.RESET_ALL)
        # print(f"Report location: {os.path.abspath(file_path)}")
                
