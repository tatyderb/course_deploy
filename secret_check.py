import sys
from auth_data import CLIENT_SECRET, CLIENT_ID


def auth_check():
    if CLIENT_ID == '...' or CLIENT_SECRET == '...':
        print('Wrong client credentials.')
        print('Go to https://stepik.org/oauth2/applications/, get authorisation data and write into auth_data.py file:')
        print("Change this variables: CLIENT_ID = '...', CLIENT_SECRET = '...'")
        print('(For stepik: client type = confidential, authorization grant type = client credentials.)')
        sys.exit()


auth_check()
