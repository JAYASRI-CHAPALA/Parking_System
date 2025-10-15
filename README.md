# 🚗 ParkEase – Parking Booking & Management Web App

A Flask‑backed web application for managing parking bookings, tracking vehicle entries/exits, and generating invoices.

## 🧾 Features

- **User authentication** (register, login)
- **Car registration**: associate license plate, brand, fuel type
- **Check‑in / Check‑out flow** with timestamp, computing parking duration and cost
- **Invoice generation**: per user, month-based listings, unpaid balances
- **Admin endpoints**: overview of parked cars, sensor alerts, maintenance tools
- **Billboard API**: availability per parking lot & sensor-integrated occupancy detection

## ⚙️ Technology Stack

- **Flask** – micro web framework for routing & backend logic  
- **SQLite** (or other) – local demo DB for storing users, records, invoices  
- **Jinja2 + HTML/CSS** – templating engine for frontend pages  
- **Python (≥ 3.8)** – backend runtime  
- Other dependencies: `flask‑login`, `flask‑sqlalchemy`, `flask‑migrate` (if applicable)

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+ installed
- (Recommended) `virtualenv` or `venv`
- Git

### 🧪 Local Setup

1. Clone your private repo (or open existing clone):
    ```bash
    git clone https://github.com/23f3004085/parking_app.git
    cd parking_app
    ```

2. Create and activate virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate       # macOS/Linux
    # venv\Scripts\activate        # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize database (if required):
    ```bash
    flask db upgrade
    # or
    python init_db.py
    ```

5. Run the server:
    ```bash
    flask run
    ```

6. Open [http://localhost:5000](http://localhost:5000) in your browser and get started!

---

