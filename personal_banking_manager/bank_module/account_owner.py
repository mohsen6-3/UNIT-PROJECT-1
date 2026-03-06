import json

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
            print("Account already exists for this user.")
            return
        self.accounts[account_number] = {
            "bank_name": bank_name,
            "balance": 0,
            "income": [],
            "expenses": [],
            "debts": []
        }
        self.save_account_data()
        print("Account added successfully.")
    # function show bank accounts
    def show_accounts(self):
        if  not  self.accounts:
            print("No accounts found .")
            return
        print(f"Bank Accounts for {self.get_account_holder()}:")
        print("Account Number   | Bank Name    | Balance")
        print("-"*40)
        for account_number,account in self.accounts.items():
            print(f"{account_number:<15}  |  {account['bank_name']:<10}  |  {account['balance']}")
        self.save_account_data()
    # function delete bank account
    def delete_account(self,account_number:int):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print("Account not found.")
            return
        del self.accounts[account_number]
        self.save_account_data()
        print("Account deleted successfully.")

    # function update bank account
    def update_account(self,account_number:int):
        account_number = str(account_number)
        if account_number not in self.accounts:
            print("Account not found.")
            return
        choise = input("Do you want to update (bank) only or (all)? ")

        if choise.lower() == "bank":
            new_bank_name = input("Enter new bank name: ")
            self.accounts[account_number]["bank_name"] = new_bank_name

        elif choise.lower() == "all":
            new_account_number = input("Enter new account number: ")
            new_bank_name = input("Enter new bank name: ")
            if new_account_number in self.accounts:
                print("Account number already exists. Please choose a different number.")
                return
            self.accounts[new_account_number] = self.accounts.pop(account_number)
            self.accounts[new_account_number]["bank_name"] = new_bank_name
        else:
            print("Invalid choice. Please choose 'bank' or 'all'.")

        self.save_account_data()
        print("Account updated successfully.")

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