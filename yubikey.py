from yubico_client import Yubico
import lock, shelve

with shelve.open("Settings.conf") as settings:
    client = Yubico(settings["id"], settings["secret"], api_urls=('http://localhost/wsapi/2.0/verify',))
while True:
    try:
        client.verify(input())
    except:
        pass
    else:
        lock.switch()
