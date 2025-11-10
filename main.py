import bcrypt
import os


def hashpassword(plain_text_password):
    # encoding password to bytes
    password_bytes = plain_text_password.encode('utf-8')
    print(f"this is encoding the password =  {password_bytes}")

    #generating a salt to be added to hashed password to make password stronger
    salt = bcrypt.gensalt()
    print(f"this a random salt generated to be added to the password after being converted to bytes = {salt}")

    #hashing the password in bytes and later will need to be converted to string
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    print(f"this is the password being hashed and combined with the salt = {hashed_password_bytes}")

    #hashed passoword being  converted to string
    hashed_password_string = hashed_password_bytes.decode('utf-8')

    return hashed_password_string

def verify_password(hashed_password_string, plain_text_password):
    #converting the plain text password to bytes for comparison
    password_bytes = plain_text_password.encode('utf-8')
    print(f"this is the password being encoded to bytes for comparison = {password_bytes}")

    #converting the hashed password to bytes for comparison
    hashed_bytes = hashed_password_string.encode('utf-8')
    print(f"converting the hashed password to bytes for comparison = {hashed_bytes}")
    # this function extracts the salt from the hash and compares it
    is_valid = bcrypt.checkpw(password_bytes, hashed_bytes)

    print(is_valid)

    return is_valid



pasword = input("Enter password: ")
hashed_password = hashpassword(pasword)
print(f"this is the hashed password = {hashed_password}")

password2 = input("Enter another password: ")
hashed_password2 = hashpassword(password2)

is_valid = verify_password(hashed_password, password2)



