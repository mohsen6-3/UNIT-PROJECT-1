from fpdf import FPDF
from pathlib import Path
from colorama import Fore, Style,Back
import os
import shutil
from datetime import datetime 
from tabulate import tabulate
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
        
        data =[
            ["Total Income", f"{total_income:.2f} SAR"],
            ["Total Expenses", f"{total_expenses:.2f} SAR"],
            ["Total Debts", f"{total_debts:.2f} SAR"],
            ["Total Balance", f"{total_balance:.2f} SAR"]
        ]

        header = ["Financial Summary", "Amount (SAR)"]
        print(tabulate(data, headers=header, tablefmt="fancy_grid"))

    # function net worth calculation
    def net_worth_calculation(self,account: dict):
        total_balance = 0
        total_debts = 0
        for acc in account.values():
            total_balance += acc["balance"] 
            total_debts += sum(debt["amount"] for debt in acc["debts"])
        net_worth = total_balance - total_debts

        data = [
            ["Total Balance", f"{total_balance:.2f} SAR"],
            ["Total Debts", f"{total_debts:.2f} SAR"],
            ["Net Worth", f"{net_worth:.2f} SAR"]
        ]
        header = ["Net Worth Calculation", "Amount (SAR)"]
        print(tabulate(data, headers=header, tablefmt="fancy_grid"))

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
        data = [
            ["Score", f"{score}/100"]
        ]
        header = ["Financial Score", "Rating"]
        print(tabulate(data, headers=header, tablefmt="fancy_grid"))
       
        if score >= 80:
            print(Fore.GREEN+"Excellent financial health."+Style.RESET_ALL)
        elif score >= 60:
            print(Fore.GREEN+"Good financial health."+Style.RESET_ALL)
        elif score >= 40:
            print(Fore.GREEN+"Average financial health."+Style.RESET_ALL)
        else:
            print(Fore.RED+"Poor financial health."+Style.RESET_ALL)
        return
        
    def generate_financial_report(self, accounts: dict,account_holder: str):

        total_balance = 0
        total_debts = 0
        total_income = 0
        total_expenses = 0
        account_holder = "Unknown"

       
        for acc in accounts.values():
            total_balance += acc["balance"]
            total_debts += sum(debt["amount"] for debt in acc["debts"])
            total_income += sum(acc["income"])
            total_expenses += sum(acc["expenses"])

            if "account_holder" in acc:
                account_holder = acc["account_holder"]

        net_worth = total_balance - total_debts

        financial_score = self.financial_score(accounts)
       
        pdf = FPDF()
        pdf.add_page()

       
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 10, "Personal Financial Report", ln=True, align="C")

        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Account Holder: {account_holder}", ln=True)

        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Generated on: {date}", ln=True)

        pdf.ln(5)

        
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Financial Summary", ln=True)

        
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
        pdf.cell(0, 8, f"Financial Score    : {financial_score}", ln=True)

        
        report_folder = "personal_banking_manager/bank_reports"
        os.makedirs(report_folder, exist_ok=True)

        file_path = os.path.join(report_folder, "financial_report.pdf")

        
        pdf.output(file_path)

        print(Fore.GREEN + "Financial report generated successfully." + Style.RESET_ALL)
        
                
