import json
import random

def deposit_cash(account, acc_num):
    amount = int(input('How much would your like to be deposited?\n'))
    current_balance = account['balance']

    current_balance += amount
    save_account(account['name'], account['contact'], acc_num, account['pin'], current_balance)

def withdraw_cash(account, acc_num):
    amount_required = int(input('How much would you like to withdraw?\n'))
    current_balance = account['balance']

    if amount_required > current_balance:
        print('Sorry, but you do not have enough balance.')
    else:
        current_balance -= amount_required
        print(f'Successfully withdrawn cash!\nBalance: {current_balance}')
    save_account(account['name'], account['contact'], acc_num, account['pin'], current_balance)
    

def check_balance(account):
    balance = account['balance']
    print(f'Your current balance is ₹{balance}')

def user_ops(account, acc_num):
    name = account['name']
    print(account)
    print(f'Welcome, {name}!')
    print('What would you like to do today?')
    print('1. Check balance\n2. Withdraw cash\n3. Deposit cash\n4. Logout\n')

    ch = int(input())

    if ch == 1:
        check_balance(account)
        pass
    elif ch == 2:
        withdraw_cash(account, acc_num)
        pass
    elif ch == 3:
        deposit_cash(account, acc_num)
        pass
    else:
        print(f'Have a good day, {name}!')
        welcome()

    account = load_account(acc_num)
    user_ops(account, acc_num)

def load_account(acc_num, login=False):
    with open('./accounts.json', mode='r') as data_file:
        data = json.load(data_file)
    if login:
        return data
    return data[acc_num]

def login():
    acc_num = input("Please enter your account number")
    try:
        data = load_account(acc_num, login=True)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print('Not registered.')
        welcome()
    else:
        try:
            account = data[acc_num]
        except KeyError:
            print('No users found.')
            login()
        else:
            pin = int(input('Enter pin.\n'))
            if pin == account['pin']:
                user_ops(account, acc_num)
            else:
                print('Incorrect pin.')
                welcome()
            

def pin_setup():
    pin = int(input('Enter your 4 digit pin:\n'))
    pin_reenter = int(input('Re-enter pin.\n'))

    if pin == pin_reenter:
        return pin
    else:
        print('Pins do not match! Re-enter.')
        pin_setup()

def save_account(name, contact, acc_num, pin, balance):

    new_data = {
        acc_num: {
            'name': name,
            'pin': pin,
            'contact': contact,
            'balance': balance,
        }
    }

    try:
        with open('./accounts.json', mode='r') as file:
            data = json.load(file)
            data.update(new_data)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open('./accounts.json', mode='w') as file:
            json.dump(new_data, file, indent=4)
    else:
        with open('./accounts.json', mode='w') as file:
            json.dump(data, file, indent=4)


def setup_user(new):

    if new == 1:
        print('Welcome, user!\n\nTo setup your account, we need a few details.')

    name = input('Enter your name.\n')
    contact = input('Enter contact (Phone/E-mail).')

    account_number = ''

    for i in range(12):
        account_number += str(random.randint(1, 9))

    print(f'Name: {name}\nContact: {contact}\nAccount Number: {account_number}')
    yna = input('Did we get that right? (Y/N)')
    yna = yna.upper()

    if yna == 'Y':
        print('Moving on...')
    if yna == 'N':
        print('Oops! Let\'s do that once more.')
        setup_user(0)
    
    pin = pin_setup()

    print('Finishing up...')
    save_account(name, contact, account_number, pin, 0)
    print('You have successfully registered!')
    welcome()


def welcome():
    print('Welcome!\nWhat would you like to do?')
    print('1. Login\n2. Register\n3. Quit')
    ch = int(input())

    if ch == 1:
        login()
        pass
    elif ch == 2:
        setup_user(1)
        pass
    else:
        print('Thanks for visiting! Have a great day!')
        exit()

welcome()