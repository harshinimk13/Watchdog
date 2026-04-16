# app.py
from flask import Flask, render_template, jsonify
from watchdog import Agent, Watchdog
import threading, time

app = Flask(__name__)
agent = Agent()
watchdog = Watchdog()
log = []

def simulation_loop():
    """Background thread that generates new actions every few seconds."""
    while True:
        action = agent.produce_action()
        result = watchdog.evaluate(action)
        record = {**action, **result}
        log.append(record)
        if len(log) > 100:  # keep last 100
            log.pop(0)
        time.sleep(3)  # new action every 3 seconds

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    """Return the latest log as JSON for AJAX polling."""
    return jsonify(log)

if __name__ == "__main__":
    t = threading.Thread(target=simulation_loop, daemon=True)
    t.start()
    app.run(debug=True, port=5000)
