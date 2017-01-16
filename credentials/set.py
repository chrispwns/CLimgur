""" Set credentials if necessary """
import os


def set_creds():

    creds = os.path.dirname(os.path.abspath(__file__)) + "\credentials.cred"
    with open(creds, "w+") as f:
        imgur_id = input("ID: ")
        imgur_secret = input("Secret: ")
        cred_string = imgur_id + ":" + imgur_secret
        f.write(cred_string)
        return imgur_id, imgur_secret
