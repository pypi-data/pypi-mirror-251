import requests
import pprint
import shutil

import os
import hashlib
import time
import json
import subprocess
import json

# ignore ssl warnings
requests.packages.urllib3.disable_warnings()

terminal_width, _ = shutil.get_terminal_size()

def getenv():
    myenv = {}
    myenv["IGN8_SELINUX_URL"] = os.getenv("IGN8_SELINUX_URL")
    return myenv

def getsetrouble():
    json_data = []
    command = [
        "journalctl",
        "-u", "setroubleshootd.service",
        "--output", "json",
        "--since", "1 day ago"
    ]

# Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            mytmpdata = json.loads(line)
            mydata = {}
            for key in mytmpdata.keys():
                newkey = key.replace("_", "")
                mydata[newkey] = mytmpdata[key]
            json_data.append(mydata)
        return json_data
    



def digest(mystring):
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()
    # Update the hash object with the bytes representation of the concatenated string
    sha256.update(mystring.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    checksum = sha256.hexdigest()

    return checksum
def calculate_checksum(hostname, event, date, time):
    # Concatenate the variables into a single string
    data_to_hash = f"{hostname}{event}{date}{time}"

    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes representation of the concatenated string
    sha256.update(data_to_hash.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    checksum = sha256.hexdigest()

    return checksum

def alligndateformat(date):
    # the input date format is MM-DD-YYYY
    # the output date format is YYYY-MM-DD
    # this function converts it to YYYYMMDD
    # this is needed for the checksum
    mysplit = date.split('/')
    try:
        date = "%s-%s-%s" % (mysplit[2], mysplit[0], mysplit[1])
    except:
        date = None

    return date

def create_suggestion(suggestion):
    myenv = getenv()
    url = myenv['IGN8_SELINUX_URL'] + '/api/suggestion/upload/'  # Replace with your API endpoint URL
    response = requests.post(url, json=suggestion, verify = False)
    if response.status_code == 201:
        return True
    else:
        if response.status_code == 200:
            return True
        else:
            if response.status_code == 400:
                return True
            else:
                print(f"Failed to upload test event. Status code: {response.status_code}")
                print(response.status_code)
                print(response.text)
                print(response.reason)



def create_message(mymessage):
    myenv = getenv()
    url = myenv['IGN8_SELINUX_URL'] + '/api/message/upload/'  # Replace with your API endpoint URL
    response = requests.post(url, json=mymessage, verify = False)
    if response.status_code == 201:
        return True
    else:
        if response.status_code == 200:
            return True
        else:
            if response.status_code == 400:
                return True
            else:
                print(f"Failed to upload test event. Status code: {response.status_code}")
                print(response.status_code)
                print(response.text)
                print(response.reason)

def create_selinux(hostdata):
    myenv = getenv()
    url = myenv['IGN8_SELINUX_URL'] + '/api/selinux/upload/'  # Replace with your API endpoint URL
    pprint.pprint(url)

    response = requests.post(url, json=hostdata, verify = False)
    if response.status_code == 201:
        return True
    else:
        if response.status_code == 200:
            return True
        else:
            if response.status_code == 400:
                return True
            else:
                print(f"Failed to upload host. Status code: {response.status_code}")
                print(response.status_code)
                print(response.text)
                print(response.reason)

    



def create_setrouble(entry):
    #url = 'https://selinuxapp01fl.unicph.domain/selinux/api/setroubleshoot/upload/'  # Replace with your API endpoint URL
    url = 'https://ignite.openknowit.com:/selinux/api/setroubleshoot/upload/'  # Replace with your API endpoint URL
    #test json string is in a file called testsetrouble.json
    response = requests.post(url, json=entry, verify = False)
    if response.status_code == 201:
        return True
    else:
        if response.status_code == 200:
            return True
        else:
            if response.status_code == 400:
                return True
            else:
                print(f"Failed to upload test event. Status code: {response.status_code}")
                print(response.status_code)
                print(response.text)
                print(response.reason)

def examinemessage(myjson):
    # we need to find sugestions in the message
    suggestfound = False
    suggetsmessages = {}
    suggestnumber = 0
    for line in myjson['MESSAGE'].splitlines():
        if "suggests" in line:
            suggestfound = True
            suggestnumber += 1
            suggestkey = "suggestion%-02d" % suggestnumber
            suggetsmessages[suggestkey]  = line
        if suggestfound:
            suggestkey = "suggestion%-02d" % suggestnumber
            suggetsmessages[suggestkey] += line

    pprint.pprint(suggetsmessages)

def create_metadata():
    # Run the command and capture the output
    #    hostname = models.CharField(max_length=128, primary_key=True)
    #status = models.CharField(max_length=50)
    #mount = models.CharField(max_length=50)
    #rootdir = models.CharField(max_length=50)
    #policyname = models.CharField(max_length=50)
    #current_mode = models.CharField(max_length=50)
    #configured_mode = models.CharField(max_length=50)
    #mslstatus = models.CharField(max_length=50)
    #memprotect = models.CharField(max_length=50)
    #maxkernel = models.CharField(max_length=50)

    sestatus_output = subprocess.check_output(['sestatus'], text=True)
    pprint.pprint(sestatus_output)


    # Parse the output to extract required information
    mymetadata = {}
    mymetadata["hostname"] = os.getenv("HOSTNAME")



    mymetadata["status"] = sestatus_output.split("SELinux status:")[1].split()[0].replace("\n","")
    mymetadata["mount"] = sestatus_output.split("SELinuxfs mount:")[1].split()[0].replace
    mymetadata["rootdir"] = sestatus_output.split("SELinux root directory:")[1].split()[0].replace("\n","")
    mymetadata["policyname"] = sestatus_output.split("Loaded policy name:")[1].split()[0].replace("\n","")
    mymetadata["current_mode"] = sestatus_output.split("Current mode:")[1].split()[0].replace("\n","")  
    mymetadata["configured_mode"] = sestatus_output.split("Mode from config file:")[1].split()[0].replace("\n","")  
    mymetadata["mslstatus"] = sestatus_output.split("Policy MLS status:")[1].split()[0].replace("\n","")    
    mymetadata["memprotect"] = sestatus_output.split("Memory protection checking:")[1].split()[0].replace("\n","")  
    mymetadata["maxkernel"] = sestatus_output.split("Max kernel policy version:")[1].split()[0].replace("\n","")
    #total = models.CharField(max_length=50)
    create_selinux(mymetadata)









def parse():
    create_metadata()
    # ensure the directory exists
    if not os.path.exists("/tmp/ign8/selinux"):
        os.makedirs("/tmp/ign8/selinux")

    setroubles = getsetrouble()
    for myjson in setroubles:
        mandatotyfields = [
                            "BOOTID",
                            "CAPEFFECTIVE",
                            "CMDLINE",
                            "CODEFILE",
                            "CODEFUNC",
                            "CODELINE",
                            "COMM",
                            "CURSOR",
                            "EXE",
                            "GID",
                            "HOSTNAME",
                            "INVOCATIONID",
                            "JOBRESULT",
                            "JOBTYPE",
                            "MACHINEID",
                            "MESSAGE",
                            "MESSAGEID",
                            "MONOTONICTIMESTAMP",
                            "OBJECTPID",
                            "PID",
                            "PRIORITY",
                            "REALTIMETIMESTAMP",
                            "SELINUXCONTEXT",
                            "SOURCEREALTIMETIMESTAMP",
                            "SYSLOGFACILITY",
                            "SYSLOGIDENTIFIER",
                            "SYSTEMDCGROUP",
                            "SYSTEMDINVOCATIONID",
                            "SYSTEMDSLICE",
                            "SYSTEMDUNIT",
                            "TRANSPORT",
                            "UID",
                            "UNIT"
            ]  
        for field in mandatotyfields:
            try:
                test = myjson[field] 
            except:
                myjson[field] = 0

        if myjson["MESSAGE"] is not None:
            mycut = terminal_width  - 15

            if len(myjson['MESSAGE'].replace("\n",";")) > terminal_width - 15:
                cutmessage = myjson['MESSAGE'].replace("\n", ";")[:mycut] + "..."
            else:
                cutmessage = myjson['MESSAGE'].replace("\n", ";")
            if "SELinux is preventing" in myjson["MESSAGE"]:
                examinemessage(myjson)

                mydigest = digest(myjson["MESSAGE"])
                myjson["digest"] = mydigest
                # if the file exists, the event has been uploaded
                if not os.path.exists("/tmp/ign8/selinux/%s" % mydigest):
                    if create_setrouble(myjson):
                        # print the fisrt 100 characters of the message
                        print("OK    : %s" % cutmessage) 
                        #create a file in /tmp/ign8/selinux with the digest as filename
                        # this is used to keep track of what has been uploaded
                        # if the file exists, the event has been uploaded
                        # if the file does not exist, the event has not been uploaded
                        # this is needed for the checksum
                        myfilename = "/tmp/ign8/selinux/%s" % mydigest
                        if not os.path.exists(myfilename):
                            with open(myfilename, 'w') as outfile:
                                json.dump(myjson, outfile)


                    else:
                        
                        print("ERROR : %s" % cutmessage)
                else:
                    print("IGNORE: %s" % cutmessage)
                    


                



def main():
    print("Ignite SELinux parser")





                
if __name__ == '__main__':


    main()

