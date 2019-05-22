from yubico_client import Yubico
import lock, shelve

ids = {"interncccccc": 1, "interncccccd": 2, "internccccch": 3, "internccccci": 4, "internccccce": 5, "interncccccg": 6, "interncccccf": 7, "interncccccb": 8, "internccccck": 9, "interncccccj": 10}

while True:
    try:
        inp = input(">")
        id = ids[inp[:12]]
        with shelve.open("Settings.conf") as settings:
            client = Yubico(id, settings["keys"][id], api_urls=('http://localhost/wsapi/2.0/verify',))
        client.verify(inp)
    except KeyboardInterrupt:
        break
    except:
        pass
    else:
        lock.switch(id)
