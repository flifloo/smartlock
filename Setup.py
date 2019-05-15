import io, socket, subprocess, shelve
from requests import post, get
from flask import request, Flask
#hostapd system

#http://192.168.43.155:5000/setup?ssid=cimaphone&password=cimakodu30&id=1

app = Flask(__name__)

def writeconfig(ssid, password):
    rtline = "\n"
    with io.open("/etc/wpa_supplicant/wpa_supplicant.conf", "w", encoding="utf8") as note:
        conf = str()
        for i in ["ctrl_interface=/var/run/wpa_supplicant\nupdate_config=1\ncountry=FR\nnetwork={\nssid=\"", ssid, "\"\nscan_ssid=1\npsk=\"", password, "\"\n}"]:
            conf += i
        note.write(conf)
    subprocess.check_call(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])

def testinternet():
    result = True
    try:
        socket.gethostbyname("www.google.com")
    except:
        result = False
    return result

@app.route("/setup")
def web_setup():
    if not (request.args.get("ssid") and request.args.get("password") and request.args.get("id")):
        return "Error"
    else:
        writeconfig(request.args.get("ssid"), request.args.get("password"))
        if testinternet():
            mac = io.open("/sys/class/net/wlan0/address").read()
            id = request.args.get("id")
            with shelve.open("Settings.conf") as settings:
                settings["token"] = id
            r = get(f"http://vps.flifloo.fr:5000/locksetup?mac={mac}&id={id}")
        else:
            return "Cant connect"
    return "Done"

@app.route("/addyubi")
def add_yubi():
    out = subprocess.check_output(["sudo", "yhsm-decrypt-aead", "--aes-key", "000102030405060708090a0b0c0d0e0f", "--key-handle", "1", "--format", "yubikey-csv", "/var/cache/yubikey-ksm/aeads/"])
    out = out[2:][:-1].split("\\n")
    del out[-1]
    dico = dict()
    for i in out:
        id = i.find(",")
        publicid = i.find(",", id+1)
        privateid = i.find(",", publicid+1)
        secretkey = i.find(",", privateid+1)
        dico[i[:id]] = {"publicid": i[id+1:publicid], "privateid": i[publicid+1:privateid], "secretkey": i[privateid+1:secretkey]}

    with shelve.open("Settings.conf") as settings:
        id = settings["register"][-1] + 1

        if id > dico.keys()[-1]:
            return "Error, too many yubikeys"

        #Verifier si une yubikey est connecter !

        subprocess.check_call(["ykpersonalize", "-1", f"-ofixed={dico[id]["publicid"]}", f"-ouid={dico[id]["privateid"]}", f"-a{dico[id]["secretkey"]}"])

    return "Ok"


if __name__ == "__main__":
    app.run(debug=True, port=6000, host="0.0.0.0")
