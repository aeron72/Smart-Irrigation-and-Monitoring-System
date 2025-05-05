# Smart-Irrigation-and-Monitoring-System

Members: Aeron Flores 

**Final Report Document Link:**
https://docs.google.com/document/d/1uENo80Rl8ItnuAQgzOpnZWEjE1_HJCSt/edit?usp=sharing&ouid=100286687965086254125&rtpof=true&sd=true

[Template_Project_Final_Report_CS596.docx.pdf](https://github.com/user-attachments/files/19952225/Template_Project_Final_Report_CS596.docx.pdf)


**Video Demo Link:**
https://youtu.be/ns965L80Z3c

Top Down Images

Pump
![pump1](https://github.com/user-attachments/assets/b4864a67-616f-4819-9e39-e54db3414e8e)

Hygrometer and Sensors
![hygro1](https://github.com/user-attachments/assets/69f18dba-168b-47d9-b9fb-b1d337d8dfed)
![hygro2](https://github.com/user-attachments/assets/782e6ab5-b352-4920-a1ba-7a925fd1318b)


My Smart Irrigation and Monitoring System is an IoT-based solution designed to automate and remotely monitor agricultural irrigation using ESP32 microcontrollers. It continuously tracks soil moisture, soil temperature, air temperature, and humidity using multiple sensors. When the soil is too dry, it automatically activates a water pump through a TCP connection between two ESP32s. All data is sent to a cloud-based Flask server running on AWS EC2, where it's logged, visualized in real time, and monitored via a live web dashboard. The system also sends instant Telegram alerts when critical conditions are detected, ensuring timely and efficient irrigation management.

---

## 🔧 Hardware Used

- 2x **ESP32 Dev Boards**
- 1x **Capacitive Soil Moisture Sensor**
- 1x **DS18B20 Waterproof Soil Temperature Probe (OneWire)**
- 1x **DFRobot DHT20 Temperature & Humidity Sensor (I2C)**
- 2x **TFT Display (TFT_eSPI compatible)**
- 1x **Relay Module**
- 1x **Water Pump (5V)**
- Jumper wires, breadboard, USB cables

---

## 🔌 Wiring Overview

### ESP32 Sensor Node
| GPIO | Component                     |
|------|-------------------------------|
| 33   | Capacitive Moisture Sensor    |
| 32   | OneWire Soil Temp Probe       |
| 21   | DHT20 (I2C SDA)               |
| 22   | DHT20 (I2C SCL)               |

### ESP32 Pump Node
| GPIO | Purpose             |
|------|---------------------|
| 32   | Relay Control Pin 1 |
| 33   | Relay Control Pin 2 |
| 26   | Relay Control Pin 3 |

---

## 📦 Software Stack

### ESP32 Firmware
- **Framework**: Arduino via PlatformIO
- Libraries:
  - `TFT_eSPI`
  - `WiFi.h`
  - `HTTPClient.h`
  - `DFRobot_DHT20`
  - `DallasTemperature`
  - `OneWire`
  - `ESPAsyncWebServer`

### EC2 Server (Python Flask)
- `Flask`
- `requests`
- `matplotlib`
- `pandas`

---

## 🚀 Installation & Setup

### 🖥 EC2 Server (Flask)
1. Install dependencies:
    ```bash
    pip install flask pandas matplotlib requests
    ```
2. Run the server:
    ```bash
    python3 server.py
    ```
3. Access live dashboard:
    ```
    http://<your-ec2-ip>:5000
    ```

### 📲 Telegram Bot Setup
1. Talk to [@BotFather](https://t.me/BotFather) and create a bot.
2. Replace `BOT_TOKEN` and `CHAT_ID` in `server.py`.
3. The server will send a notification when moisture < 30%.

### 🔧 ESP32 Code Upload
Use [PlatformIO](https://platformio.org/) to upload code to each board.

- Sensor ESP32:
    ```ini
    [env:ttgo-lora32-v1]
    platform = espressif32
    board = ttgo-lora32-v1
    framework = arduino
    monitor_speed = 115200
    lib_deps =
      TFT_eSPI
      DFRobot DHT20
      DallasTemperature
    ```

- Pump ESP32:
    ```ini
    [env:ttgo-lora32-v1]
    platform = espressif32
    board = ttgo-lora32-v1
    framework = arduino
    monitor_speed = 115200
    lib_deps =
      ESP Async WebServer
      TFT_eSPI
    ```

---

## 🌐 Web Interface

### EC2 Dashboard
- Live log of sensor data
- Link to soil moisture plot

### Pump ESP32 Dashboard
- Accessible via `http://<pump-esp32-ip>/`
- Toggle GPIO pins 32, 33, 26
- Shows pump status on TFT

---

## 📊 Data & Alerts

- All sensor readings are logged in `sensor_log.csv`.
- Access real-time soil moisture graph at `/moisture_plot`.
- Telegram bot sends alerts when moisture drops below threshold.

---
## Architecture

<img width="714" alt="image" src="https://github.com/user-attachments/assets/65dfdb7d-fbbc-40d5-8b36-769d2142d6bd" />


---
## Data Analytics
<img width="748" alt="image" src="https://github.com/user-attachments/assets/fcd44105-ecf6-4801-bedf-339a43e48ef6" />
AWS stores data for moisture over time.



<img width="244" alt="image" src="https://github.com/user-attachments/assets/ce64bee0-052e-4379-b67b-a8d948213c46" />

AWS also gives sensor data based on current time.

---
## 🧪 Future Improvements

- Add OTA update support
- Deploy live AWS web dashboard using Flask + JS
- Integrate power monitoring
- Add water level detection

---


## ✨ Created by Aeron Flores

