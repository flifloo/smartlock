import shelve
from os.path import isfile

class Main:
    def __init__(self):
        if not isfile("Settings.conf"):
            setup()
        else:
            isconnection()
