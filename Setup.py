import io, socket, subprocess
from requests import post, get
from flask import request, Flask

#http://192.168.43.155:5000/setup?ssid=cimaphone&password=cimakodu30&id=1

app = Flask(__name__)

def writeconfig(ssid, password):
    rtline = "\n"
    with io.open("/etc/wpa_supplicant/wpa_supplicant.conf", "w", encoding="utf8") as note:
        conf = "ctrl_interface=/var/run/wpa_supplicant\nupdate_config=1\ncountry=FR\nnetwork={\nssid=\""
        conf += ssid
        conf += "\"\nscan_ssid=1\npsk=\""
        conf += password
        conf += "\"\n}"
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
            r = post("http://flifloo.ddns.net:5000/locksetup", data = {"mac": os.open("/sys/class/net/wlan0/address").read(), "id": request.args.get("id")})
        else:
            return "Cant connect"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
