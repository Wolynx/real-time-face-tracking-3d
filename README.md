# 🎥 Real-Time 3D Face Tracking with Heatmap

This project performs **real-time face tracking** using a webcam and visualizes
the head position in a **3D virtual space**.

It also generates a **heat map report** showing the most visited positions
in the scene over time.

---

## 🚀 Features

- Real-time face tracking using **MediaPipe Face Mesh**
- Smooth 3D head movement with **EMA filtering**
- 3D scene rendering with **PyVista**
- Motion trail visualization
- Post-session **heat map analysis**
- FPS counter for performance monitoring

---

## 🧠 How It Works

- The **nose landmark** is used as the main reference point
- Face width is used to estimate **depth (Z-axis)**
- Positions are smoothed using an **Exponential Moving Average**
- All positions are stored to generate a **density-based heat map**

---

## 📦 Requirements

- Python 3.9+
- Webcam

Install dependencies:

```bash
pip install -r requirements.txt
