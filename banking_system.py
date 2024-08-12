import json

# Display menu
def display():
    # Displays the main menu
    bank_name = "SecureBank"
    print(f"=============================\n    Welcome to {bank_name}\n=============================")
    print("""    1. Open new account
    2. Deposit 
    3. Withdraw 
    4. Balance Enquiry
    5. All Account Holder List
    6. Modify Bank Account
    7. Close account
    8. Exit
=============================      
Select one option""")

# Load data from the database (file)
def load_data():
    # Loads data from 'database.json' file if it exists, otherwise returns empty lists
    try:
        with open('database.json', 'r') as db:
            data = json.load(db)
            return data['account_holders'], data['account_holders_pins'], data['balance_list']
    except FileNotFoundError:
        return [], [], []

# Save data to the database (file)
def save_data(account_holders, account_holders_pins, balance_list):
    # Saves the provided data to 'database.json' file
    data = {
        'account_holders': account_holders,
        'account_holders_pins': account_holders_pins,
        'balance_list': balance_list
    }
    with open('database.json', 'w') as db:
        json.dump(data, db, indent=4)  # Add indent for better readability

# Initializing the data
account_holders, account_holders_pins, balance_list = load_data()

def new_account():
    # Creates a new account with the user's name, pin, and initial deposit
    name = input("Enter Your Name : ")
    pin = input("Enter a pin of your choice : ")
    while len(pin) != 4 or not pin.isdigit():
        print("Pin must be a 4-digit number.")
        pin = input("Enter a pin of your choice : ")
    
    account_number = str(len(account_holders) + 1).zfill(4)
    
    amount = int(input("Enter money to deposit (Min Rs 500/-) : "))
    while amount < 500:
        print("Deposit Min Rs 500/-")
        amount = int(input("Enter money to deposit (Min Rs 500/-) : "))
    
    account_holders.append({"name": name, "account_number": account_number})
    account_holders_pins.append(pin)
    balance_list.append(amount)
    save_data(account_holders, account_holders_pins, balance_list)
    
    print("----New account created successfully! Your account number is {}----".format(account_number))

def deposit():
    # Deposits money into an account if the account number and pin are correct
    account_number = input("Enter account number : ")
    pin = input("Enter pin : ")
    
    for index, account in enumerate(account_holders):
        if account['account_number'] == account_number and account_holders_pins[index] == pin:
            amount = int(input("Enter amount to deposit : "))
            balance_list[index] += amount
            save_data(account_holders, account_holders_pins, balance_list)
            print("----Amount deposited successfully!----")
            print(f"----Your Balance is {balance_list[index]}----")
            return
    print("Account not found or incorrect pin.")

def withdraw():
    # Withdraws money from an account if the account number and pin are correct and sufficient balance is available
    account_number = input("Enter account number : ")
    pin = input("Enter pin : ")
    
    for index, account in enumerate(account_holders):
        if account['account_number'] == account_number and account_holders_pins[index] == pin:
            amount = int(input("Enter amount to withdraw : "))
            if balance_list[index] >= amount:
                balance_list[index] -= amount
                save_data(account_holders, account_holders_pins, balance_list)
                print("----Amount withdrawn successfully!----")
                print(f"----Your Balance is {balance_list[index]}----")
                return
            else:
                print("Insufficient balance.")
                return
    print("Account not found or incorrect pin.")

def balance_enquiry():
    # Displays the balance of an account if the account number and pin are correct
    account_number = input("Enter account number : ")
    pin = input("Enter pin : ")
    
    for index, account in enumerate(account_holders):
        if account['account_number'] == account_number and account_holders_pins[index] == pin:
            print(f"Your account balance is Rs. {balance_list[index]}")
            return
    print("Account not found or incorrect pin.")

def all_account_holders():
    # Displays a list of all account holders
    if account_holders:
        print("List of all account holders:")
        for i, account in enumerate(account_holders):
            print(f"{i+1}. {account['name']} (Account Number: {account['account_number']})")
    else:
        print("No account holders found.")

def modify_account():
    # Allows the user to change the pin of an account if the account number and current pin are correct
    account_number = input("Enter Your account number : ")
    pin = input("Enter current pin : ")
    
    for index, account in enumerate(account_holders):
        if account['account_number'] == account_number and account_holders_pins[index] == pin:
            new_pin = input("Enter new pin : ")
            while len(new_pin) != 4 or not new_pin.isdigit():
                print("Pin must be a 4-digit number.")
                new_pin = input("Enter new pin : ")
            account_holders_pins[index] = new_pin
            save_data(account_holders, account_holders_pins, balance_list)
            print("----Pin changed successfully!----")
            return
    print("Account not found or incorrect pin.")

def close_account():
    # Closes an account if the account number and pin are correct
    account_number = input("Enter Your account number : ")
    pin = input("Enter pin : ")
    
    for index, account in enumerate(account_holders):
        if account['account_number'] == account_number and account_holders_pins[index] == pin:
            del account_holders[index]
            del account_holders_pins[index]
            del balance_list[index]
            save_data(account_holders, account_holders_pins, balance_list)
            print("----Account closed successfully!----")
            return
    print("Account not found or incorrect pin.")

# Main loop to display the menu and execute selected operations
while True:
    display()
    input_value = input("Enter your choice: ")
    if input_value == '1':
        new_account()
    elif input_value == '2':
        deposit()
    elif input_value == '3':
        withdraw()
    elif input_value == '4':
        balance_enquiry()
    elif input_value == '5':
        all_account_holders()
    elif input_value == '6':
        modify_account()
    elif input_value == '7':
        close_account()
    elif input_value == '8':
        print("Exiting the system.\n\nThank You !!!\n\nHave a good day!")
        break
    else:
        print("Invalid input. Please try again.")
