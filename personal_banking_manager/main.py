from bank_module.account_owner import AccountOwner
from bank_module.user_manager import UserManager


user_manager = UserManager()
current_user = None

menu = '''
\n"===== Unified Personal Banking Manager ====="
1- Register account holder
2- Login account holder
3- Logout account holder
4- Add Bank Account
5- Show Bank Accounts
6- Delete Bank Account
7- Update Bank Account
8- Add Income
9- Add Expense
10- Add Debt
11- Pay Debt
12- Financial Summary
13- Net Worth Calculation
14- Financial Score
15- Generate Financial PDF Report
16- Exit
Please select an option (1-16):
'''
while True:
    match input(menu):
        # Register Account Holder
        case "1":
            account_holder = input("Enter your name: ")
            national_id = int(input("Enter your national ID: "))

            user = user_manager.register(account_holder, national_id)

            if user:
                current_user = user
        # Login Account Holder
        case "2":
            if current_user is not None:
                print(f"User {current_user.get_account_holder()} already logged in.")
            else:
                national_id = int(input("Enter your national ID: "))
                user = user_manager.login(national_id)
                if user:
                    current_user = user              
        # Logout Account Holder
        case "3":
            if current_user is None:
                print("No user logged in.")
            else:
                print(f"User {current_user.get_account_holder()} logged out successfully.")
                current_user = None
        # Add Bank Account
        case "4":
            if current_user is None:
                print("You must login first.")
            else:
                user_bank = input("Enter your bank name such as (Alrajhi-SNP-Riyadh-Alinma-Albilad-...): ")
                user_account_number = int(input("Enter your account number: "))
                current_user.add_account(user_bank, user_account_number)
        # Show Bank Accounts
        case "5":
            if current_user is None:
                print("No user logged in.")
            else:
                current_user.show_accounts()
        
        # Delete Bank Account
        case "6":
            if current_user is None:
                print("No user logged in.")
            else:
                user_account_number = input("Enter your account number: ")
                current_user.delete_account(user_account_number)
    
        # Update Bank Account
        case "7":
            if current_user is None:
                print("No user logged in.")
            else:
                user_account_number = input("Enter your account number: ")
                current_user.update_account(user_account_number)
                current_user.show_accounts()
        # Add Income
        case "8":
            if current_user is None:
                print("No user logged in.")
            else:
                account_number = input("Enter your account number: ")
                current_user.add_income(account_number)
        # Add Expense
        case "9":
            pass
        # Add Debt
        case "10":
            pass
        # Pay Debt
        case "11":
            pass
        # Financial Summary
        case "12":
            pass
        # Net Worth Calculation
        case "13":
            pass
        # Financial Score
        case "14":
            pass
        # Generate Financial PDF Report
        case "15":
            pass
        # Exit
        case "16":
            print("Exiting the program. Goodbye!")
            break
        # Default case for invalid input
        case _:
            print("Invalid option. Please try again.")