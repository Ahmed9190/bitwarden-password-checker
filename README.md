# Bitwarden Password Checker (UNIX Systems ONLY)

## Uses the Bitwarden-cli tool - available [here](https://bitwarden.com/help/cli/) -, the Twilio API, and the HaveIBeenPwned API in order to check the passwords in your vault against the SHA-1 hashes of compromised passwords. If a compromised password is found, it alerts you with a text message.

<br></br>

## In order to setup everything, you must enter all of the necessary information into a .env file. Please note, for the `SKIP_ACCOUNTS` field, account names should be separated by a comma. If you would not like to skip any accounts, simply do not fill in this field, however, do not delete the entry.
## Also, make sure to install all of the necessary dependencies (pexpect, twilio, python-dotenv, requests)

<br></br>

## Also note, your passwords are NEVER exposed to the public HaveIBeenPwned API. Your passwords are taken in plain text from your Bitwarden vault and turned to SHA-1 hashes. Then, ONLY the first 5 characters of the hash are sent to the API, which returns all hashes with the matching characters. This list is then checked against the full hashes stored in a python list.

<br></br>

### Side note on the dependency of UNIX systems. This is because of the need for the pexpect module, which is used to login to your Bitwarden account with your API credentials. The functions which are used are only available for use on UNIX based systems.