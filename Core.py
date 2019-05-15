import shelve, subprocess
from os.path import isfile

class Main:
    def __init__(self):
        if not isfile("Settings.conf"):
            subprocess.check_call(["sudo", "yhsm-generate-keys", "-D", "/etc/yubico/yhsm/keys.json", "--key-handle", "1", "--start-public-id", "interncccccc", "-c", "10"])
            out = str(subprocess.check_output(["sudo", "ykval-gen-clients", "--urandom", "10"]))
            out = out[2:-1].split("\\n")
            keys = dict()
            for i in out:
                id = i.find(",")
                keys[i[:id]] = i[id:] #Risque d'y avoir un \n ?
            with shelve.open("Settings.conf") as settings:
                settings["keys"] = keys
                settings["register"] = list()

        else:
            pass
