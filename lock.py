from gpiozero import LED
import shelve, io, requests

led = LED(17)

def state(current : bool = None):
    with shelve.open("Settings.conf") as settings:
        if not "state" in settings:
            settings["state"] = False
    if current != None:
        with shelve.open("Settings.conf") as settings:
            settings["state"] = current
    else:
        with shelve.open("Settings.conf") as settings:
            return settings["state"]


def unlock(keyid = None):
    led.on()
    state(True)
    mac = io.open("/sys/class/net/wlan0/address").read()
    requests.get(f"http://vps.flifloo.fr:5001/logs?mac={mac}&state=unlock&id={str(keyid)}")

def lock(keyid = None):
    led.off()
    state(False)
    requests.get(f"http://vps.flifloo.fr:5001/logs?mac={mac}&state=lock&id={str(keyid)}")

def switch(keyid = None):
    if state():
        lock(keyid)
    else:
        unlock(keyid)
