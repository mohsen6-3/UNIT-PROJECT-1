import json
from bank_module.account_owner import AccountOwner
from colorama import Fore, Style,Back
FILE_NAME = "personal_banking_manager/bank_data/accounts.json"

class UserManager:


    # load data
    def load_data(self):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # save data
    def save_data(self, data):
        try:
            with open(FILE_NAME, "w") as file:
                json.dump(data, file, indent=4)
        except IOError :
            print(Fore.RED+"Error saving data."+Style.RESET_ALL)

    # register user
    def register(self, account_holder, national_id, password):
        password = str(password)
        data = self.load_data()

        if str(national_id) in data:
            print(Fore.BLUE+"User already registered."+Style.RESET_ALL)
            return None

        data[str(national_id)] = {
            "account_holder": account_holder,
            "password": password,
            "accounts": {}
        }

        self.save_data(data)

        print(Fore.GREEN+"User registered successfully."+Style.RESET_ALL)
        return AccountOwner(account_holder, national_id, password)

    # login user
    def login(self, national_id, password):
        password = str(password)
        data = self.load_data()

        if str(national_id) not in data:
            print(Fore.RED+"User not registered. Please register first."+Style.RESET_ALL)
            return None

        if data[str(national_id)]["password"] != password:
            print(Fore.RED+"Invalid password."+Style.RESET_ALL)
            return None

        account_holder = data[str(national_id)]["account_holder"]

        print(Fore.GREEN+f"Welcome {account_holder}!"+Style.RESET_ALL)

        return AccountOwner(account_holder, national_id,password)
    