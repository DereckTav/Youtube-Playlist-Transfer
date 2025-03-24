from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import os
import json

SCOPE = 'https://www.googleapis.com/auth/youtube'

def authorize_user():
    if not os.path.exists('access_token.json') or os.stat('access_token.json').st_size == 0:
        flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', scopes=[SCOPE])  
        flow.authorization_url()

        flow.run_local_server()
        print()

        creds = flow.credentials

        with open('access_token.json', 'w') as file:
            file.write(creds.to_json())
    else:
        with open('access_token.json', 'r') as file:
            token_file = file.read()
            token = json.loads(token_file)
           
        creds = Credentials.from_authorized_user_info(token, SCOPE)
        
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', scopes=[SCOPE])  
            flow.authorization_url()

            flow.run_local_server()
            print()

            creds = flow.credentials

            with open('access_token.json', 'w') as file:
                file.write(creds.to_json())

def delete_token():
    if os.path.exists('access_token.json'):
        with open('access_token.json', 'r') as file:
            token_file = file.read()
            credential = json.loads(token_file)

        refresh_token = credential['refresh_token']
        requests.post('https://oauth2.googleapis.com/revoke',
                params={'token': refresh_token},
                headers = {'content-type': 'application/x-www-form-urlencoded'})
        
        os.remove('access_token.json')

def getCredentials():
    with open('access_token.json', 'r') as file:
        token_file = file.read()
        token = json.loads(token_file)
        
    return Credentials.from_authorized_user_info(token, SCOPE)