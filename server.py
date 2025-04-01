from flask import Flask, request, render_template_string, send_file
import threading
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests

app = Flask(__name__)

# Telegram Bot credentials
BOT_TOKEN = "YourToken"
CHAT_ID = "YouIrD"

# HTML template for live log page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ESP32 Irrigation Data</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f4; }
        h1 { color: #007BFF; }
        p { font-size: 18px; font-family: monospace; }
        .log { text-align: left; margin: auto; width: 70%; background: #fff; padding: 10px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); }
    </style>
    <script>
        function refreshData() {
            fetch(window.location.href)
                .then(response => response.text())
                .then(html => document.body.innerHTML = html);
        }
        setInterval(refreshData, 3000);  // Refresh every 3 seconds
    </script>
</head>
<body>
    <h1>ESP32 Smart Irrigation Logs</h1>
    <p><a href="/moisture_plot" target="_blank">📈 View Soil Moisture Graph</a></p>
    <div class="log">
        <p><strong>Live Logs:</strong></p>
        {% for log in logs %}
            <p>{{ log }}</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Rolling log buffer
log_buffer = []

# Send Telegram alert if soil is dry
def send_telegram_alert(moisture, timestamp):
    message = f"🚨 Soil is dry! Moisture = {moisture}% at {timestamp}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        print("Telegram alert sent:", response.json())
    except Exception as e:
        print("Failed to send Telegram alert:", e)

# Root route: render HTML log dashboard
@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template, logs=log_buffer)

# Route to receive ESP32 sensor updates
@app.route("/update", methods=["GET"])
def update_data():
    try:
        # Get query params
        moisture = request.args.get("moisture")
        capacitance = request.args.get("capacitance")
        soil_temp = request.args.get("soil_temp")
        air_temp = request.args.get("air_temp")
        humidity = request.args.get("humidity")

        if None in [moisture, capacitance, soil_temp, air_temp, humidity]:
            return "Missing one or more parameters", 400

        timestamp = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        log = (f"[{timestamp}] Moisture: {moisture}%, Capacitance: {capacitance}, "
               f"Soil Temp: {soil_temp}°F, Air Temp: {air_temp}°F, Humidity: {humidity}%")

        # Update rolling buffer
        if len(log_buffer) >= 20:
            log_buffer.pop(0)
        log_buffer.append(log)
        print(log)

        # Save to CSV
        with open("sensor_log.csv", "a") as file:
            file.write(f"{timestamp},{moisture},{capacitance},{soil_temp},{air_temp},{humidity}\n")

        # Trigger Telegram alert if soil is too dry
        if int(moisture) < 30:
            send_telegram_alert(moisture, timestamp)

        return "Data received", 200

    except Exception as e:
        return str(e), 500

# Moisture graph route
@app.route("/moisture_plot")
def moisture_plot():
    try:
        df = pd.read_csv("sensor_log.csv", names=["timestamp", "moisture", "capacitance", "soil_temp", "air_temp", "humidity"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["moisture"] = pd.to_numeric(df["moisture"], errors="coerce")

        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["moisture"], marker='o', linestyle='-', color='green')
        plt.title("Soil Moisture Over Time")
        plt.xlabel("Timestamp")
        plt.ylabel("Moisture (%)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return send_file(img, mimetype='image/png')

    except Exception as e:
        return f"Error generating plot: {str(e)}"

# Optional: terminal log every 10 seconds
def auto_logger():
    while True:
        time.sleep(10)
        if log_buffer:
            print("[EC2 DEBUG] Latest:", log_buffer[-1])

threading.Thread(target=auto_logger, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
