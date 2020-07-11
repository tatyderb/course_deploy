"""
Authentication data for Stepik + get token
"""

import sys

API_HOST = 'https://stepik.org'

# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
# client_id = "..."
# client_secret = "..."
# course_id = 1

CLIENT_ID = "..."
CLIENT_SECRET = "..."


def auth_check():
    if CLIENT_ID == '...' or CLIENT_SECRET == '...':
        print('Wrong client credentials.')
        print('Go to https://stepik.org/oauth2/applications/, get authorisation data and write into auth.py file.')
        print('Client type = confidential, authorization grant type = client credentials.')
        sys.exit()


auth_check()
