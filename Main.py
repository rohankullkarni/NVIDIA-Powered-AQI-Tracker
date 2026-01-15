import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime


API_KEY = ""#iqair api key   
AUTO_REFRESH_MS = 300000   
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 540


def get_aqi_category(aqi):

 
    try:
        aqi = int(aqi)
    except Exception:
        return "Unknown", "#808080"
    if aqi <= 50:
        return "Good", "#009966"
    if aqi <= 100:
        return "Moderate", "#ffde33"
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#ff9933"
    if aqi <= 200:
        return "Unhealthy", "#cc0033"
    if aqi <= 300:
        return "Very Unhealthy", "#660099"
    return "Hazardous", "#7e0023"

# Networkin'
def fetch_aqi(use_nearest=False):
    city = city_entry.get().strip()
    state = state_entry.get().strip()
    country = country_entry.get().strip()

    
    if use_nearest or (not city and not state and not country):
        url = "http://api.airvisual.com/v2/nearest_city"
        params = {'key': API_KEY}
    else:
        if not (city and state and country):
            status_label.config(text="Fill all fields or leave all blank for nearest", fg="white")
            return
        url = "http://api.airvisual.com/v2/city"
        params = {
            'city': city,
            'state': state,
            'country': country,
            'key': API_KEY
        }

    try:
        status_label.config(text="Fetching...", fg="white")
        root.update_idletasks()

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get('status') != 'success':
            msg = data.get('data', {}).get('message') or "API error"
            status_label.config(text=f"API error: {msg}", fg="white")
            return

        pollution = data['data']['current']['pollution']
        aqius = pollution.get('aqius')
        if aqius is None:
            status_label.config(text="No AQI data available for this location", fg="white")
            return

        category, color = get_aqi_category(aqius)

        # Update UI
        aqi_value_label.config(text=str(aqius), bg=color, fg="white")
        aqi_status_label.config(text=category, bg=color, fg="white")
        # Update the small card background (so text fields remain readable)
        card_frame.config(bg="#222222")
        # Show location & last update
        location = f"{data['data'].get('city')}, {data['data'].get('state')}, {data['data'].get('country')}"
        location_label.config(text=location, fg="white", bg="#222222")
        last_label.config(text="Last update: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fg="white", bg="#222222")
        status_label.config(text="Updated", fg="white")

        global last_request_params
        last_request_params = (url, params)

    except requests.exceptions.RequestException as e:
        status_label.config(text=f"Network/API error: {e}", fg="white")
    except Exception as e:
        status_label.config(text=f"Unexpected error: {e}", fg="white")


def auto_refresh_loop():
    if last_request_params:
        url, params = last_request_params
        # determine if nearest:
        use_nearest = (url.endswith("/nearest_city"))
        fetch_aqi(use_nearest=use_nearest)
    root.after(AUTO_REFRESH_MS, auto_refresh_loop)


#  GUI
def draw_gradient(canvas, color1, color2):

    canvas.delete("gradient")  
    width = canvas.winfo_width() if canvas.winfo_width() > 1 else WINDOW_WIDTH
    height = canvas.winfo_height() if canvas.winfo_height() > 1 else WINDOW_HEIGHT
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    for i in range(height):
        r = int(r1 + (r2 - r1) * (i / height))
        g = int(g1 + (g2 - g1) * (i / height))
        b = int(b1 + (b2 - b1) * (i / height))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color, tags=("gradient",))

def on_resize(event):
    draw_gradient(canvas, "#1e3c72", "#2a5298")
    # reposition
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    # coordinates
    left = int(w * 0.08)
    top = int(h * 0.08)
    right = int(w * 0.92)
    bottom = int(h * 0.92)
    canvas.coords(overlay_rect, left, top, right, bottom)
    canvas.coords(card_window, w // 2, h // 2)

# Build window 
root = tk.Tk()
root.title("AQI Tracker")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Top-level canvas with gradient
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)
# initial gradient (will be redrawn on resize)
draw_gradient(canvas, "#1e3c72", "#2a5298")

# semi-transparent overlay rectangle (using stipple so gradient shows through)
w0 = WINDOW_WIDTH
h0 = WINDOW_HEIGHT
overlay_rect = canvas.create_rectangle(int(w0*0.08), int(h0*0.08),
                                       int(w0*0.92), int(h0*0.92),
                                       fill="#000000", stipple="gray25", outline="", tags=("overlay",))

card_frame = tk.Frame(root, bg="#222222", bd=0, relief="flat")
card_width = int(WINDOW_WIDTH * 0.76)
card_height = int(WINDOW_HEIGHT * 0.76)
card_window = canvas.create_window(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                   window=card_frame, width=card_width, height=card_height)

# Inside card
title_label = tk.Label(card_frame, text="Air Quality Tracker", font=("TkDefaultFont", 20, "bold"),
                       bg="#222222", fg="white")
title_label.pack(pady=(12, 6))

inputs_frame = tk.Frame(card_frame, bg="#222222")
inputs_frame.pack(pady=6)

lbl_city = tk.Label(inputs_frame, text="City:", bg="#222222", fg="white")
lbl_city.grid(row=0, column=0, padx=(0,6), sticky="e")
city_entry = tk.Entry(inputs_frame, width=20)
city_entry.grid(row=0, column=1, padx=(0,12))

lbl_state = tk.Label(inputs_frame, text="State:", bg="#222222", fg="white")
lbl_state.grid(row=0, column=2, padx=(0,6), sticky="e")
state_entry = tk.Entry(inputs_frame, width=20)
state_entry.grid(row=0, column=3, padx=(0,12))

lbl_country = tk.Label(inputs_frame, text="Country:", bg="#222222", fg="white")
lbl_country.grid(row=0, column=4, padx=(0,6), sticky="e")
country_entry = tk.Entry(inputs_frame, width=20)
country_entry.grid(row=0, column=5)


buttons_frame = tk.Frame(card_frame, bg="#222222")
buttons_frame.pack(pady=(8, 6))

fetch_btn = tk.Button(buttons_frame, text="Fetch AQI (city)", command=lambda: fetch_aqi(use_nearest=False))
fetch_btn.grid(row=0, column=0, padx=6)

nearest_btn = tk.Button(buttons_frame, text="Use Nearest Station", command=lambda: fetch_aqi(use_nearest=True))
nearest_btn.grid(row=0, column=1, padx=6)


status_label = tk.Label(card_frame, text="Ready", bg="#222222", fg="white")
status_label.pack(pady=(4,8))


result_frame = tk.Frame(card_frame, bg="#222222", bd=0, relief="flat")
result_frame.pack(pady=(6,12), fill="x", padx=20)

location_label = tk.Label(result_frame, text="", bg="#222222", fg="white")
location_label.pack()

aqi_value_label = tk.Label(result_frame, text="--", font=("TkDefaultFont", 48, "bold"), bg="#222222", fg="white")
aqi_value_label.pack(pady=(6,4))

aqi_status_label = tk.Label(result_frame, text="", font=("TkDefaultFont", 16), bg="#222222", fg="white")
aqi_status_label.pack()

last_label = tk.Label(card_frame, text="", bg="#222222", fg="white")
last_label.pack(pady=(6,12))


last_request_params = None

# Bind resize so gradient and overlay adapt
canvas.bind("<Configure>", on_resize)

# Start auto-refresh loop
root.after(AUTO_REFRESH_MS, auto_refresh_loop)


root.mainloop()
