from gpiozero import LED
import shelve

led = LED(17)

def state(current : bool = None):
    if current != None:
        with shelve.open("Settings.conf") as settings:
            settings["state"] = current
    else:
        with shelve.open("Settings.conf") as settings:
            return settings["state"]


def unlock():
    led.on()
    state(True)

def lock():
    led.off()
    state(False)

def switch():
    if state():
        lock()
    else:
        unlock()
