from bank_module.account_owner import AccountOwner
from bank_module.user_manager import UserManager
from colorama import Fore, Style
import pwinput
from pyfiglet import Figlet

f = Figlet(font="small")

print(Fore.BLUE+f.renderText("Unified Personal Banking Manager")+Style.RESET_ALL)



user_manager = UserManager()
current_user = None

def get_number_input(message):
    try:
        return int(input(message))
    except ValueError:
        print(Fore.RED+"Invalid input. Please enter a number."+Style.RESET_ALL)
        return None

def require_login():
    global current_user
    if current_user is None:
        print(Fore.BLUE+"You must login first."+Style.RESET_ALL)
        return False
    return True
menu ='''
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
    choice = input(Fore.LIGHTWHITE_EX + menu + Style.RESET_ALL)
    match choice:
        # Register Account Holder
        case "1":
            name = input("Enter your name: ")
            national_id = get_number_input("Enter your national ID: ")
            if national_id is None:
                continue
            try:
                password = int(pwinput.pwinput("Enter your password: ", mask="*"))
                confirm = int(pwinput.pwinput("Confirm password: ", mask="*"))
                if password != confirm:
                    print(Fore.RED+"Passwords do not match. Please try again."+Style.RESET_ALL)
                    continue
            except ValueError:
                print(Fore.RED+"Invalid input. Please enter a valid password."+Style.RESET_ALL)
                continue
            user = user_manager.register(name, national_id,password)
            if user:
                current_user = user
        # Login Account Holder
        case "2":
            if current_user is not None:
                print(Fore.BLUE + f"User {current_user.get_account_holder()} already logged in." + Style.RESET_ALL)
                continue

            national_id = get_number_input("Enter your national ID: ")
            if national_id is None:
                continue
            try:
                password = int(pwinput.pwinput("Enter your password: ", mask="*"))
            except ValueError:
                print(Fore.RED+"Invalid input. Please enter a valid password."+Style.RESET_ALL)
                continue
            user = user_manager.login(national_id, password)
            if user:
                current_user = user              
        # Logout Account Holder
        case "3":
            if not require_login():
                continue

            print(Fore.GREEN + f"{current_user.get_account_holder()} logged out successfully." + Style.RESET_ALL)
            current_user = None
        # Add Bank Account
        case "4":
            if not require_login():
                continue

            bank = input("Enter your bank name such as (Alrajhi-SNP-Riyadh-Alinma-Albilad-...): ")
            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.add_account(bank, account_number)
        # Show Bank Accounts
        case "5":
            if not require_login():
                continue

            current_user.show_accounts()
        
        # Delete Bank Account
        case "6":
            if not require_login():
                continue

            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.delete_account(account_number)
    
        # Update Bank Account
        case "7":
            if not require_login():
                continue

            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.update_account(account_number)
            current_user.show_accounts()
        # Add Income
        case "8":
            if not require_login():
                continue

            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.add_income(account_number)
        # Add Expense
        case "9":
            if not require_login():
                continue

            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.add_expense(account_number)
        # Add Debt
        case "10":
            if not require_login():
                continue

            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.add_debt(account_number)
        # Pay Debt
        case "11":
            if not require_login():
                continue

            account_number = get_number_input("Enter your account number: ")
            if account_number is None:
                continue

            current_user.pay_debt(account_number)
        # Financial Summary15
        case "12":
            if not require_login():
                continue

            current_user.financial_summary()
        # Net Worth Calculation
        case "13":
            if not require_login():
                continue

            current_user.net_worth_calculation()
        # Financial Score
        case "14":
            if not require_login():
                continue

            current_user.financial_score()
        # Generate Financial PDF Report
        case "15":
            if not require_login():
                continue

            current_user.generate_financial_report()
        # Exit
        case "16":
            print(Fore.GREEN+"Exiting the program. Goodbye!"+Style.RESET_ALL)
            break
        # Default case for invalid input
        case _:
            print(Fore.RED+"Invalid option. Please try again."+Style.RESET_ALL)