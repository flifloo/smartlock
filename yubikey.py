from yubico_client import Yubico
import lock, shelve

ids = {"interncccccc": 1, "interncccccd": 2}

while True:
    try:
        inp = input(">")
        id = ids[inp[:12]]
        with shelve.open("Settings.conf") as settings:
            client = Yubico(id, settings["keys"][id], api_urls=('http://localhost/wsapi/2.0/verify',))
            #client = Yubico(1, "QMho+Y4mtsY+KbCYu1gRKtDtwAM=", api_urls=('http://localhost/wsapi/2.0/verify',))
        client.verify(inp)
    except:
        pass
    else:
        lock.switch()
