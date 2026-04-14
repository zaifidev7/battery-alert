# 🔋 Battery Alert Monitor (Windows)

A lightweight Python script that runs silently in the background and shows **Windows pop-up notifications** when your battery hits critical levels.

## 📢 Alert Levels

| Battery % | Alert Type | Message |
|-----------|-----------|---------|
| **95%** | 🔋 Almost Full | Suggests unplugging to extend battery life |
| **40%** | ⚠️ Getting Low | Recommends plugging in soon |
| **20%** | 🔴 Low Battery! | Urgent warning to plug in immediately |

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.7+ installed → [Download Python](https://www.python.org/downloads/)
- Make sure `pip` is available

### 2. Clone the repo
```bash
git clone https://github.com/zaifidev7/battery-alert.git
cd battery-alert
```

### 3. Run Setup
Double-click `setup.bat` — it will:
- Install required packages (`psutil`, `win10toast`)
- Optionally add the monitor to **Windows startup** so it runs automatically on login

### 4. Start the monitor
```bash
# Option A: Double-click
run_monitor.bat

# Option B: Terminal
python battery_monitor.py
```

---

## ⚙️ Customization

Open `battery_monitor.py` and edit these values at the top:

```python
# Change alert thresholds
ALERT_LEVELS = {
    95: { ... },   # change 95 to any %
    40: { ... },   # change 40 to any %
    20: { ... },   # change 20 to any %
}

# How often to check battery (seconds)
CHECK_INTERVAL = 60   # default: every 1 minute

# Cooldown between repeat alerts (seconds)
ALERT_COOLDOWN = 300  # default: 5 minutes
```

---

## 📁 File Structure

```
battery-alert/
├── battery_monitor.py   # Main script
├── requirements.txt     # Python dependencies
├── setup.bat            # One-click setup + startup registration
├── run_monitor.bat      # Manual launcher
└── README.md
```

---

## 🛠 How It Works

1. Every 60 seconds, the script reads your battery percentage using `psutil`
2. If the battery **crosses a threshold** (going up for 95%, going down for 40%/20%), a Windows toast notification pops up
3. A 5-minute cooldown prevents repeated notifications for the same level
4. The script runs silently in the background — no terminal window when launched via startup

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `psutil` | Read battery stats |
| `win10toast` | Show Windows notifications |

---

## 🤝 Contributing

Pull requests welcome! Feel free to open issues for feature requests.

---

## 📄 License

MIT License — free to use and modify.
