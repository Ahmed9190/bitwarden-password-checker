from subprocess import Popen, PIPE
from dotenv import load_dotenv
from twilio.rest import Client
import pexpect
import hashlib
import requests
import json
import os

load_dotenv()

bitwarden_client_id = os.getenv('BITWARDEN_CLIENT_ID')
bitwarden_client_secret = os.getenv('BITWARDEN_CLIENT_SECRET')
bitwarden_master_password = os.getenv('BITWARDEN_MASTER_PASSWORD')
skip_accounts = os.getenv('SKIP_ACCOUNTS').split(',')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_from_number = os.getenv('TWILIO_FROM_NUMBER')
my_phone_number = os.getenv('MY_PHONE_NUMBER')

for acc in skip_accounts:
    location = skip_accounts.index(acc)
    skip_accounts[location] = acc.upper()

try:
    child = pexpect.spawn('bw login --apikey')
    child.expect('client_id.*')
    child.sendline(bitwarden_client_id)
    child.expect('client_secret.*')
    child.sendline(bitwarden_client_secret)
    child.readlines()
except pexpect.exceptions.EOF:
    pass

proc = Popen(['bw','unlock'], stdin=PIPE, encoding='utf-8')
proc.communicate(input=bitwarden_master_password)

proc = Popen(['bw','list','items'], stdin=PIPE, stdout=PIPE, encoding='utf-8')
proc.communicate(input=bitwarden_master_password)
stdout, stderr = proc.communicate()

data = json.loads(stdout.encode('utf-8'))

compromised_passwords = []

for i in data:
    try:
        name = i['name']
        password = i['login']['password']
        hashed_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
        check_api = requests.get('https://api.pwnedpasswords.com/range/' + hashed_pass[:5])

        if hashed_pass[5:].upper() in check_api.text and name.upper() not in skip_accounts:
            compromised_passwords.append({name: password})

    except KeyError:
        pass

if compromised_passwords:
    num = len(compromised_passwords)
    message = f"{len(compromised_passwords)} of your passwords {'has' if num==1 else 'have'} been compromised. Please change the passwords for the following accounts.\n\n"
    
    for entry in compromised_passwords:
        for key, value in entry.items():
            message += f"Account: {key}\nPassword: {value}\n\n"
            
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages \
        .create(
            body=message,
            from_=twilio_from_number,
            to=my_phone_number
        )