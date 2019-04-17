from flask import request, Flask
import lock, shelve

app = Flask(__name__)
@app.route("/unlock")
def web_unlock():
    if not (request.args.get("token") and request.args.get("state")):
        return "Error"
    else:
        with shelve.open("Settings.conf") as settings:
            token = settings["token"]
        if request.args.get("token") != token:
            return "Invalid Token"
        if request.args.get("state") == "open":
            lock.unlock()
        elif request.args.get("state") == "close":
            lock.lock()
        elif request.args.get("state") == "switch":
            lock.switch()
        else:
            return "Invalid State"
    return "Done"

@app.route("/state")
def web_state():
    return str(lock.state())

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
