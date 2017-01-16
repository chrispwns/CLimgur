""" Retrieve the credentials from credentials.cred if it exists """
import os


def get_creds():

    creds = os.path.dirname(os.path.abspath(__file__)) + "\credentials.cred"
    try:
        with open(creds) as f:
            cred_string = f.read()
            cred_string = cred_string.split(":")
            imgur_id = cred_string[0]
            imgur_secret = cred_string[1]
            return imgur_id, imgur_secret
    except FileNotFoundError:
        return False
