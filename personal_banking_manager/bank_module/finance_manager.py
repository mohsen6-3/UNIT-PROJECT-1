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
        return total_income, total_expenses, total_debts, total_balance

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
        return total_balance, total_debts, net_worth

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
        return score
        
    def generate_financial_report(self, accounts: dict, account_holder: str):

        income, expenses, debts, balance = self.financial_summary(accounts)
        total_balance, total_debts, net_worth = self.net_worth_calculation(accounts)
        score = self.financial_score(accounts)

        pdf = FPDF()
        pdf.add_page()

        # ---------- Title ----------
        pdf.set_font("Arial","B",18)
        pdf.cell(0,10,"Personal Banking Financial Report",ln=True,align="C")

        pdf.ln(5)

        # ---------- Account info ----------
        pdf.set_font("Arial",size=12)

        pdf.cell(0,8,f"Account Holder: {account_holder}",ln=True)

        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        pdf.cell(0,8,f"Report Date: {date}",ln=True)

        pdf.ln(5)

        # ---------- Financial Summary ----------
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,"Financial Summary",ln=True)

        pdf.set_font("Arial",size=12)

        pdf.cell(0,8,f"Total Income: {income:.2f} SAR",ln=True)
        pdf.cell(0,8,f"Total Expenses: {expenses:.2f} SAR",ln=True)
        pdf.cell(0,8,f"Total Debts: {debts:.2f} SAR",ln=True)
        pdf.cell(0,8,f"Total Balance: {balance:.2f} SAR",ln=True)

        pdf.ln(5)

        # ---------- Net Worth ----------
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,"Net Worth Calculation",ln=True)

        pdf.set_font("Arial",size=12)

        pdf.cell(0,8,f"Total Balance: {total_balance:.2f} SAR",ln=True)
        pdf.cell(0,8,f"Total Debts: {total_debts:.2f} SAR",ln=True)
        pdf.cell(0,8,f"Net Worth: {net_worth:.2f} SAR",ln=True)

        pdf.ln(5)

        # ---------- Financial Score ----------
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,"Financial Score",ln=True)

        pdf.set_font("Arial",size=12)

        pdf.cell(0,8,f"Score: {score}/100",ln=True)

        if score >= 80:
            status = "Excellent"
        elif score >= 60:
            status = "Good"
        elif score >= 40:
            status = "Average"
        else:
            status = "Poor"

        pdf.cell(0,8,f"Financial Health: {status}",ln=True)

        pdf.ln(5)

        # ---------- Accounts Details ----------
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,"Accounts Details",ln=True)

        pdf.set_font("Arial",size=12)

        for name, acc in accounts.items():

            balance = acc["balance"]
            income = sum(acc["income"])
            expenses = sum(acc["expenses"])
            debts = sum(debt["amount"] for debt in acc["debts"])

            pdf.cell(0,8,f"Account: {name}",ln=True)
            pdf.cell(0,8,f"Balance: {balance:.2f} SAR",ln=True)
            pdf.cell(0,8,f"Income: {income:.2f} SAR",ln=True)
            pdf.cell(0,8,f"Expenses: {expenses:.2f} SAR",ln=True)
            pdf.cell(0,8,f"Debts: {debts:.2f} SAR",ln=True)

            pdf.ln(3)

        # ---------- Save file ----------
        report_folder = "personal_banking_manager/bank_reports"
        os.makedirs(report_folder, exist_ok=True)

        file_path = os.path.join(report_folder,"financial_report.pdf")

        pdf.output(file_path)

        print(Fore.GREEN+"Financial report generated successfully."+Style.RESET_ALL)
        
                
