import base64
import os
import json
import subprocess
from  ..vault import getlogin
from  ..common import prettyllog




def getenv(myenv):
    myenv['PODMAN_REGISTRY_AUTH_FILE'] = os.environ.get("REGISTRY_AUTH_FILE", "/etc/containers/auth.json")
    if os.path.exists(myenv['PODMAN_REGISTRY_AUTH_FILE']):
        prettyllog("Found auth file: " + myenv['PODMAN_REGISTRY_AUTH_FILE'])
        podmanlogin = subprocess.run(["podman", "login", "--authfile", myenv['PODMAN_REGISTRY_AUTH_FILE']], capture_output=True)
        if podmanlogin.returncode == 0:
            prettyllog("Podman login successful")
            return myenv
        else:
            prettyllog("Podman login failed")
            # check the vauly if we have a new password for the registry
            # if so, update the auth file
            vaultlogin = getlogin("PODMAN_REGISTRY_AUTH_FILE")
            if vaultlogin is not None:
                #clear the auth file and save the new one
                with open(myenv['PODMAN_REGISTRY_AUTH_FILE'], 'w') as f:
                    f.write(json.dumps(vaultlogin))
                #retry the login
                podmanlogin = subprocess.run(["podman", "login", "--authfile", myenv['PODMAN_REGISTRY_AUTH_FILE']], capture_output=True)
                if podmanlogin.returncode == 0:
                    prettyllog("Podman login successful")
                    return myenv
                else:
                    prettyllog("Podman login failed")
                    return None
            return None
    else:
        prettyllog("No auth file found at: " + myenv['PODMAN_REGISTRY_AUTH_FILE'])
        # read the auth file from vault
        vaultlogin = getlogin("PODMAN_REGISTRY_AUTH_FILE")
        if vaultlogin is not None:
            #clear the auth file and save the new one
            with open(myenv['PODMAN_REGISTRY_AUTH_FILE'], 'w') as f:
                f.write(json.dumps(vaultlogin))
            #retry the login
            podmanlogin = subprocess.run(["podman", "login", "--authfile", myenv['PODMAN_REGISTRY_AUTH_FILE']], capture_output=True)
            if podmanlogin.returncode == 0:
                prettyllog("Podman login successful")
                return myenv
            else:
                prettyllog("Podman login failed")
                return None
        return myenv
    






