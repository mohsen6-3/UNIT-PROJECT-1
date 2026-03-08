import json
from bank_module.account_owner import AccountOwner

class UserManager:

    FILE_NAME = "accounts.json"

    # load data
    def load_data(self):
        try:
            with open(self.FILE_NAME, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    # save data
    def save_data(self, data):
        try:
            with open(self.FILE_NAME, "w") as file:
                json.dump(data, file, indent=4)
        except IOError :
            print("Error saving data.")

    # register user
    def register(self, account_holder, national_id):

        data = self.load_data()

        if str(national_id) in data:
            print("User already registered.")
            return None

        data[str(national_id)] = {
            "account_holder": account_holder,
            "accounts": {}
        }

        self.save_data(data)

        print("User registered successfully.")
        return AccountOwner(account_holder, national_id)

    # login user
    def login(self, national_id):

        data = self.load_data()

        if str(national_id) not in data:
            print("User not registered. Please register first.")
            return None

        account_holder = data[str(national_id)]["account_holder"]

        print(f"Welcome {account_holder}!")

        return AccountOwner(account_holder, national_id)