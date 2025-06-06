from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

# Data storage
esp_data = {
    "analog_input": 0,
    "danger_level": 0,
    "timestamp": "",
    "emergency": False,
    "red_led": False,
    "blue_led": False,
    "buzzer": False,
    "emergency_led": False,
    "servo_open": False
}

control_data = {
    "emergency_button": False,
    "servo_open": False
}

log_entries = []

@app.route('/')
def index():
    return render_template('esp_dashboard.html')

@app.route("/esp/update", methods=["POST"])
def update_esp():
    global esp_data

    data = request.json
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    esp_data = {
        "analog_input": data.get("analog_input", 0),
        "danger_level": data.get("danger_level", 0),
        "emergency": data.get("emergency", False),
        "red_led": data.get("red_led", False),
        "blue_led": data.get("blue_led", False),
        "buzzer": data.get("buzzer", False),
        "emergency_led": data.get("emergency_led", False),
        "servo_open": data.get("servo_open", False),
        "timestamp": current_time
    }

    if data.get("emergency") is not None:
        event = "EMERGENCY ACTIVATED" if data["emergency"] else "Emergency cleared"
        log_entries.append({
            "event": event,
            "time": current_time,
            "danger_level": esp_data["danger_level"],
            "emergency": data["emergency"]
        })
        if len(log_entries) > 50:
            log_entries.pop(0)

    return jsonify({"message": "ESP data received"})

@app.route("/esp/emergency", methods=["POST"])
def esp_emergency():
    global esp_data, log_entries
    data = request.json
    emergency_state = data.get("emergency", False)
    esp_data["emergency"] = emergency_state

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = "PHYSICAL EMERGENCY BUTTON PRESSED" if emergency_state else "Physical emergency cleared"
    log_entries.append({
        "event": event,
        "time": current_time,
        "danger_level": esp_data["danger_level"],
        "emergency": emergency_state
    })
    if len(log_entries) > 50:
        log_entries.pop(0)

    return jsonify({"message": "Emergency state updated"})

@app.route("/flet/emergency", methods=["POST"])
def flet_emergency():
    global control_data, log_entries
    data = request.json
    emergency_state = data.get("emergency", False)
    control_data["emergency_button"] = emergency_state

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = "FLET EMERGENCY BUTTON PRESSED" if emergency_state else "Flet emergency cleared"
    log_entries.append({
        "event": event,
        "time": current_time,
        "danger_level": esp_data["danger_level"],
        "emergency": emergency_state
    })
    if len(log_entries) > 50:
        log_entries.pop(0)

    return jsonify({"message": "Emergency state updated"})

@app.route("/esp/servo", methods=["POST"])
def control_servo():
    global control_data, log_entries
    data = request.json
    servo_state = data.get("servo_open", False)
    control_data["servo_open"] = servo_state

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = "Servo opened" if servo_state else "Servo closed"
    log_entries.append({
        "event": event,
        "time": current_time,
        "danger_level": esp_data["danger_level"],
        "emergency": esp_data["emergency"]
    })
    if len(log_entries) > 50:
        log_entries.pop(0)

    return jsonify({"message": "Servo state updated"})

@app.route("/esp/servo_status", methods=["GET"])
def get_servo_status():
    return jsonify({"servo_open": control_data["servo_open"]})

@app.route("/esp/control", methods=["GET"])
def control_esp():
    return jsonify(control_data)

@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    return jsonify({
        "esp": esp_data,
        "logs": log_entries[-20:]
    })

if __name__ == "__main__":
    if not os.path.exists('templates'):
        os.makedirs('templates')
    with open('templates/esp_dashboard.html', 'w') as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lab Safety Monitor Dashboard</title>
            <script>
                async function fetchDashboard() {
                    const response = await fetch('/dashboard');
                    const data = await response.json();
                    const esp = data.esp;

                    document.getElementById('analog_input').innerText = esp.analog_input;
                    document.getElementById('danger_level').innerText = esp.danger_level;
                    document.getElementById('emergency').innerText = esp.emergency ? 'YES' : 'NO';
                    document.getElementById('timestamp').innerText = esp.timestamp;
                    document.getElementById('red_led').innerText = esp.red_led;
                    document.getElementById('blue_led').innerText = esp.blue_led;
                    document.getElementById('buzzer').innerText = esp.buzzer;
                    document.getElementById('emergency_led').innerText = esp.emergency_led;
                    document.getElementById('servo_open').innerText = esp.servo_open;

                    const logs = data.logs.map(log =>
                        `<li>[${log.time}] ${log.event} | Danger: ${log.danger_level} | Emergency: ${log.emergency}</li>`
                    ).join('');
                    document.getElementById('log').innerHTML = logs;
                }

                setInterval(fetchDashboard, 2000);
                window.onload = fetchDashboard;
            </script>
        </head>
        <body>
            <h2>Lab Safety Monitor Dashboard</h2>
            <p>Analog Input: <span id="analog_input">Loading...</span></p>
            <p>Danger Level: <span id="danger_level">Loading...</span></p>
            <p>Emergency: <span id="emergency">Loading...</span></p>
            <p>Timestamp: <span id="timestamp">Loading...</span></p>
            <p>Red LED: <span id="red_led">Loading...</span></p>
            <p>Blue LED: <span id="blue_led">Loading...</span></p>
            <p>Buzzer: <span id="buzzer">Loading...</span></p>
            <p>Emergency LED: <span id="emergency_led">Loading...</span></p>
            <p>Servo Open: <span id="servo_open">Loading...</span></p>

            <h3>Recent Log Entries</h3>
            <ul id="log"></ul>
        </body>
        </html>
        """)
    app.run(debug=True, host='0.0.0.0', port=5000)
