import json
from bank_module.finance_manager import FinanceManager
from colorama import Fore, Style,Back
# Create class AccountOwner
class AccountOwner:
    # constructor 
    def __init__(self,account_holder:str,national_id:int):
        self.__account_holder = account_holder
        self.__national_id = national_id
        self.accounts = {}
        self.load_account_data()

    # getter and setter for account holder 
    def set_account_holder(self,account_holder:str):  
        self.__account_holder = account_holder
    def get_account_holder(self):
        return self.__account_holder
    
    # getter and setter for national ID
    def set_national_id(self,national_id:int):
        self.__national_id = national_id
    def get_national_id(self):
        return self.__national_id
    
    # function add bank account
    def add_account(self,bank_name:str,account_number:int):
        account_number = str(account_number)
        if account_number in self.accounts:
            print(Fore.BLUE+"Account already exists for this user."+Style.RESET_ALL)
            return
        self.accounts[account_number] = {
            "bank_name": bank_name,
            "balance": 0,
            "income": [],
            "expenses": [],
            "debts": []
        }
        self.save_account_data()

        print(Fore.GREEN +"Account added successfully."+Style.RESET_ALL)
    # function show bank accounts
    def show_accounts(self):
        if  not  self.accounts:
            print(Fore.BLUE+"No accounts found ."+Style.RESET_ALL)
            return
        print(f"Bank Accounts for {self.get_account_holder()}:")
        print("Account Number   | Bank Name    | Balance      | Income       | Expenses     | Debts")
        print("-"*90)
        for account_number,account in self.accounts.items():
            print(f"{account_number:<15}  |  {account['bank_name']:<10}  |  {account['balance']:<10.2f}  |  {sum(account['income']):<10.2f}  |  {sum(account['expenses']):<10.2f}  |  {sum(debt['amount'] for debt in account['debts']):<10.2f}")
        self.save_account_data()
    # function delete bank account
    def delete_account(self,account_number:int):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print(Fore.BLUE+"Account not found."+Style.RESET_ALL)
            return
        del self.accounts[account_number]
        self.save_account_data()
        print(Fore.GREEN+"Account deleted successfully."+Style.RESET_ALL)

    # function update bank account
    def update_account(self,account_number:int):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print(Fore.BLUE+"Account not found."+Style.RESET_ALL)
            return
        
        choise = input("Do you want to update (bank) only or (all)? ")

        if choise.lower() == "bank":
            new_bank_name = input("Enter new bank name: ")
            self.accounts[account_number]["bank_name"] = new_bank_name

        elif choise.lower() == "all":
            try:
                new_account_number = int(input("Enter new account number: "))
            except ValueError:
                print(Fore.RED+"Invalid input. Account number must be a number."+Style.RESET_ALL)
                return
            new_bank_name = input("Enter new bank name: ")
            new_account_number = str(new_account_number)
            if new_account_number in self.accounts:
                print(Fore.BLUE+"Account number already exists. Please choose a different number."+Style.RESET_ALL)
                return
            self.accounts[new_account_number] = self.accounts.pop(account_number)
            self.accounts[new_account_number]["bank_name"] = new_bank_name
        else:
            print(Fore.RED+"Invalid choice. Please choose 'bank' or 'all'."+Style.RESET_ALL)
            return

        self.save_account_data()
        print(Fore.GREEN+"Account updated successfully."+Style.RESET_ALL)

    # function to save account data to a JSON file
    def save_account_data(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        data[str(self.get_national_id())] = {
            "account_holder": self.get_account_holder(),
            "accounts": self.accounts
        }
        with open("accounts.json", "w") as file:
            json.dump(data, file, indent=4)

    # function to load account data from a JSON file
    def load_account_data(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
                if str(self.get_national_id()) in data:
                    self.accounts = data[str(self.get_national_id())]["accounts"]
                else:
                    self.accounts = {}
        except FileNotFoundError:
            self.accounts = {}  
    
    # function add income to a specific account
    def add_income(self, account_number):

        account_number = str(account_number)
        if account_number not in self.accounts:
            print(Fore.BLUE+"Account not found."+Style.RESET_ALL)
            return
        try:
            amount = float(input("Enter income amount: "))
            finance = FinanceManager()
            finance.add_income(self.accounts[account_number], amount)
            self.save_account_data()
        except ValueError:
            print(Fore.RED+"Invalid input. Please enter a valid number."+Style.RESET_ALL)
            return
    # function add expense to a specific account
    def add_expense(self, account_number):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print(Fore.BLUE+"Account not found."+Style.RESET_ALL)
            return
        try:
            amount = float(input("Enter expense amount: "))
            finance = FinanceManager()
            finance.add_expense(self.accounts[account_number], amount)
            self.save_account_data()
        except ValueError:
            print(Fore.RED+"Invalid input. Please enter a valid number."+Style.RESET_ALL)
            return

    # function add debt to a specific account
    def add_debt(self, account_number):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print(Fore.BLUE+"Account not found."+Style.RESET_ALL)
            return
        try:
            amount = float(input("Enter debt amount: "))
            description = input("Enter debt description: ")
            finance = FinanceManager()
            finance.add_debt(self.accounts[account_number], amount, description)
            self.save_account_data()
        except ValueError:
            print(Fore.RED+"Invalid input. Please enter a valid number."+Style.RESET_ALL)
            return
    
    # function pay debt from a specific account
    def pay_debt(self, account_number):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print(Fore.BLUE+"Account not found."+Style.RESET_ALL)
            return
        try:
            amount = float(input("Enter amount to pay towards debt: "))
            finance = FinanceManager()
            finance.pay_debt(self.accounts[account_number], amount)
            self.save_account_data()
        except ValueError:
            print(Fore.RED+"Invalid input. Please enter a valid number."+Style.RESET_ALL)

    def financial_summary(self):
        finance = FinanceManager()
        finance.financial_summary(self.accounts)

    def net_worth_calculation(self):
        finance = FinanceManager()
        finance.net_worth_calculation(self.accounts)
    
    def financial_score(self):
        finance = FinanceManager()
        finance.financial_score(self.accounts)
    
    def generate_financial_report(self):
        finance = FinanceManager()
        finance.generate_financial_report(self.accounts)
        