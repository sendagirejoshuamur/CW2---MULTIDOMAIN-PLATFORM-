import bcrypt
import os


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
    # handling the case were the file doesnt exist
    try:
        if os.path.isfile(USER_DATA_FILE):
            return False


        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                # this will remove any white space and split by commas in the username
                stored_username = line.strip().split(',')[0]
                if stored_username == username:
                    return True
    # incase there is an error it will print the following plus the error message stored in error
    except Exception as error:
        print(f"Error: {error}")

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






