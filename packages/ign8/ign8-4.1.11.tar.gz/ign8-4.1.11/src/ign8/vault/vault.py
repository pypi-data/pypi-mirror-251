import os
import requests

def getenv(myenv):
    myenv['VAULT_URL'] = os.environ.get("IGN_VAULT_URL", None)
    myenv['VAULT_TOKEN'] = os.environ.get("IGN_VAULT_TOKEN", None)


def checkaccess():
    checkaccess = requests.get("http://localhost:8000/api/v1/healthcheck/")
