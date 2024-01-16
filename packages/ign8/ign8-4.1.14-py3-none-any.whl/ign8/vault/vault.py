import os
import requests
import pprint


def getenv(myenv):
    myenv['VAULT_URL'] = os.environ.get("IGN_VAULT_URL", None)
    myenv['VAULT_TOKEN'] = os.environ.get("IGN_VAULT_TOKEN", None)


def checkaccess():
    myenv = getenv({})
    pprint.pprint(myenv)
    if myenv['VAULT_URL'] is None:
        print("No vault URL set")
        return None
    if myenv['VAULT_TOKEN'] is None:
        print("No vault token set")
        return None
    headers = {'X-Vault-Token': myenv['VAULT_TOKEN']}   
    checkaccess = requests.get(myenv['VAULT_URL']+"/api/v1/healthcheck/", headers=headers, verify=False)
    if checkaccess.status_code == 200:
        return True
    else:
        print("Vault access failed")
        return None


def getlogin(path):
    checkaccess()
    vaultlogin = requests.get("http://localhost:8000/api/v1/vault/login/?path=" + path)
    if vaultlogin.status_code == 200:
        return vaultlogin.json()
    else:
        return None