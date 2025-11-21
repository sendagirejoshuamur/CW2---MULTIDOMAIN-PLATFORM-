import bcrypt
import os
import re
import streamlit as st


def hashpassword(plain_text_password):
    # encoding password to bytes
    password_bytes = plain_text_password.encode('utf-8')

    #generating a salt to be added to hashed password to make password stronger
    salt = bcrypt.gensalt()

    #hashing the password in bytes and later will need to be converted to string
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)

    #hashed passoword being  converted to string
    hashed_password_string = hashed_password_bytes.decode('utf-8')

    return hashed_password_string

def verify_password(hashed_password_string, plain_text_password):
    #converting the plain text password to bytes for comparison
    password_bytes = plain_text_password.encode('utf-8')


    #converting the hashed password to bytes for comparison
    hashed_bytes = hashed_password_string.encode('utf-8')

    # this function extracts the salt from the hash and compares it
    is_valid = bcrypt.checkpw(password_bytes, hashed_bytes)

    print(is_valid)
    return is_valid

# creating a textfile to store the users login info
USER_DATA_FILE = 'users.txt'


def user_exists(username):
    # """Check if a username already exists in the user data file"""
    # handling the case were the file doesnt exist
    try:
        if not os.path.isfile(USER_DATA_FILE):
            return False

        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                # this will remove any white space and split by commas in the username
                stored_username = line.strip().split(',')[0]
                if stored_username == username:
                    return True
        return False

    # incase there is an error it will print the following plus the error message stored in error
    except Exception as error:
        print(f"Error checking username: {error}")
        return False




def register_user(username, password):
    # checking if the username exists
    if user_exists(username):
        print(f"User {username} already exists")
        return False

    # hashing the password to store in the file
    hashed_password = hashpassword(password)

    try :
        # appending the username and hashed password to the file
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f"{username},{hashed_password}\n")
            print(f"User {username} registered successfully")
            return True

    except Exception as error:
        # incase there is an error it will print the following plus the error message stored in error
        print(f"Failed to register user {username}: {error}")
        return False


def login_user(username, password):
    # checking if the registered users by checking if the file is empty
    if os.path.getsize(USER_DATA_FILE) == 0:
        print("no users registered yet")
        return False

    try:
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                stored_username = line.strip().split(',')[0]
                stored_hash = line.strip().split(',')[1]

                if stored_username == username:
                    if verify_password(stored_hash, password):
                        print(f"successfully logged in: {stored_username}")
                        return True
                    else:
                        print(f"invalid password login failed with: {stored_username}")
                        return False

        # If we get here, we've checked all users and didn't find the username
        print("username not found")
        return False

    except Exception as error:
        print(f"Failed to login user: {error}")
        return False



def validate_username(username):
    # """
    # Validating username format using regex.
    # Args:
    #     username (str): The username to validate   
    # Returns:
    #     tuple: (bool, str) - (is_valid, error_message)
    # """
    
    # Check if username is empty
    if not username:
        return False, "Username cannot be empty."

    # Check length requirements
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    
    if len(username) > 20:
        return False, "Username cannot exceed 20 characters."
    
    # Regex pattern: only alphanumeric characters (letters and numbers)
    username_pattern = r'^[a-zA-Z0-9]+$'
    
    if not re.match(username_pattern, username):
        return False, "Username can only contain letters (a-z, A-Z) and numbers (0-9)."
    
    # All checks passed
    return True, "Username is valid."


def validate_password(password):
    # """
    # Validating password strength using regex.
    # Args:
    #     password (str): The password to validate
        
    # Returns:
    #     tuple: (bool, str) - (is_valid, error_message)
    # """
    
    # Check if password is empty
    if not password:
        return False, "Password cannot be empty."
    
    # Check length requirements
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    if len(password) > 50:
        return False, "Password cannot exceed 50 characters."
    
    # Regex patterns for password requirements
    patterns = {
        'digit': r'.*\d',                    # At least one digit
        'uppercase': r'.*[A-Z]',             # At least one uppercase letter
        'lowercase': r'.*[a-z]',             # At least one lowercase letter
        'special_char': r'.*[!@#$%^&*(),.?":{}|<>]'  # Optional: at least one special character
    }
    
    # Checking  each requirement
    if not re.match(patterns['digit'], password):
        return False, "Password must contain at least one number (0-9)."
    
    if not re.match(patterns['uppercase'], password):
        return False, "Password must contain at least one uppercase letter (A-Z)."
    
    if not re.match(patterns['lowercase'], password):
        return False, "Password must contain at least one lowercase letter (a-z)."
    
    # checking the password for special characters
    if not re.match(patterns['special_char'], password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)."
    
    # if all checks are passed it will return the following
    return True, "Password is strong."


def display_menu():
    print("\n" + "="*50)
    print("Welcome to JOSHUA SENDAGIRE'S CW2 MULTI DOMAIN PLATFORM $_$")
    print("Secure Authentication System")
    print("="*50)
    print("\n[1]. Register a new user")
    print("[2]. Login")
    print("[3]. Exit")
    print("="*50)




def main():
    # main program loop
    print("\nWelcome to the week 7 Authentication System")
    print("="*50)

    while True:
        display_menu()
        choice = input("Enter your choice(1-3): ").strip()

        if choice == "1":
            # registration flow
            print("\n ---Registering a new user---")
            username = input("Enter username: ").strip()

            # validating username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # checking if the username exists            if user_exists(username):
                print(f"Error: Username '{username}' is already taken. Please choose a different username.")
                continue

            # validating password
            password = input("Enter password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # password confirmation
            password_confirmation = input("Confirm password: ").strip()
            if password_confirmation != password:
                print("Passwords do not match.")
                continue

            register_user(username, password)
            print(f"User '{username}' registered successfully!")

        elif choice == "2":
            print("\n ---User Login---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            # attempting to login
            if login_user(username, password):
                print("Login successful.")
                input("Press enter to return to main menu...")
            else:
                print("Login failed. Check your username and password.")

        elif choice == "3":
            # exiting the program
            print("\nThank you for using SJ's authentication system")
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()








