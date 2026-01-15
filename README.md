# NVIDIA-Powered-AQI-Tracker
A desktop Air Quality Index (AQI) Tracker built using Python, Tkinter, and the IQAir AirVisual API. This application fetches real-time air quality data either for a specific city or from the nearest monitoring station, and displays it in a modern, responsive GUI with live auto-refresh.  Developed and tested on NVIDIA Jetson Nano (Linux).

✨ Features

📍 Fetch AQI by City, State, and Country

📡 One-click Nearest Station AQI

🔄 Auto-refresh every 5 minutes

🎨 Color-coded AQI categories (Good → Hazardous)

🕒 Displays last updated time

🖥️ Responsive gradient UI (resizes smoothly)

⚙️ Robust error handling for network & API failures

🧪 AQI Categories Used
AQI Range	Category
0 – 50	Good
51 – 100	Moderate
101 – 150	Unhealthy for Sensitive Groups
151 – 200	Unhealthy
201 – 300	Very Unhealthy
301+	Hazardous
🛠️ Tech Stack

Python 3

Tkinter – GUI framework

Requests – HTTP API calls

IQAir AirVisual API

Linux (Jetson Nano)

📦 Requirements

Install dependencies before running:

pip install requests


Tkinter comes pre-installed with most Python Linux distributions (including Jetson Nano).

🔑 API Setup

Create a free account at:
👉 https://www.iqair.com/air-pollution-data-api

Get your API Key

Add it to the code:

API_KEY = "YOUR_API_KEY_HERE"

▶️ How to Run
python aqi_tracker.py

🧭 Usage
Option 1: City-Based AQI

Enter City, State, and Country

Click Fetch AQI (city)

Option 2: Nearest Station

Leave all fields blank

Click Use Nearest Station

The AQI will update automatically every 5 minutes.

🖼️ UI Overview

Gradient background canvas

Semi-transparent overlay card

Large AQI value display

Color changes based on AQI severity

Responsive resizing support

🔄 Auto Refresh

Auto-refresh interval: 300,000 ms (5 minutes)

Uses last successful request parameters

Runs safely in Tkinter’s event loop

⚠️ Known Limitations

Free IQAir API has rate limits

Requires active internet connection

Nearest station depends on IP-based geolocation

🚀 Future Improvements

🌍 Map-based AQI visualization

📊 Historical AQI graphs

💾 Local AQI data caching

🌙 Dark/Light mode toggle

📱 Mobile-friendly UI (Kivy / Qt)

🧑‍💻 Author

Rohan Kulkarni
Built on NVIDIA Jetson Nano (Linux)


⚠️ License & Usage

© 2026 Rohan Kulkarni. All Rights Reserved.

This project is provided for **viewing and educational reference only**.
No permission is granted to use, copy, modify, or distribute this code,
in whole or in part, without explicit written consent from the author.
