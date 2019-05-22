from gpiozero import LED #OutputDevice
import shelve, io, requests

mac = io.open("/sys/class/net/wlan0/address").read()
led = LED(17)
#open = OutputDevice(17, initial_value = False)
#close = OutputDevice(27, initial_value = False)

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
    #close.off()
    #open.on()
    state(True)
    r = requests.get(f"http://vps.flifloo.fr:5001/logs?mac={mac}&state=unlock&id={str(keyid)}")

def lock(keyid = None):
    #open.off()
    #close.on()
    led.off()
    state(False)
    r = requests.get(f"http://vps.flifloo.fr:5001/logs?mac={mac}&state=lock&id={str(keyid)}")

def switch(keyid = None):
    if state():
        lock(keyid)
    else:
        unlock(keyid)
