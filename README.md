# 🌱 GreenCampus Energy Optimizer

An intelligent, AI-driven classroom energy manager built to eliminate electricity waste in smart campuses. 

## 🏆 Hackathon Project

This project uses real-time Computer Vision (OpenCV) to detect human occupancy in a classroom and dynamically manages energy-consuming devices (lights and fans).

### 🚀 Features
- **Real-Time Occupancy Detection:** Leverages laptop webcam to detect student presence.
- **Smart Logic Automation:** 
  - 0 students detected = Everything OFF (Max savings)
  - Occupied = Devices scale proportionally based on headcount.
- **Interactive Dashboard:** Beautiful, modern UI with a live data chart rendering energy savings.
- **AI Feedback Suggestions:** System dynamically advises administrators on how to optimize physical airflow/doors based on current capacity.

### 🛠 Tech Stack
- **Frontend:** HTML5, modern CSS, JavaScript (Vanilla), Chart.js
- **Backend:** Python, Flask
- **Machine Learning:** OpenCV (Haar Cascades for facial recognition)

### ⚙️ How to Run Locally

1. Create a virtual environment (optional)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. Access the dashboard: `http://127.0.0.1:5000`

### 💡 The Problem We Solve
Educational institutions waste massive amounts of electricity by leaving lights and AC units running in empty or low-occupancy rooms. **GreenCampus** completely automates this process without requiring manual human intervention, saving thousands of dollars and significantly reducing carbon footprints.
