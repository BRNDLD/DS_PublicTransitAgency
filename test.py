from logic.db import DbController
from logic.usuario import User

def handle_user_input():
    username = input("Enter username: ")
    password = input("Enter password: ")
    code = input("Enter code (optional): ")

    user = User(DbController())

    if code:
        if user.authenticate(username, password):
            print("Successful login as admin.")
        else:
            confirm_password = input("Confirm password: ")
            signup_message = user.signup(username, password, confirm_password)
            print(signup_message)
    else:
        if user.authenticate(username, password):
            print("Successful login.")
        else:
            print("User does not exist.")

if __name__ == "__main__":
    handle_user_input()