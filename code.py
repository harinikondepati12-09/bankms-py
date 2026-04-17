accounts = {}
import msvcrt
import sys

def input_password(prompt):
    # If running in IDLE - use normal input
    if "idlelib" in sys.modules:
        return input(prompt)

    # Otherwise use masked input (CMD)
    import msvcrt
    print(prompt, end="", flush=True)

    password = ""

    while True:
        ch = msvcrt.getch()

        if ch == b'\r':
            print()
            break
        elif ch == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        elif ch in (b'\x00', b'\xe0'):
            msvcrt.getch()
        else:
            password += ch.decode("utf-8")
            print("*", end="", flush=True)

    return password

# load data
def load_data():
    global accounts
    try:
        file = open("bank.txt", "r")
        data = file.read()
        if data != "":
            accounts = eval(data)
        file.close()
    except:
        accounts = {}


# save data
def save_data():
    file = open("bank.txt", "w")
    file.write(str(accounts))
    file.close()


# login system
def login():
    username = input("Enter username: ")
    password = input_password("Password: ")

    if username == "admin" and password == "admin":
        print("Admin Login Successful")
        return "admin"

    elif username in accounts and accounts[username]["password"] == password:
        print("User Login Successful")
        return username

    else:
        print("Invalid login")
        return None


# create account
def create_account():
    username = input("Create username: ")
    password = input_password("Password: ")

    balance = int(input("Enter initial balance: "))

    accounts[username] = {
        "password": password,
        "balance": balance,
        "transactions": []
    }

    save_data()
    print("Account created successfully!")
    
# view minimum balance
def view_balance(user):
    print("Current Balance:", accounts[user]["balance"])
    
# deposit
def deposit(user):
    amount = int(input("Enter amount: "))
    accounts[user]["balance"] += amount
    accounts[user]["transactions"].append("Deposited " + str(amount))
    save_data()
    print("Amount deposited!")


# withdraw
def withdraw(user):
    amount = int(input("Enter amount: "))
    if accounts[user]["balance"] >= amount:
        accounts[user]["balance"] -= amount
        accounts[user]["transactions"].append("Withdrew " + str(amount))
        save_data()
        print("Amount withdrawn!")
    else:
        print("Insufficient balance!")


# fund transfer
def transfer(user):
    to_user = input("Enter receiver username: ")
    amount = int(input("Enter amount: "))

    if to_user in accounts:
        if accounts[user]["balance"] >= amount:
            accounts[user]["balance"] -= amount
            accounts[to_user]["balance"] += amount

            accounts[user]["transactions"].append("Transferred " + str(amount) + " to " + to_user)
            accounts[to_user]["transactions"].append("Received " + str(amount) + " from " + user)

            save_data()
            print("Transfer successful!")
        else:
            print("Insufficient balance!")
    else:
        print("Receiver not found!")


# transcation history
def show_transactions(user):
    print("Transaction History:")
    for t in accounts[user]["transactions"]:
        print(t)


# interest
def calculate_interest(user):
    rate = 5
    time = 1
    balance = accounts[user]["balance"]
    interest = (balance * rate * time) / 100
    print("Interest:", interest)


# loan check
def loan_check(user):
    if accounts[user]["balance"] > 5000:
        print("Eligible for loan")
    else:
        print("Not eligible")


# delete account
def delete_account(user):
    confirm = input("Are you sure? (yes/no): ")
    if confirm == "yes":
        del accounts[user]
        save_data()
        print("Account deleted!")
        return True
    return False


# admin panel
def admin_panel():
    while True:
        print("\n- ADMIN PANEL -")
        print("1. View All Accounts")
        print("2. Delete Any Account")
        print("3. Logout")

        ch = int(input("Enter choice: "))

        if ch == 1:
            print(accounts)

        elif ch == 2:
            user = input("Enter username to delete: ")
            if user in accounts:
                del accounts[user]
                save_data()
                print("Account deleted by admin")
            else:
                print("User not found")

        elif ch == 3:
            break


# user menu
def user_menu(user):
    while True:
        print("\n- USER MENU -")
        print("1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Interest")
        print("7. Loan Check")
        print("8. Delete Account")
        print("9. Logout")

        ch = int(input("Enter choice: "))

        if ch == 1:
            view_balance(user)

        elif ch == 2:
            deposit(user)

        elif ch == 3:
            withdraw(user)

        elif ch == 4:
            transfer(user)

        elif ch == 5:
            show_transactions(user)

        elif ch == 6:
            calculate_interest(user)

        elif ch == 7:
            loan_check(user)

        elif ch == 8:
            if delete_account(user):
                break

        elif ch == 9:
            break


# main menu
load_data()

while True:
    print("\n1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        create_account()

    elif choice == 2:
        user = login()
        if user == "admin":
            admin_panel()
        elif user:
            user_menu(user)

    elif choice == 3:
        save_data()
        break
