import psutil
import time
from win10toast import ToastNotifier
import sys

# Alert thresholds (battery %)
ALERT_LEVELS = {
    95: {
        "title": "🔋 Battery Almost Full",
        "message": "Battery is at 95%. Consider unplugging your charger to extend battery life.",
        "icon": None,
        "duration": 8,
    },
    40: {
        "title": "⚠️ Battery Getting Low",
        "message": "Battery is at 40%. You may want to plug in your charger soon.",
        "icon": None,
        "duration": 8,
    },
    20: {
        "title": "🔴 Low Battery Warning!",
        "message": "Battery is at 20%! Please plug in your charger immediately.",
        "icon": None,
        "duration": 10,
    },
}

# How often to check battery (in seconds)
CHECK_INTERVAL = 60  # every 1 minute

# Cooldown so we don't spam the same alert (in seconds)
ALERT_COOLDOWN = 300  # 5 minutes


def get_battery_info():
    """Returns (percent, is_plugged_in) or None if no battery found."""
    battery = psutil.sensors_battery()
    if battery is None:
        return None
    return battery.percent, battery.power_plugged


def show_notification(title, message, duration=8):
    """Show a Windows toast notification."""
    toaster = ToastNotifier()
    toaster.show_toast(
        title,
        message,
        duration=duration,
        threaded=True,
    )


def main():
    print("✅ Battery Monitor started. Running in background...")
    print(f"   Alerts set at: 95%, 40%, 20%")
    print(f"   Checking every {CHECK_INTERVAL} seconds\n")

    toaster = ToastNotifier()
    last_alert_time = {}  # tracks last time each threshold was alerted

    # Track previous battery level to detect crossing a threshold
    prev_percent = None

    while True:
        try:
            battery_info = get_battery_info()

            if battery_info is None:
                print("No battery detected. Are you on a desktop?")
                time.sleep(CHECK_INTERVAL)
                continue

            percent, plugged = battery_info
            percent_int = int(percent)
            now = time.time()

            status = "Plugged in" if plugged else "On battery"
            print(f"[{time.strftime('%H:%M:%S')}] Battery: {percent_int}% | {status}")

            for threshold, alert in ALERT_LEVELS.items():
                # Check if we just crossed this threshold
                crossed = False

                if prev_percent is not None:
                    if threshold == 95:
                        # Trigger when battery goes UP to/past 95 while plugged in
                        crossed = (plugged and prev_percent < 95 and percent_int >= 95)
                    else:
                        # Trigger when battery drops DOWN to/past threshold (not plugged in)
                        crossed = (not plugged and prev_percent > threshold and percent_int <= threshold)

                # Respect cooldown to avoid repeat spam
                last_time = last_alert_time.get(threshold, 0)
                cooldown_passed = (now - last_time) > ALERT_COOLDOWN

                if crossed and cooldown_passed:
                    print(f"  → 🔔 Sending alert for {threshold}% threshold!")
                    toaster.show_toast(
                        alert["title"],
                        alert["message"],
                        duration=alert["duration"],
                        threaded=True,
                    )
                    last_alert_time[threshold] = now

            prev_percent = percent_int

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
